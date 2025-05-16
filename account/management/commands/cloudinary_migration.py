from django.core.management.base import BaseCommand
from django.conf import settings
import cloudinary
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
