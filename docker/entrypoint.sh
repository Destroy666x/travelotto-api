#!/usr/bin/env bash
pipenv install --system
python manage.py migrate
python manage.py runserver 0.0.0.0:8000