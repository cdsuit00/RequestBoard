#!/bin/bash
# test_backend.sh
# Automated testing script for RequestBoard backend

BASE_URL="http://127.0.0.1:5000/api"

echo "=== 1️⃣ Signup new user ==="
SIGNUP_RESPONSE=$(curl -s -X POST $BASE_URL/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "password": "password123"
  }')
echo $SIGNUP_RESPONSE
echo

echo "=== 2️⃣ Login user ==="
LOGIN_RESPONSE=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "password": "password123"
  }')
echo $LOGIN_RESPONSE
echo

ACCESS_TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

echo "=== 3️⃣ Create a new request ==="
CREATE_REQUEST=$(curl -s -X POST $BASE_URL/requests \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "title": "Fix bug in login",
    "description": "Login fails when password is empty",
    "priority": "High"
  }')
echo $CREATE_REQUEST
echo

REQUEST_ID=$(echo $CREATE_REQUEST | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")

echo "=== 4️⃣ Get paginated list of requests ==="
curl -s -X GET "$BASE_URL/requests?page=1&per_page=10" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
echo
echo

echo "=== 5️⃣ Update request ==="
curl -s -X PATCH $BASE_URL/requests/$REQUEST_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"status": "In Progress"}'
echo
echo

echo "=== 6️⃣ Add response to request ==="
curl -s -X POST $BASE_URL/requests/$REQUEST_ID/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"content": "Started working on this bug."}'
echo
echo

echo "=== 7️⃣ Get all responses for request ==="
curl -s -X GET $BASE_URL/requests/$REQUEST_ID/responses \
  -H "Authorization: Bearer $ACCESS_TOKEN"
echo
echo

echo "=== 8️⃣ Delete request ==="
curl -s -X DELETE $BASE_URL/requests/$REQUEST_ID \
  -H "Authorization: Bearer $ACCESS_TOKEN"
echo
echo "✅ Test script completed"
