from django.apps import apps
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
import cloudinary
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import json
import os
import re
import requests
import sys

class CloudinaryMigration:
    """
    Class to handle the phased migration of Cloudinary images from one account to another,
    preserving the original folder structure.
    """
    def __init__(self, model_path, batch_size=30, target=False, parallel_workers=5):
        if target:
            cloudinary.config(
                cloud_name=settings.TARGET_CLOUDINARY_CLOUD_NAME,
                api_key=settings.TARGET_CLOUDINARY_API_KEY,
                api_secret=settings.TARGET_CLOUDINARY_API_SECRET
            )

        # Temporary directory for downloads
        self.temp_dir = os.path.join(settings.BASE_DIR, 'temp_cloudinary_images')
        os.makedirs(self.temp_dir, exist_ok=True)

        # Migration state tracking
        model_path = model_path.replace('.', '_')
        self.state_file = os.path.join(settings.BASE_DIR, f'{model_path}_migration_state.json')
        self.batch_size = batch_size
        self.parallel_workers = parallel_workers

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
                'model_path': '',
                'urls': ['', {}],
                'successful_migrations': {},
                'failed_migrations': {},
                'model_updates': 0
            }
        self.save_state()

    def save_state(self):
        """Save current migration state to file"""
        self.state['last_updated'] = datetime.now().isoformat()
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def collect_urls_from_model(self, model, model_path, field_name):
        """Collect Cloudinary URLs from Django model field"""
        queryset = model.objects.filter()

        url_model_map = []
        for obj in queryset:
            image = getattr(obj, field_name)
            url_model_map.append({
                'url': image.url,
                'instance_id': obj.pk
            })

        self.state['model_path'] = model_path
        self.state['urls'] = [field_name, url_model_map]
        self.save_state()

        return url_model_map

    def extract_info_from_url(self, url):
        """Extract full path including folders from Cloudinary URL"""
        match = re.search(r'/upload/v\d+/(.+?)(?:\?|$)', url)

        if match:
            full_path = match.group(1)

            # Extract filename from path
            filename = os.path.basename(full_path)

            # Determine extension (default to jpg if not present)
            if '.' in filename:
                extension = filename.split('.')[-1]
            else:
                extension = 'jpg'

            return {
                'public_id': full_path,
                'extension': extension,
                'filename': filename
            }
        
        # Fallback for unusual URL formats
        parts = url.split('/')
        filename = parts[-1].split('?')[0]
        
        if '.' in filename:
            extension = filename.split('.')[-1]
        else:
            extension = 'jpg'
            
        # Use the filename as public_id as a last resort
        return {
            'public_id': filename,
            'extension': extension,
            'filename': filename
        }

    def download_image(self, url, index):
        """Download an image from a URL"""
        try:
            info = self.extract_info_from_url(url)
            temp_filename = f"{info['filename']}.{info['extension']}"
            temp_path = os.path.join(self.temp_dir, temp_filename)

            response = requests.get(url, stream=True, timeout=30)
            if response.status_code != 200:
                raise Exception(f"Failed to download")
            
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
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
                unique_filename=False,
                overwrite=True,
                resource_type='auto',
                use_filename=True,
                folder=''
            )

            cloud_name = settings.TARGET_CLOUDINARY_CLOUD_NAME
            new_url = f"https://res.cloudinary.com/{cloud_name}/image/upload/v1/{info['public_id']}"

            return True, new_url
        except Exception as e:
            return False, None
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def process_single_url(self, url_data):
        """Process a single URL, for parallel execution"""
        index, data = url_data
        temp_path, info = self.download_image(data['url'], index)
        if temp_path:
            success, new_url = self.upload_image(temp_path, info, data['url'], index)
            return {
                'index': index,
                'success': success,
                'new_url': new_url,
                'original_url': data['url'],
                'instance_id': data['instance_id']
            }

        return {
            'index': index,
            'success': False,
            'new_url': None,
            'original_url': data['url'],
            'instance_id': data['instance_id']
        }

    def migrate_batch(self, start_index=None):
        """Migrate a batch of URLs"""
        if start_index is None:
            start_index = self.state['last_processed_url_index']
        field_name, urls = self.state['urls']
        url_model_map = urls[start_index : start_index + self.batch_size]

        # Create a list of (index, url_model_map[index]) tuples for parallel processing
        url_data = [(i + start_index, data) for i, data in enumerate(url_model_map)]

        # Process URLs in parallel
        with ThreadPoolExecutor(max_workers=self.parallel_workers) as executor:
            results = list(executor.map(self.process_single_url, url_data))

        for result in results:
            instance_id = result['instance_id']
            if result['success']:
                self.state['successful_migrations'][instance_id] = self.state['successful_migrations'].get(instance_id, {})
                self.state['successful_migrations'][instance_id][field_name] = result['new_url']
                self.state['successful_migrations'][instance_id]['updated'] = False
            else:
                self.state['failed_migrations'][instance_id] = self.state['failed_migrations'].get(instance_id, {})
                self.state['failed_migrations'][instance_id][field_name] = result['original_url']

        # Update last processed index
        self.state['last_processed_url_index'] = start_index + len(url_model_map)

        # Check if all batches are complete
        if self.state['last_processed_url_index'] >= len(self.state['urls'][1]):
            self.state['status'] = 'completed'
        else:
            self.state['status'] = 'in_progress'

        self.save_state()

        return True

    def update_model_instances(self):
        """Update model instances with new URLs"""
        updated_count = 0
        failed_count = 0
        successful_migrations = self.state['successful_migrations']

        app_label, model_name = self.state['model_path'].split('.')
        model_class = apps.get_model(app_label, model_name)

        # Fetch all instances at once
        instance_ids = [int(id) for id in successful_migrations.keys()]
        instance_dict = {
            str(instance.pk): instance for instance in model_class.objects.filter(pk__in=instance_ids)
        }

        # Process update as atomic transaction
        with transaction.atomic():
            try:
                to_update = []
                for instance_id, data in successful_migrations.items():
                    if data.get('updated', False):
                        continue

                    instance = instance_dict.get(str(instance_id))
                    if not instance:
                        continue

                    updated = False

                    # Update each field that needs updating
                    for field_name, new_url in data.items():
                        if field_name == 'updated':
                            continue

                        setattr(instance, field_name, new_url)
                        updated = True

                    if updated:
                        to_update.append(instance)
                        data['updated'] = True
                        updated_count += 1

                if to_update:
                    # Bulk update all instances of this model
                    fields = list(data.keys()).pop('updated')
                    model_class.objects.bulk_update(to_update, fields)
            except Exception as e:
                failed_count += 1

        self.state['model_updates'] += updated_count
        self.save_state()

        return { 'success': updated_count, 'failed': failed_count }

    def cleanup(self):
        """Clean up temporary files"""
        if os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)


