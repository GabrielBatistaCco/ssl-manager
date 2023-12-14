#!/bin/sh

set -e

while ! nc -z mongo-db 27017; do
  echo "🟡 Waiting for Mongodb Database Startup..."
  sleep 2
done

echo "✅ Mongodb Database Started Successfully"

# python manage.py collectstatic --noinput
python manage.py makemigrations app_ssl --noinput
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000
