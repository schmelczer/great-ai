#!/bin/sh

set -e

echo "Installing dependencies if necessary"
python3 -m pip install --upgrade autoflake isort black[jupyter] mypy flake8

for dir in "$@"; do
    echo "Checking $dir"

    cd "$dir"

    python3 -m autoflake --expand-star-imports --remove-all-unused-imports --ignore-init-module-imports --remove-unused-variables --in-place -r . --check
    python3 -m isort --profile black --skip .env . --check
    python3 -m black . --exclude .env --check

    if find . -name "*.py" 2>/dev/null | grep -q .; then
        yes | python3 -m mypy . --install-types > /dev/null || true
        python3 -m mypy --namespace-packages --ignore-missing-imports --install-types --non-interactive --disallow-untyped-defs --disallow-incomplete-defs --follow-imports=silent --exclude=external/ --exclude=/build/ --pretty .
    fi

    python3 -m flake8 . --count --show-source --statistics --exclude=__init__.py,.env,external --ignore=E501,E402,F821,W503,E722,E203

    cd -
done
