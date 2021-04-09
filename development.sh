#!/usr/bin/env sh

yarn install
poetry install

exec yarn dev
