#!/bin/bash
set -e

APP_DIR="/app"
TOKEN_FILE="$APP_DIR/access_token.txt"
DB_FILE="$APP_DIR/nodes.db"

echo "===== Node Sub Manager Startup ====="

# ---------------------------
# 初始化数据库
# ---------------------------
if [ ! -f "$DB_FILE" ]; then
    echo "[INIT] $DB_FILE not found. Initializing database..."
    python3 /app/db_init.py
    echo "数据库初始化完成"
fi

# ---------------------------
# 初始化 token
# ---------------------------
if [ -d "$TOKEN_FILE" ]; then
    echo "[WARN] $TOKEN_FILE is a directory, removing it..."
    rm -rf "$TOKEN_FILE" || echo "无法删除目录，可能被占用"
fi

if [ ! -f "$TOKEN_FILE" ]; then
    echo "[INIT] $TOKEN_FILE not found. Generating new token..."
    touch "$TOKEN_FILE"
    TOKEN=$(python3 -c "import string, random; print(''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20)))")
    echo "$TOKEN" > "$TOKEN_FILE"
fi

echo "Current Token: $(cat $TOKEN_FILE)"
echo "------------------------------------"

# ---------------------------
# 启动 Flask
# ---------------------------
echo "[START] Starting app.py..."
exec python3 /app/app.py
