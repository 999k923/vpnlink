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
        return token

# -------------------------
# 初始化数据库
# -------------------------
with app.app_context():
    db.create_all()

# -------------------------
# 路由
# -------------------------
@app.route('/')
def index():
    try:
        nodes = Node.query.all()
    except Exception as e:
        return f"数据库错误: {e}", 500
    return render_template('index.html', nodes=nodes)

@app.route('/add', methods=['POST'])
def add_node():
    data = request.form
    node = Node(
        name=data.get('name'),
        protocol=data.get('protocol'),
        address=data.get('address'),
        port=int(data.get('port')),
        remark=data.get('remark', '')
    )
    db.session.add(node)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:node_id>', methods=['POST'])
def delete_node(node_id):
    node = Node.query.get_or_404(node_id)
    db.session.delete(node)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/sub')
def get_sub():
    token = request.args.get('token', '')
    if token != get_token():
        abort(403, description="访问订阅需要正确的 token")
    
    nodes = Node.query.all()
    result = ""
    for node in nodes:
        # 简单示例输出，可根据协议格式调整
        result += f"{node.protocol}://{node.address}:{node.port}#{node.remark}\n"
    return result, 200, {'Content-Type': 'text/plain; charset=utf-8'}

# -------------------------
# 启动
# -------------------------
if __name__ == '__main__':
    print(f"访问订阅链接时需要使用 token: {get_token()}")
    app.run(host='::', port=5786)
