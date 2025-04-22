#!/bin/bash
set -e

export DJANGO_SETTINGS_MODULE=core.settings


python manage.py migrate --noinput
python manage.py collectstatic --noinput

python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='ahmad').exists():
    User.objects.create_superuser('ahmad', '1234', first_name='Ahmad', last_name='Abdurahimov')
EOF

exec gunicorn -c gunicorn_conf.py core.wsgi:application
