#!/usr/bin/env bash

pipenv run python manage.py makemigrations --noinput
pipenv run python manage.py makemigrations plant_core --noinput
pipenv run python manage.py migrate
pipenv run python manage.py collectstatic --noinput
pipenv run python create_plant_keeper_user.py || true
pipenv run python init_plant_config.py