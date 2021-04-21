FROM python:3.8-alpine

RUN apk add --update --no-cache g++ gcc postgresql-dev libffi-dev zlib-dev jpeg-dev musl-dev ffmpeg

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

### Upgrade pip to prevent errors
RUN pip install setuptools --upgrade
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /stories
WORKDIR /stories
ADD . /stories

EXPOSE 7007