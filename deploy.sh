#!/bin/bash
echo "更新系统..."
sudo apt update && sudo apt upgrade -y

echo "安装 Python3 & pip..."
sudo apt install python3 python3-pip -y

echo "安装依赖..."
pip3 install -r requirements.txt

echo "初始化数据库..."
python3 db_init.py

echo "创建 systemd 服务..."
SERVICE_FILE="/etc/systemd/system/node_sub.service"

sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=Node Subscription Manager
After=network.target

[Service]
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 $(pwd)/app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOL

echo "启动服务并设置开机自启..."
sudo systemctl daemon-reload
sudo systemctl start node_sub
sudo systemctl enable node_sub

# 显示 token
TOKEN=$(python3 -c "from app import get_token; print(get_token())")
echo "部署完成！"
echo "访问后台: http://服务器IP:5786/"
echo "订阅地址访问时需要使用 token: $TOKEN"
