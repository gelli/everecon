#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

pipenv run celery -A everecon worker -l INFO -B -E
