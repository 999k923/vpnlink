#!/bin/bash
echo "启动 Node Subscription Manager..."
sudo systemctl start node_sub
sudo systemctl enable node_sub
echo "服务已启动并设置开机自启"

# 显示 token
TOKEN=$(python3 -c "from app import get_token; print(get_token())")
echo "访问订阅时需要使用 token: $TOKEN"
echo "访问后台: http://服务器IP:5786/"
echo "订阅地址访问时需要使用 token: $TOKEN"
