#!/bin/sh

set -e

for dir in "$@"; do
    echo "Formatting and checking $dir"

    cd "$dir"

    echo Running autoflake
    python3 -m autoflake --expand-star-imports --remove-all-unused-imports --ignore-init-module-imports --remove-unused-variables --in-place -r .

    echo Running isort
    python3 -m isort --profile black --skip .env .

    echo Running black
    python3 -m black . --exclude .env

    if find . -name "*.py" 2>/dev/null | grep -q .; then
        echo Running mypy

        if [ ! -d .mypy_cache ]; then
            python3 -m mypy --namespace-packages --ignore-missing-imports --disallow-untyped-defs --disallow-incomplete-defs --follow-imports=silent --exclude=external/ --exclude=/build/ --pretty . || true
        fi

        python3 -m mypy --namespace-packages --ignore-missing-imports --install-types --non-interactive --disallow-untyped-defs --disallow-incomplete-defs --follow-imports=silent --exclude=external/ --exclude=/build/ --pretty . || true
    fi

    python3 -m flake8 . --count --show-source --statistics --exclude=__init__.py,.env,external --ignore=E501,E402,F821,W503,E722,E203

    cd -
done
