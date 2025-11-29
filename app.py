from flask import Flask, Response, render_template, request, redirect, url_for
from models import db, Node
import base64
import os
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nodes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    if not os.path.exists("nodes.db"):
        db.create_all()


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


@app.route("/sub")
def sub():
    nodes = Node.query.filter_by(enabled=True).all()
    out_links = []

    for n in nodes:
        link = n.link.strip()

        # VMESS 节点：vmess://base64_json
        if link.startswith("vmess://"):
            try:
                import json
                raw = link[8:]
                decoded = base64.b64decode(raw + "==").decode()
                j = json.loads(decoded)

                # 用后台备注覆盖 VMESS 的 ps 字段
                j["ps"] = n.name

                # 重新 Base64 编码
                new_raw = base64.b64encode(json.dumps(j).encode()).decode()
                out_links.append("vmess://" + new_raw)

            except Exception as e:
                out_links.append(link)
                continue

        else:
            # 其它协议(VLESS/SS/Trojan...)，清理旧 #备注
            import re
            clean = re.sub(r"#.*$", "", link)
            out_links.append(f"{clean}#{n.name}")

    sub_content = "\n".join(out_links)
    sub_b64 = base64.b64encode(sub_content.encode()).decode()

    return Response(sub_b64, mimetype="text/plain")



if __name__ == "__main__":
    app.run(host="::", port=5786)
