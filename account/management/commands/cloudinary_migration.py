from django.core.management.base import BaseCommand
from django.conf import settings
import cloudinary
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import json
import os
import re
import requests

class CloudinaryMigration:
    """
    Class to handle the phased migration of Cloudinary images from one acount to another.
    """
    def __init__(self, batch_size=30):
        cloudinary.config(
            cloud_name=settings.TARGET_CLOUDINARY_CLOUD_NAME,
            api_key=settings.TARGET_CLOUDINARY_API_KEY,
            api_secret=settings.TARGET_CLOUDINARY_API_SECRET
        )

        # Temporary directory for downloads
        self.temp_dir = os.path.join(settings.BASE_DIR, 'temp_cloudinary_images')
        os.makedirs(self.temp_dir, exist_ok=True)

        # Migration state tracking
        self.state_file = os.path.join(settings.BASE_DIR, 'migration_state.json')
        self.batch_size = batch_size

        # Initialize state
        self.load_state()
        
    def load_state(self):
        """Load migration state from file or initialize if not exists"""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
        else:
            self.state = {
                'status': 'pending',
                'last_processed_url_index': 0,
                'last_updated': datetime.now().isoformat(),
                'field_name': '',
                'app_label': '',
                'url_model_map': [],
                'successful_migrations': [],
                'failed_migrations': []
            }
        self.save_state()

    def save_state(self):
        """Save current migration state to file"""
        self.state['last_updated'] = datetime.now().isoformat()
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def collect_urls_from_model(self, model, field_name, app_label):
        """Collect Cloudinary URLs from Django model field"""
        queryset = model.objects.filter()

        url_model_map = []
        for obj in queryset:
            image = getattr(obj, field_name)
            url_model_map.append({
                'url': image.url,
                'instance_id': obj.pk
            })

        self.state['field_name'] = field_name
        self.state['app_label'] = app_label
        self.state['url_model_map'] = url_model_map
        self.save_state()

        return url_model_map

    def extract_info_from_url(self, url):
        """Extract public ID and extension from Cloudinary URL
        """
        parts = url.split('/')
        filename = parts[-1].split('?')[0] # Remove any query parameters

        if '.' not in filename:
            return {
                'public_id': filename,
                'extension': 'jpg' # Default extension if not specified
            }
        
        # Try regex pattern for standard Cloudinary URLs
        regex = r'/v\d+/([^/]+)\.(\w+)(?:\?|$)'
        match = re.search(regex, url)
        if match:
            return {
                'public_id': match.group(1),
                'extension': match.group(2)
            }
        
        # Fallback if regex doesn't match
        if '.' in filename:
            public_id = '.'.join(filename.split('.')[:-1])
            extension = filename.split('.')[-1]
        else:
            public_id = filename
            extension = 'jpg'

        return {
            'public_id': public_id,
            'extension': extension
        }


    def download_image(self, url, index):
        """Download an image from a URL"""
        try:
            info = self.extract_info_from_url()
            temp_path = os.path.join(self.temp_dir, f"{info['public_id']}.{info['extension']}")

            response = requests.get(url, stream=True, timeout=30)
            if response.status_code != 200:
                raise Exception(f"Failed to download")
            
            with open(temp_path, 'wb') as f:
                for  chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

                return temp_path, info
        except Exception as e:
            return None, None
        
    def upload_image(self, temp_path, info, original_url, index):
        """Upload image to new Cloudinary account"""
        if not temp_path:
            return False, None
        
        try:
            upload_result = cloudinary.uploader.upload(
                temp_path,
                public_id=info['public_id'],
                resource_type='auto',
                overwrite=True
            )
            return True, upload_result['secure_url']
        except Exception as e:
            return False, None
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def process_single_url(self, url_data):
        """Process a single URL, for parallel execution"""
        index, data = url_data
        temp_path, info = self.download_image(data.url, index)
        if temp_path:
            success, new_url = self.upload_image(temp_path, info, data.url, index)
            return {
                'index': index,
                'success': success,
                'new_url': new_url,
                'instance_id': data.instance_id
            }
        
        return {
            'index': index,
            'success': False,
            'new_url': None,
            'instance_id': data.instance_id
        }

    def migrate_batch(self, start_index=None):
        """Migrate a batch of URLs"""
        if start_index is None:
            start_index = self.state['last_processed_url_index']
        url_model_map = self.state['url_model_map'][start_index : start_index + self.batch_size]

        # Create a list of (index, url_model_map[index]) tuples for parallel processing
        url_data = [(i + start_index, data) for i, data in enumerate(url_model_map)]

        # Process URLs in parallel
        with ThreadPoolExecutor(max_workers=self.parallel_workers) as executor:
            results = list(executor.map(self.process_single_url, url_data))

        model_updates = []
        for result in results:
            if result['success']:
                self.state['successful_migrations'].append({
                    'instance_id': result['instance_id'],
                    'new_url': result['new_url']
                })
                if result['new_url']:
                    model_updates.append({

                    })
            else:
                self.state['failed_migrations'].append({
                    'instance_id': result['instance_id'],
                    'original_url': result['original_url']
                })

        # Update models with new URLs
        self.update_model_instances(model_updates)

        # Update last processed index
        self.state['last_processed_url_index'] = start_index + len(url_model_map)

        # Check if this batch is done
        if self.state['last_processed_url_index'] >= len(self.state['url_model_map']):
            self.state['status'] = 'completed'
        else:
            self.state['status'] = 'in_progress'

        self.save_state()

        return True


class Command(BaseCommand):
    help = 'Cloudinary migration utility'

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest='command', help='Command to run')

        # Initialize migration
        init_parser = subparsers.add_parser('init', help='Initialize migration')

        # Collect URLs from model
        collect_model_parser = subparsers.add_parser('collect-model', help='Collect URLs from Django model')
        collect_model_parser.add_argument('model', help='Model name (app.ModelName)')
        collect_model_parser.add_argument('field', help='Field name containing Cloudinary URLs')

        # Migrate in batches
        migrate_parser = subparsers.add_parser('migrate-batch', help='Migrate a batch of URLs')
        migrate_parser.add_argument('--start', type=int, help='Start index (default: continue from last batch)')

    def handle(self, *args, **options):
        command = options['command']

        if command == 'init':
            migration = CloudinaryMigration()
            self.stdout.write(self.style.SUCCESS('Migration initialized'))
        elif command == 'collect-model':
            migration = CloudinaryMigration()
            from django.apps import apps
            model_path = options['model'].split('.')
            if len(model_path) != 2:
                self.stdout.write(self.style.ERROR('Model should be in format app.ModelName'))
                return

            app_label, model_name = model_path
            model = apps.get_model(app_label, model_name)
            url_model_map = migration.collect_urls_from_model(model, options['field'], app_label)
            self.stdout.write(self.style.SUCCESS(f"Collected {len(url_model_map)} URLs from {model_name}"))

        elif command == 'migrate-batch':
            migration = CloudinaryMigration()
            start_index = options.get('start')
            success = migration.migrate_batch(start_index)


