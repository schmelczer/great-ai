#!/bin/sh

set -e

echo "Installing dependencies if necessary"
python3 -m pip install --upgrade autoflake isort black black[jupyter] mypy flake8

echo "Checking $1"

python3 -m autoflake --expand-star-imports --remove-all-unused-imports --ignore-init-module-imports --remove-unused-variables --in-place -r $1 --check
python3 -m isort --profile black --skip .env $1 --check
python3 -m black $1 --exclude .env --check

yes | python3 -m mypy $1 --install-types > /dev/null || true
python3 -m mypy --namespace-packages --ignore-missing-imports --install-types --non-interactive --disallow-untyped-defs --disallow-incomplete-defs --follow-imports=silent --exclude=external/ --exclude=/build/ --pretty $1

python3 -m flake8 $1 --count --show-source --statistics --exclude=__init__.py,.env,external --ignore=E501,E402,F821,W503,E722,E203
