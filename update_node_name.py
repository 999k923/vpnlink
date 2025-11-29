# update_node_name.py
from app import app, db
from models import Node
import base64
import json
import re

def update_nodes():
    """
    批量更新数据库里 VMESS 和 VLESS 节点的备注
    """
    with app.app_context():
        nodes = Node.query.all()
        updated_count = 0

        for n in nodes:
            link = n.link.strip()

            # VMESS
            if link.startswith("vmess://"):
                try:
                    raw = link[8:]
                    decoded = base64.b64decode(raw + "==").decode()
                    j = json.loads(decoded)
                    j["ps"] = n.name
                    new_raw = base64.b64encode(json.dumps(j).encode()).decode()
                    n.link = "vmess://" + new_raw
                    updated_count += 1
                except Exception as e:
                    print(f"VMESS 更新失败 id={n.id}：{e}")

            # VLESS
            elif link.startswith("vless://"):
                try:
                    clean = re.sub(r"#.*$", "", link)
                    n.link = f"{clean}#{n.name}"
                    updated_count += 1
                except Exception as e:
                    print(f"VLESS 更新失败 id={n.id}：{e}")

            # 其它协议节点，可按需处理
            else:
                pass

        db.session.commit()
        print(f"✅ 更新完成，总共 {updated_count} 个节点")
