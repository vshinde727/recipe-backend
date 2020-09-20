FROM python:3.7-alpine
MAINTAINER Vivek Shinde

# PYTHONUNBUFFERED = 1 is recommonded when running python in containere
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir -p /app
WORKDIR /app
COPY ./app /app

# -D Application process only user 
RUN adduser -D user 
USER user

