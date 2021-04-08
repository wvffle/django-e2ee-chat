#!/usr/bin/env sh

yarn install
poetry install

# shellcheck disable=SC2046
# shellcheck disable=SC2006
if [ ! `command -v git` ]; then
  apk update
  apk add git
fi
poetry run pre-commit install --hook-type commit-msg --hook-type pre-commit

exec poetry run yarn dev
