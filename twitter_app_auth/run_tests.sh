#!/usr/bin/env bash

GREEN='\033[0;32m'

# Export PYTHONPATH
export PYTHONPATH=`pwd`

# Install all python modules used for automation
pip install -r requirements.txt

# Run all tests
py.test --junitxml results.xml --html=reports/index.html \
-s -v tests/api/ --disable-pytest-warnings

# Print info after test completion
echo -e "${GREEN}===================================
All tests have completed.

You can check HTML format reports under ./reports/index.html
You can check logs in file ./twitter_auth.log
==================================="