class Command(BaseCommand):
    help = 'Cloudinary migration utility'

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest='command', help='Command to run')

        # Initialize migration
        init_parser = subparsers.add_parser('init', help='Initialize migration')
        init_parser.add_argument('model', help='Model name (app.ModelName)')

        # Collect URLs from model
        collect_model_parser = subparsers.add_parser('collect-model', help='Collect URLs from Django model')
        collect_model_parser.add_argument('model', help='Model name (app.ModelName)')
        collect_model_parser.add_argument('field', help='Field name containing Cloudinary URLs')

        # Migrate in batches
        migrate_parser = subparsers.add_parser('migrate-batch', help='Migrate a batch of URLs')
        migrate_parser.add_argument('model', help='Model name (app.ModelName)')
        migrate_parser.add_argument('--start', type=int, help='Start index (default: continue from last batch)')

        # Update model instances
        update_models_parser = subparsers.add_parser('update-models', help='Update model instances with new URLs')
        update_models_parser.add_argument('model', help='Model name (app.ModelName)')

        # Cleanup
        subparsers.add_parser('cleanup', help='Clean up temporary files')

    def handle(self, *args, **options):
        command = options['command']
        model_path = options['model'].split('.')
        if len(model_path) != 2:
            self.stdout.write(self.style.ERROR('Model should be in format app.ModelName'))
            return

        if command == 'init':
            migration = CloudinaryMigration(options['model'])
            self.stdout.write(self.style.SUCCESS('Migration initialized'))
        elif command == 'collect-model':
            migration = CloudinaryMigration(options['model'])
            app_label, model_name = model_path
            model = apps.get_model(app_label, model_name)
            url_model_map = migration.collect_urls_from_model(model, options['model'], options['field'])
            self.stdout.write(self.style.SUCCESS(f"Collected {len(url_model_map)} URLs from {model_name}"))

        elif command == 'migrate-batch':
            migration = CloudinaryMigration(options['model'], target=True)
            start_index = options.get('start')
            success = migration.migrate_batch(start_index)

            self.stdout.write(self.style.SUCCESS('Batch migration completed'))

        elif command == 'update-models':
            migration = CloudinaryMigration(options['model'])
            result = migration.update_model_instances()

            self.stdout.write(self.style.SUCCESS(f"Updated {result['success']} instances, {result['failed']} failed"))

        elif command == 'cleanup':
            migration = CloudinaryMigration('None.None')
            migration.cleanup()
            self.stdout.write(self.style.SUCCESS('Cleanup completed'))

        else:
            self.stdout.write(self.style.ERROR('Unknown command'))