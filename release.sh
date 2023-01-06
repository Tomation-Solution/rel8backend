#!/bin/sh

python manage.py migrate_schemas --shared
python manage.py migrate

python manage.py init_public_client
python manage.py init_admin
