#!/bin/bash
echo "停止 Node Subscription Manager 并取消开机自启..."
sudo systemctl stop node_sub
sudo systemctl disable node_sub
echo "服务已停止，开机自启已取消"
