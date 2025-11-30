#!/bin/sh

DB_FILE="/app/nodes.db"
TOKEN_FILE="/app/access_token.txt"

echo "===== Node Sub Manager Startup ====="

# 初始化数据库
if [ ! -f "$DB_FILE" ]; then
    echo "[INIT] nodes.db not found. Initializing database..."
    python3 db_init.py
else
    echo "[OK] Database already exists."
fi

# 初始化 Token
if [ ! -f "$TOKEN_FILE" ]; then
    echo "[INIT] access_token.txt not found. Generating new token..."
    python3 - <<EOF
import secrets
token = secrets.token_hex(16)
open('/app/access_token.txt', 'w').write(token)
EOF
else
    echo "[OK] Token file exists."
fi

echo "------------------------------------"
echo "Current Token: $(cat $TOKEN_FILE)"
echo "------------------------------------"

echo "[START] Starting app.py..."
python3 app.py
