#!/bin/bash
# 省略前面安装和依赖部分

# 启动服务
sudo systemctl daemon-reload
sudo systemctl start node_sub
sudo systemctl enable node_sub

# 显示 token
if [ -f "instance/token.txt" ]; then
    TOKEN=$(cat instance/token.txt)
    echo "部署完成！"
    echo "访问后台: http://服务器IP:5786/"
    echo "订阅地址: http://服务器IP:5786/sub?token=$TOKEN"
    echo "请妥善保管 token，避免被他人抓取"
else
    echo "部署完成，但未找到 token 文件！"
fi
