from flask import Flask, Response, render_template, request, redirect, url_for
from models import db, Node
import base64
import os
import re
import json
import secrets

# ---------------------------
# 随机生成访问 token，如果 token.txt 存在则读取
# ---------------------------
TOKEN_FILE = "instance/token.txt"
if not os.path.exists("instance"):
    os.makedirs("instance")

if os.path.exists(TOKEN_FILE):
    with open(TOKEN_FILE, "r") as f:
        ACCESS_TOKEN = f.read().strip()
else:
    ACCESS_TOKEN = secrets.token_urlsafe(16)  # 生成随机 token
    with open(TOKEN_FILE, "w") as f:
        f.write(ACCESS_TOKEN)

# ---------------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/nodes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

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
    link = re.sub(r"#.*$", "", link)

    if name and link:
        node = Node(name=name, link=link)
        db.session.add(node)
        db.session.commit()
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
                j["ps"] = n.name
                new_raw = base64.b64encode(json.dumps(j).encode()).decode()
                out_links.append("vmess://" + new_raw)
            except:
                out_links.append(link)
        # VLESS 节点
        elif link.startswith("vless://"):
            clean = re.sub(r"#.*$", "", link)
            out_links.append(f"{clean}#{n.name}")
        else:
            clean = re.sub(r"#.*$", "", link)
            out_links.append(f"{clean}#{n.name}")

    sub_content = "\n".join(out_links)
    sub_b64 = base64.b64encode(sub_content.encode()).decode()
    return Response(sub_b64, mimetype="text/plain")


# ---------------------------
# 自动更新节点备注
# ---------------------------
def update_node_name(node):
    link = node.link.strip()
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
    elif link.startswith("vless://"):
        clean = re.sub(r"#.*$", "", link)
        node.link = f"{clean}#{node.name}"
        db.session.commit()


# ---------------------------
if __name__ == "__main__":
    print(f"访问订阅链接时需要使用 token: {ACCESS_TOKEN}")
    app.run(host="::", port=5786)
