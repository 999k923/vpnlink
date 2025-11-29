#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import string
import random
from flask import Flask, request, render_template, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy

# -------------------------
# 基础配置
# -------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
DB_PATH = os.path.join(INSTANCE_DIR, 'nodes.db')

# 创建 instance 文件夹
os.makedirs(INSTANCE_DIR, exist_ok=True)
# 确保 instance 目录可写
os.chmod(INSTANCE_DIR, 0o775)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------------
# 数据库模型
# -------------------------
class Node(db.Model):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    protocol = db.Column(db.String(50))
    address = db.Column(db.String(255))
    port = db.Column(db.Integer)
    remark = db.Column(db.String(255))  # 节点备注

# -------------------------
# Token 生成/读取
# -------------------------
TOKEN_FILE = os.path.join(INSTANCE_DIR, 'access_token.txt')

def generate_token(length=20):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def get_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            return f.read().strip()
    else:
        token = generate_token()
        with open(TOKEN_FILE, 'w') as f:
            f.write(token)
        os.chmod(TOKEN_FILE, 0o600)  # 文件安全权限
        return token

# -------------------------
# 初始化数据库
# -------------------------
with app.app_context():
    db.create_all()
    # 确保数据库文件可写
    if os.path.exists(DB_PATH):
        os.chmod(DB_PATH, 0o664)

# -------------------------
# 路由
# -------------------------
@app.route('/')
def index():
    try:
        nodes = Node.query.all()
    except Exception as e:
        return f"数据库错误: {e}", 500
    return render_template('index.html', nodes=nodes, token=get_token())

@app.route('/add', methods=['POST'])
def add_node():
    try:
        data = request.form
        node = Node(
            name=data.get('name'),
            protocol=data.get('protocol'),
            address=data.get('address'),
            port=int(data.get('port', 0)),
            remark=data.get('remark', '')
        )
        db.session.add(node)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return f"添加节点失败: {e}", 500
    return redirect(url_for('index'))

@app.route('/delete/<int:node_id>', methods=['POST'])
def delete_node(node_id):
    try:
        node = Node.query.get_or_404(node_id)
        db.session.delete(node)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return f"删除节点失败: {e}", 500
    return redirect(url_for('index'))

@app.route('/sub')
def get_sub():
    token = request.args.get('token', '')
    if token != get_token():
        abort(403, description="访问订阅需要正确的 token")
    
    try:
        nodes = Node.query.all()
    except Exception as e:
        return f"读取订阅失败: {e}", 500

    result = ""
    for node in nodes:
        result += f"{node.protocol}://{node.address}:{node.port}#{node.remark}\n"
    return result, 200, {'Content-Type': 'text/plain; charset=utf-8'}

# -------------------------
# 启动
# -------------------------
if __name__ == '__main__':
    print(f"访问订阅链接时需要使用 token: {get_token()}")
    app.run(host='::', port=5786)
