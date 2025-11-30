FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# 给启动脚本执行权限
RUN chmod +x entrypoint.sh

EXPOSE 5786

ENTRYPOINT ["./entrypoint.sh"]
