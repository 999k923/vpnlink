# 基于轻量 Python 镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 确保 token 文件存在，避免 IsADirectoryError
RUN touch access_token.txt

# 设置 Flask 使用环境变量的 host 和 port
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5786

# 暴露端口
EXPOSE 5786

# 启动服务，读取环境变量
CMD ["python3", "app.py"]
