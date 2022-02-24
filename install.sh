#!/bin/bash
sudo apt-get update && install default-libmysqlclient-dev
python3 -m venv venv
. venv/bin/activate && pip install -r requirements.txt  && python manage.py makemigrations && python manage.py migrate && python manage.py createcachetable && python manage.py createsuperuser && python manage.py collectstatic --noinput
