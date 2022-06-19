#!/bin/sh

set -e

echo "Installing dependencies if necessary"
python3 -m pip install --upgrade autoflake isort black[jupyter] mypy flake8

echo "Formatting and checking $1"

cd $1

echo Running autoflake
python3 -m autoflake --expand-star-imports --remove-all-unused-imports --ignore-init-module-imports --remove-unused-variables --in-place -r .

echo Running isort
python3 -m isort --profile black --skip .env .

echo Running black
python3 -m black . --exclude .env

if ls *.py 1> /dev/null 2>&1; then
    echo Running mypy
    python3 -m mypy --namespace-packages --ignore-missing-imports --install-types --non-interactive --disallow-untyped-defs --disallow-incomplete-defs --pretty --follow-imports=silent --exclude=external/ --exclude=/build/ .
fi

echo Running Flake8
python3 -m flake8 . --count --show-source --statistics --exclude=__init__.py,.env,external --ignore=E501,E722,E402,W503,E203

cd -

echo "Finished formatting"
