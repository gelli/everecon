#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset

pipenv run celery -A everecon worker -l INFO
