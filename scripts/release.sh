#!/bin/sh

set -eu

[ "$#" -eq 1 ] || { echo "Usage: $0 VERSION" >&2; exit 1; }
version=${1#v}
cd "$(dirname "$0")/.."

[ "$(git branch --show-current)" = main ] || { echo "Run from main." >&2; exit 1; }
[ -z "$(git status --porcelain)" ] || { echo "Commit or stash changes first." >&2; exit 1; }
if git show-ref --verify --quiet "refs/tags/v$version"; then
    echo "Tag v$version already exists." >&2
    exit 1
fi

artifacts=$(mktemp -d)
trap 'rm -rf "$artifacts"' EXIT

python3 - "$version" <<'PY'
import re
import sys
from pathlib import Path

path = Path("great_ai/__init__.py")
source = path.read_text()
current = re.search(r'^__version__ = "([^"]+)"$', source, re.MULTILINE)
version = sys.argv[1]
if not re.fullmatch(r"(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*)){2}", version):
    sys.exit("Version must have X.Y.Z format.")
if current is None or tuple(map(int, version.split("."))) <= tuple(map(int, current[1].split("."))):
    sys.exit("Version must be greater than the current package version.")
path.write_text(source[:current.start(1)] + version + source[current.end(1):])
PY

uv build --python 3.13 --out-dir "$artifacts"
git commit --only -m "Release $version" -- great_ai/__init__.py
git tag -a "v$version" -m "Release $version"
git push --atomic origin HEAD:refs/heads/main "refs/tags/v$version"
