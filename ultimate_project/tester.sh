#!/bin/bash

# Couleurs pour le feedback
GREEN="\e[32m"
RED="\e[31m"
RESET="\e[0m"

# Fonction pour afficher le résultat d'un test
function check_result {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[✔] $1 passed${RESET}"
    else
        echo -e "${RED}[✘] $1 failed${RESET}"
        exit 1
    fi
}

# Vérification de l'environnement Python
python3 --version > /dev/null 2>&1 || { echo -e "${RED}Python3 is not installed!${RESET}"; exit 1; }

# Installation des dépendances
echo "Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install black flake8 pytest playwright > /dev/null 2>&1
playwright install > /dev/null 2>&1
check_result "Dependency installation"

# Exécution de Black
echo "Running Black..."
black . --check > /dev/null 2>&1
check_result "Black formatting check"

# Exécution de Flake8
echo "Running Flake8..."
flake8 . > /dev/null 2>&1
check_result "Flake8 linting"

# Exécution des tests Playwright
echo "Running Playwright tests..."
python3 tests/test_navigation.py > /dev/null 2>&1
check_result "Playwright tests"

echo -e "${GREEN}All tests passed successfully! 🎉${RESET}"
