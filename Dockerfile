FROM python:3.7-alpine
MAINTAINER Vivek Shinde

# PYTHONUNBUFFERED = 1 is recommonded when running python in containere
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps 

RUN mkdir -p /app
WORKDIR /app
COPY ./app /app

# -D Application process only user 
RUN adduser -D user 
USER user

