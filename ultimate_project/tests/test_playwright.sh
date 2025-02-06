#!/bin/bash
source tests/utils.sh
echo "Running Playwright tests..."
python3 tests/test_navigation.py > /dev/null 2>&1
check_result "Playwright tests"