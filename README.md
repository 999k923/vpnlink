# Node Subscription Manager

轻量级节点管理系统，支持 TUIC/VLESS/VMess/Trojan。
Web后台管理节点，订阅 Base64 自动带备注。

## 功能
- Web后台增删改节点
- 节点备注显示在客户端
- 支持 TUIC/VLESS/VMess/Trojan
- 动态生成 Base64 订阅
- Ubuntu 一键部署

## 部署
```bash
git clone https://github.com/你的用户名/node_sub_manager.git
cd node_sub_manager
chmod +x deploy.sh
./deploy.sh
```
访问后台：`http://服务器IP:5786/`  
订阅地址：`http://服务器IP:5786/sub`
