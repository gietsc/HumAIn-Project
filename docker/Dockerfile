FROM ubuntu:latest
FROM python:3.8.5-slim

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
RUN mkdir source
COPY source /source
WORKDIR /source
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
WORKDIR /
CMD export PYTHONPATH="${PYTHONPATH}:/" ; python3 source/app.py