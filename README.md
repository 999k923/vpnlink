# 节点订阅管理器Node Subscription Manager
实现多个代理/节点集中起来，通过一个域名提供统一订阅，客户端更新订阅就能获取所有节点。

轻量级节点管理系统，支持 TUIC/VLESS/VMess/Trojan/hy2等等节点统一管理方便域名订阅。
Web后台新增，修改，删除节点。

访问后台：`http://服务器IP:5786/`  
订阅地址：`http://您的IP:5786/sub?token=“TOKEN”`

<img width="1012" height="680" alt="image" src="https://github.com/user-attachments/assets/48df43a8-beb6-4af2-9eac-78d828a51d29" />



## 功能
- Web后台增删改节点。
- 方便不同设备获取订阅后节点备名称会显示在客户端节点备注里面
- Ubuntu 一键部署

## 一键部署
```bash
git clone https://github.com/999k923/node_sub_manager.git && cd node_sub_manager && chmod +x deploy.sh run.sh stop.sh && ./deploy.sh
```
## 注意## 注意
默认监听ipv4，如果是ipv6 only vps,需要把部署文件里面的监听改成监听ipv6后重启
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

## docker compose部署  docker部署有报错，问AI 可以解决，或者用上面的一键部署不会有报错。
```bash
services:
  node_sub_manager:
    image: 999k923/node_sub_manager:latest
    container_name: node_sub_manager
    restart: always

    ports:
      - "5786:5786"

    volumes:
      - ./nodes.db:/app/nodes.db
      - ./access_token.txt:/app/access_token.txt
      - ./logs:/app/logs

    environment:
      - FLASK_RUN_HOST=0.0.0.0
      - FLASK_RUN_PORT=5786
```
如果报错shh界面运行下面代码：
```bash
rm -rf /opt/stacks/node/access_token.txt
```
```bash
touch /opt/stacks/node/access_token.txt
```
```bash
docker exec -it node_sub_manager /bin/bash
```
```bash
python3 db_init.py
```

docker部署后获取不到订阅检查订阅tocken有没有正确生成，
```bash
docker exec -it node_sub_manager cat /app/access_token.txt
```
获取不到token，手动写入
1. 删除旧 token 文件
```bash
rm -f /opt/stacks/node/access_token.txt
```
3. 写入新的 token
```bash
echo "abc123xyz" > /opt/stacks/node/access_token.txt
```
5. 重启服务
```bash
docker restart node_sub_manager
```

还是那句话还有其他问题问AI可以解决，或者用上面的一键部署不会有报
