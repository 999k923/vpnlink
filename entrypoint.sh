#!/bin/bash
set -e

# --------------------------
# 初始化数据库
# --------------------------
if [ ! -f /app/nodes.db ]; then
    echo "[INIT] nodes.db not found. Initializing database..."
    python3 /app/db_init.py
    echo "数据库初始化完成"
fi

# --------------------------
# 初始化 token 文件
# --------------------------
TOKEN_FILE="/app/access_token.txt"

# 如果 access_token.txt 是目录（Docker 映射错），先删除
if [ -d "$TOKEN_FILE" ]; then
    echo "[WARN] $TOKEN_FILE is a directory, removing it..."
    rm -rf "$TOKEN_FILE"
fi

# 如果文件不存在或为空，生成 token
if [ ! -s "$TOKEN_FILE" ]; then
    echo "[INIT] access_token.txt not found or empty. Generating new token..."
    python3 - <<EOF
import os, random, string
token_file = "/app/access_token.txt"
chars = string.ascii_letters + string.digits
token = ''.join(random.choice(chars) for _ in range(20))
with open(token_file, "w") as f:
    f.write(token)
print(f"访问订阅链接时需要使用 token: {token}")
EOF
fi

# 启动 Flask 应用
exec python3 /app/app.py
