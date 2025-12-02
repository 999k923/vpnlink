#!/bin/bash
# run.sh - 使用 gunicorn 启动 Node Subscription Manager + systemd 保活

APP_DIR="/root/node_sub_manager"
SERVICE_FILE="/etc/systemd/system/node_sub.service"

echo "=== 安装依赖 (gunicorn) ==="
apt update -y
apt install python3-pip -y
pip install gunicorn flask

echo "=== 创建或覆盖 systemd 服务文件 ==="

cat <<EOF > $SERVICE_FILE
[Unit]
Description=Node Subscription Manager
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=$APP_DIR
ExecStart=/usr/bin/gunicorn -b 0.0.0.0:5786 app:app
Restart=always
RestartSec=3
User=root
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

echo "=== 重新加载 systemd 配置 ==="
systemctl daemon-reload

echo "=== 设置开机自启 ==="
systemctl enable node_sub

echo "=== 重启并启动服务 ==="
systemctl restart node_sub

echo "=== 查看服务状态 ==="
sleep 1
systemctl status node_sub --no-pager -n 20
