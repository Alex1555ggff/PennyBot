FROM python:3.12-alpine

WORKDIR /app/bot

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ./bot .


RUN apk add --update --no-cache-dir --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

