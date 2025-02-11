#!/bin/bash

source tests/utils.sh

echo "FAIL 1"

python3 --version > /dev/null 2>&1 || { echo -e "${RED}Python3 is not installed!${RESET}"; exit 1; }

echo "FAIL 2"
./tests/test_linters.sh
echo "FAIL 3"
./tests/start_server.sh re
echo "FAIL 4"
./tests/test_playwright.sh
echo "FAIL 5"
./tests/start_server.sh prod
echo "FAIL 6"
./tests/test_playwright.sh
echo "FAIL 7"

echo -e "${GREEN}All tests passed successfully! 🎉${RESET}"
