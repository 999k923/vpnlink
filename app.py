from flask import Flask, Response, render_template, request, redirect, url_for
from models import db, Node
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nodes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# ---------------------------
# Web管理后台
# ---------------------------
@app.route("/")
def index():
    nodes = Node.query.all()
    return render_template("index.html", nodes=nodes)

@app.route("/add", methods=["POST"])
def add_node():
    name = request.form["name"]
    link = request.form["link"]
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

# ---------------------------
# 动态订阅生成
# ---------------------------
@app.route("/sub")
def sub():
    nodes = Node.query.filter_by(enabled=True).all()
    links = [f"{n.link}#{n.name}" for n in nodes]
    sub_content = "\n".join(links)
    sub_base64 = base64.b64encode(sub_content.encode()).decode()
    return Response(sub_base64, mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5786)
