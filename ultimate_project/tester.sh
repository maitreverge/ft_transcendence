#!/bin/bash

source tests/utils.sh

python3 --version > /dev/null 2>&1 || { echo -e "${RED}Python3 is not installed!${RESET}"; exit 1; }

./tests/test_linters.sh
./tests/start_server.sh re
./tests/test_playwright.sh
./tests/start_server.sh prod
./tests/test_playwright.sh

echo -e "${GREEN}All tests passed successfully! 🎉${RESET}"