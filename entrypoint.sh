#!/bin/bash
echo "migrating database"
python manage.py migrate

# password comes from secrets/superuserpassword.txt
echo "trying to create the superuser"
python manage.py createsuperuser --noinput --username admin1 --email admin@example.com

python manage.py runserver 0.0.0.0:8000