FROM python:3.11-slim

# 安装依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 复制文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 赋予脚本执行权限
RUN chmod +x entrypoint.sh

# 入口
ENTRYPOINT ["/app/entrypoint.sh"]
