#!/usr/bin/env bash
export WOLFIT_SETTINGS=$(pwd)/dev.settings
uv run flask sample_data load
