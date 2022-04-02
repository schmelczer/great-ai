#!/bin/bash

set -e

echo "Installing dependencies if necessary"
python3 -m pip install --upgrade autoflake isort black black[jupyter] mypy

echo "Formatting and checking $1"

echo Running autoflake
python3 -m autoflake --expand-star-imports --remove-all-unused-imports --ignore-init-module-imports --remove-unused-variables --in-place -r $1

echo Running isort
python3 -m isort --profile black --skip .env $1

echo Running black
python3 -m black $1 --exclude .env

echo Running mypy
python3 -m mypy --namespace-packages --ignore-missing-imports --install-types --non-interactive --disallow-untyped-defs --disallow-incomplete-defs --pretty --follow-imports=silent --exclude=external/ --exclude=/build/ $1