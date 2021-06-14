#!/usr/bin/env sh

apk add gcc g++ make libffi-dev openssl-dev python3-dev build-base linux-headers zlib-dev jpeg-dev musl-dev cargo

yarn install
poetry install

poetry run python manage.py makemigrations
poetry run python manage.py migrate

exec yarn dev
