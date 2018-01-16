#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

pipenv run python manage.py migrate
pipenv run python manage.py runserver_plus 0.0.0.0:8000