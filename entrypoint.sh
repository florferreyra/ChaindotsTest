#!/bin/sh
set -e

cd app

echo "Applying migrations..."
python manage.py migrate --no-input

# create superuser is doesn't exists
python manage.py shell -c "import os; from django.contrib.auth import get_user_model; User = get_user_model(); \
User.objects.create_superuser(username=os.environ.get('DJANGO_SUPERUSER_USERNAME'), \
email=os.environ.get('DJANGO_SUPERUSER_EMAIL'), password=os.environ.get('DJANGO_SUPERUSER_PASSWORD')) \
if not User.objects.filter(username=os.environ.get('DJANGO_SUPERUSER_USERNAME')).exists() else print('Superuser already exists')"

cd ..

echo "Init Django server..."
exec "$@"
