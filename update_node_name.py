from app import app, db
from models import Node
import base64
import json
import re

with app.app_context():
    nodes = Node.query.all()
    updated_count = 0

    for n in nodes:
        link = n.link.strip()
        original_link = link

        # VMESS 节点
        if link.startswith("vmess://"):
            try:
                raw = link[8:]
                decoded = base64.b64decode(raw + "==").decode()
                j = json.loads(decoded)
                # 覆盖或添加 ps
                j["ps"] = n.name
                new_raw = base64.b64encode(json.dumps(j).encode()).decode()
                n.link = "vmess://" + new_raw
                updated_count += 1
            except Exception as e:
                print(f"VMESS 节点更新失败 id={n.id}：{e}")

        # VLESS 节点
        elif link.startswith("vless://"):
            try:
                # 移除原 #备注，添加后台 name
                clean = re.sub(r"#.*$", "", link)
                n.link = f"{clean}#{n.name}"
                updated_count += 1
            except Exception as e:
                print(f"VLESS 节点更新失败 id={n.id}：{e}")

        # 其它协议，可选覆盖
        else:
            # 如果想覆盖 #备注，也可以打开下面一行
            # n.link = re.sub(r"#.*$", "", link) + f"#{n.name}"
            pass

    db.session.commit()
    print(f"✅ 批量更新完成，总共更新 {updated_count} 个节点")
