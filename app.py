from flask import Flask, Response, render_template, request, redirect, url_for
from models import db, Node
import base64
import os
import re
import json

# ---------------------------
# 配置安全访问 token
# ---------------------------
ACCESS_TOKEN = "你的随机字符串"  # 必须替换成自己的随机 token

# ---------------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/nodes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# 初始化数据库
with app.app_context():
    if not os.path.exists("instance/nodes.db"):
        db.create_all()


# ---------------------------
# Web 管理后台
# ---------------------------
@app.route("/")
def index():
    nodes = Node.query.all()
    return render_template("index.html", nodes=nodes)


@app.route("/add", methods=["POST"])
def add_node():
    name = request.form.get("name", "").strip()
    link = request.form.get("link", "").strip()
    # 去掉 link 中自带的 #备注
    link = re.sub(r"#.*$", "", link)

    if name and link:
        node = Node(name=name, link=link)
        db.session.add(node)
        db.session.commit()

        # 自动更新备注覆盖
        update_node_name(node)

    return redirect(url_for("index"))


@app.route("/delete/<int:node_id>")
def delete_node(node_id):
    node = Node.query.get(node_id)
    if node:
        db.session.delete(node)
        db.session.commit()
    return redirect(url_for("index"))


@app.route("/toggle/<int:node_id>")
def toggle_node(node_id):
    node = Node.query.get(node_id)
    if node:
        node.enabled = not node.enabled
        db.session.commit()
    return redirect(url_for("index"))


# ---------------------------
# 动态订阅生成
# ---------------------------
@app.route("/sub")
def sub():
    # 验证 token
    token = request.args.get("token", "")
    if token != ACCESS_TOKEN:
        return "Forbidden", 403

    nodes = Node.query.filter_by(enabled=True).all()
    out_links = []

    for n in nodes:
        link = n.link.strip()

        # VMESS 节点
        if link.startswith("vmess://"):
            try:
                raw = link[8:]
                decoded = base64.b64decode(raw + "==").decode()
                j = json.loads(decoded)
                # 用后台备注覆盖 ps 字段
                j["ps"] = n.name
                new_raw = base64.b64encode(json.dumps(j).encode()).decode()
                out_links.append("vmess://" + new_raw)
            except:
                out_links.append(link)
                continue
        # VLESS 节点
        elif link.startswith("vless://"):
            clean = re.sub(r"#.*$", "", link)
            out_links.append(f"{clean}#{n.name}")
        # 其它协议
        else:
            clean = re.sub(r"#.*$", "", link)
            out_links.append(f"{clean}#{n.name}")

    sub_content = "\n".join(out_links)
    sub_b64 = base64.b64encode(sub_content.encode()).decode()
    return Response(sub_b64, mimetype="text/plain")


# ---------------------------
# 自动更新单条节点备注函数
# ---------------------------
def update_node_name(node):
    link = node.link.strip()
    # VMESS 节点
    if link.startswith("vmess://"):
        try:
            raw = link[8:]
            decoded = base64.b64decode(raw + "==").decode()
            j = json.loads(decoded)
            j["ps"] = node.name
            new_raw = base64.b64encode(json.dumps(j).encode()).decode()
            node.link = "vmess://" + new_raw
            db.session.commit()
        except:
            pass
    # VLESS 节点也可以覆盖
    elif link.startswith("vless://"):
        clean = re.sub(r"#.*$", "", link)
        node.link = f"{clean}#{node.name}"
        db.session.commit()


# ---------------------------
if __name__ == "__main__":
    app.run(host="::", port=5786)
