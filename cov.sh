#!/usr/bin/env bash

export WOLFIT_SETTINGS=$(pwd)/test.settings
export FLASK_ENV=test
export FLASK_DEBUG=0
uv run coverage run --source "app/" --omit "app/commands.py" -m pytest
uv run coverage html

set -e
if grep -qEi "(Microsoft|WSL)" /proc/version &> /dev/null ; then
        sensible-browser htmlcov/index.html
else
        open htmlcov/index.html
fi
