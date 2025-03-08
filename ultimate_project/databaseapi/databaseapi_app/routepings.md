curl -X POST http://databaseapi:8007/verify-credentials/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user1", "password":"password"}'
