#!/bin/bash
set -e

echo "===== Node Sub Manager Startup ====="

# 初始化数据库
if [ ! -f "/app/nodes.db" ]; then
    echo "[INIT] /app/nodes.db not found. Initializing database..."
    python3 db_init.py
    echo "数据库初始化完成"
fi

# 初始化 token 文件（如果不存在）
if [ ! -f "/app/access_token.txt" ]; then
    echo "[INIT] /app/access_token.txt not found. Generating new token..."
    TOKEN=$(python3 -c "import string, random; print(''.join(random.choices(string.ascii_letters + string.digits, k=20)))")
    echo "$TOKEN" > /app/access_token.txt
else
    echo "[INIT] /app/access_token.txt exists"
fi

echo "Current Token: $(cat /app/access_token.txt)"
echo "===================================="

# 启动 Flask 应用
exec python3 app.py
