#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

pipenv run python manage.py migrate
pipenv run python manage.py runserver 0.0.0.0:8000
