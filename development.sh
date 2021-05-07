#!/usr/bin/env sh

yarn install
poetry install

python manage.py makemigrations
python manage.py migrate

exec yarn dev
