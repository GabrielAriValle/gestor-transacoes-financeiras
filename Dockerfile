FROM python:3.11-slim

WORKDIR /app

COPY requirements/base.txt /app/
RUN pip install --no-cache-dir -r base.txt

COPY . /app/

EXPOSE 8000
