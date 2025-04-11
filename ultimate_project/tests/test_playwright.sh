#!/bin/bash
source tests/utils.sh

start=$(date +%s)

# make clean

# make delete_volume re > /dev/null 2>&1 &

# echo "⏳ Attente que le serveur soit prêt..."

# until curl -k -s -o /dev/null -w "%{http_code}" https://localhost:8443/login | grep 200 > /dev/null; do

# echo "⏳ NOT READY YET"
#   sleep 1
# done

echo "✅ Serveur prêt, lancement des tests..."
echo "Running Playwright tests..."
#
python3 tests/test_authentication.py
sleep 1
python3 tests/test_2fa.py
sleep 1
python3 tests/test_cookies.py
sleep 1
python3 tests/test_username.py
sleep 1
python3 tests/test_sametime_auth.py
sleep 1
python3 tests/test_xss_sql.py
sleep 1
python3 tests/test_navigation.py
check_result "Playwright tests"

end=$(date +%s)
elapsed=$((end - start))
echo "⏱️ Tests terminés en $elapsed secondes"