# app.py
from flask import Flask, Response, render_template, request, redirect, url_for
from models import db, Node
import base64
import os
import re
from update_node_name import update_nodes  # 安全导入，无循环依赖

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nodes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# 初始化数据库
with app.app_context():
    if not os.path.exists("nodes.db"):
        db.create_all()


# ---------------------------
# Web管理后台
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

        # 新增节点后自动更新所有 VMESS/VLESS 备注
        update_nodes()

    return redirect(url_for("index"))


@app.route("/delete/<int:node_id>")
def delete_node(node_id):
    node = Node.query.get(node_id)
    if node:
        db.session.delete(node)
        db.session.commit()

        # 删除节点后自动更新备注
        update_nodes()

    return redirect(url_for("index"))


@app.route("/toggle/<int:node_id>")
def toggle_node(node_id):
    node = Node.query.get(node_id)
    if node:
        node.enabled = not node.enabled
        db.session.commit()

        # 切换启用状态后自动更新备注
        update_nodes()

    return redirect(url_for("index"))


@app.route("/edit/<int:node_id>", methods=["POST"])
def edit_node(node_id):
    node = Node.query.get(node_id)
    if node:
        name = request.form.get("name", "").strip()
        link = request.form.get("link", "").strip()

        if name:
            node.name = name
        if link:
            node.link = re.sub(r"#.*$", "", link)

        db.session.commit()

        # 修改节点后自动更新备注
        update_nodes()

    return redirect(url_for("index"))


# ---------------------------
# 动态订阅生成
# ---------------------------
@app.route("/sub")
def sub():
    nodes = Node.query.filter_by(enabled=True).all()
    out_links = []

    for n in nodes:
        link = n.link.strip()

        # VMESS
        if link.startswith("vmess://"):
            import json
            try:
                raw = link[8:]
                decoded = base64.b64decode(raw + "==").decode()
                j = json.loads(decoded)
                j["ps"] = n.name
                new_raw = base64.b64encode(json.dumps(j).encode()).decode()
                out_links.append("vmess://" + new_raw)
            except Exception as e:
                out_links.append(link)
            continue

        # VLESS
        elif link.startswith("vless://"):
            clean = re.sub(r"#.*$", "", link)
            out_links.append(f"{clean}#{n.name}")
            continue

        # 其它协议
        else:
            clean = re.sub(r"#.*$", "", link)
            out_links.append(f"{clean}#{n.name}")

    sub_content = "\n".join(out_links)
    sub_b64 = base64.b64encode(sub_content.encode()).decode()
    return Response(sub_b64, mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="::", port=5786)
