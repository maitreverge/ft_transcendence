#!/bin/bash
source tests/utils.sh
echo "Running Playwright tests..."
python3 tests/test_navigation.py
check_result "Playwright tests"