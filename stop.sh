#!/bin/bash
# stop.sh - 停止 Node Subscription Manager 后台服务，并取消开机自启

SERVICE_NAME="node_sub"
APP_DIR="/root/node_sub_manager"
PID_FILE="$APP_DIR/node_sub.pid"

# 停止 systemd 服务
if systemctl list-units --all | grep -q "$SERVICE_NAME.service"; then
    systemctl stop $SERVICE_NAME
    systemctl disable $SERVICE_NAME
    echo "服务已停止并取消开机自启 (systemd)"
fi

# 如果还有 PID 文件，尝试杀掉 nohup 进程
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null 2>&1; then
        kill $PID
        echo "后台进程已停止 (PID: $PID)"
    fi
    rm -f "$PID_FILE"
fi
