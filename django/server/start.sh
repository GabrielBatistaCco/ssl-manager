#!/bin/sh

set -e

while ! nc -z ${DB_HOST} 3306; do
  echo "🟡 Waiting for MariaDB Database Startup..."
  sleep 2
done

echo "✅ MariaDB Database Started Successfully"

crond &
python manage.py makemigrations app_ssl --noinput
python manage.py migrate --noinput

if [[ ${SERVER_IP} == 'localhost' || ${SERVER_IP} == '127.0.0.1' ]]; then
  python manage.py runserver 0.0.0.0:8000
else
  python manage.py runserver_plus 0.0.0.0:8000 --cert-file /etc/ssl/certs/ixc_cert.crt --key-file /etc/ssl/certs/ixc_cert.key
fi

#python manage.py runserver_plus 0.0.0.0:8000 --cert-file /etc/ssl/certs/ixc_cert.crt --key-file /etc/ssl/certs/ixc_cert.key
#python manage.py runserver 0.0.0.0:8000
