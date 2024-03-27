FROM python:3.10-slim

ENV OUTPUT_JSON_DIR=/app/city_info
ENV MONGO_URI=mongodb://mongo:27017

WORKDIR /app

COPY src/* /app/

# If you are in China, you can use the following commands to speed up the installation
RUN sed -i 's#http://deb.debian.org/#http://mirrors.aliyun.com/#' /etc/apt/sources.list.d/debian.sources
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install --no-cache-dir -r /app/requirements.txt
RUN apt-get update && apt-get install -y p7zip-full wget && apt-get clean

RUN ln -s /app/geo_engine.py /usr/local/bin/geo-query
