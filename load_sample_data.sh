#!/usr/bin/env bash
export WOLFIT_SETTINGS=$(pwd)/dev.settings
# Usage: ./load_sample_data.sh [subreddit_name] [count]
# Example: ./load_sample_data.sh learnpython 50
uv run flask sample_data load ${1:+--subreddit "$1"} ${2:+--count "$2"}
