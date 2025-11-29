# 节点订阅管理器Node Subscription Manager
实现多个代理/节点集中起来，通过一个域名提供统一订阅，客户端更新订阅就能获取所有节点。

轻量级节点管理系统，支持 TUIC/VLESS/VMess/Trojan/hy2等等节点统一管理方便域名订阅。
Web后台新增，修改，删除节点。

<img width="1012" height="680" alt="image" src="https://github.com/user-attachments/assets/48df43a8-beb6-4af2-9eac-78d828a51d29" />



## 功能
- Web后台增删改节点。
- 方便不同设备获取订阅后节点备名称会显示在客户端节点备注里面
- Ubuntu 一键部署

## 部署
```bash
git clone https://github.com/999k923/node_sub_manager.git && cd node_sub_manager && chmod +x deploy.sh run.sh stop.sh && ./deploy.sh
```
## 注意
默认监听ipv4，如果是ipv6only vps需要改成监听ipv6后重启
```bash
nano app.py
```
最后一行里面的app.run(host="0.0.0.0", port=5786)改成 app.run(host="::", port=5786)

访问后台：`http://服务器IP:5786/`  

默认用户名密码

WEB_USER = "admin"   # 手动填写用户名

WEB_PASS = "123456"  # 手动填写密码

更改用户名密码
```bash
nano app.py
```

订阅地址：`http://您的IP:5786/sub?token=“TOKEN”`

token安装时候随机生成，并记录在access_token.txt，或者忘记token了，可以重新运行run.sh 再次显示token

重启命令：
```bash
systemctl restart node_sub
```
停止：
```bash
bash stop.sh
```
启动：
```bash
bash run.sh
```

# 查看日志
```bash
journalctl -u node_sub -f
```
