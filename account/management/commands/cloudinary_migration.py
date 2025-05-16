from django.core.management.base import BaseCommand
from django.conf import settings
import cloudinary
from datetime import datetime
import json
import os

class CloudinaryMigration:
    """
    Class to handle the phased migration of Cloudinary images from one acount to another.
    """
    def __init__(self):
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
                'last_updated': datetime.now().isoformat(),
                'url_model_map': [],
                'failed_migrations': []
            }
        self.save_state()

    def save_state(self):
        """Save current migration state to file"""
        self.state['last_updated'] = datetime.now().isoformat()
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)


class Command(BaseCommand):
    help = 'Cloudinary migration utility'

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest='command', help='Command to run')

        # Initialize migration
        init_parser = subparsers.add_parser('init', help='Initialize migration')

        # Collect URLs from model
        collect_model_parser = subparsers.add_parser('collect-model', help='Collect URLs from Django model')

    def handle(self, *args, **options):
        command = options['command']

        if command == 'init':
            migration = CloudinaryMigration()
            self.stdout.write(self.style.SUCCESS('Migration initialized'))
