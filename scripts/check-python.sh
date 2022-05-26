#!/bin/sh

set -e

echo "Installing dependencies if necessary"
python3 -m pip install --upgrade autoflake isort black[jupyter] mypy flake8

echo "Checking $1"

cd $1

python3 -m autoflake --expand-star-imports --remove-all-unused-imports --ignore-init-module-imports --remove-unused-variables --in-place -r . --check
python3 -m isort --profile black --skip .env . --check
python3 -m black . --exclude .env --check

yes | python3 -m mypy . --install-types > /dev/null || true
python3 -m mypy --namespace-packages --ignore-missing-imports --install-types --non-interactive --disallow-untyped-defs --disallow-incomplete-defs --follow-imports=silent --exclude=external/ --exclude=/build/ --pretty .

python3 -m flake8 . --count --show-source --statistics --exclude=__init__.py,.env,external --ignore=E501,E722,E402,W503,E203

cd -
