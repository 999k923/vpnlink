# 使用官方 Python 3.11 slim 作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制代码
COPY . /app

# 安装依赖
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 创建默认挂载目录（确保宿主机映射时不会报错）
RUN mkdir -p /app/nodes.db /app/logs

# 授权脚本
RUN chmod +x /app/run.sh /app/stop.sh /app/deploy.sh /app/entrypoint.sh

# 暴露端口
EXPOSE 5786

# Docker 入口
ENTRYPOINT ["/app/entrypoint.sh"]
