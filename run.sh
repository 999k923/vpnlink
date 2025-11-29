#!/bin/bash
# run.sh - 启动 Node Subscription Manager 后台服务，并启用 systemd 开机自启

APP_DIR="/root/node_sub_manager"
APP_FILE="app.py"
PID_FILE="$APP_DIR/node_sub.pid"
SERVICE_FILE="/etc/systemd/system/node_sub.service"
TOKEN_FILE="$APP_DIR/access_token.txt"

# 检查 systemd 服务文件，如果不存在就创建
if [ ! -f "$SERVICE_FILE" ]; then
    echo "创建 systemd 服务文件..."
    cat <<EOF > $SERVICE_FILE
[Unit]
Description=Node Subscription Manager
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$APP_DIR
ExecStart=/usr/bin/python3 $APP_DIR/$APP_FILE
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable node_sub
fi

# 启动 systemd 服务
systemctl start node_sub
echo "服务已启动并设置开机自启"

# 显示订阅 token
if [ -f "$TOKEN_FILE" ]; then
    TOKEN=$(cat "$TOKEN_FILE")
    echo "访问订阅链接时需要使用 token: $TOKEN"
else
    echo "token 文件不存在，请先运行 app.py 生成 token"
fi
