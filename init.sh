#!/usr/bin/env bash

rm -rv plant_core/migrations || true
python manage.py makemigrations --noinput
python manage.py makemigrations plant_core --noinput
python manage.py migrate
python manage.py collectstatic --noinput
python create_plant_keeper_user.py || true
python init_plant_config.py
