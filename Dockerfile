FROM ubuntu:latest
FROM python:3.8.5

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
RUN mkdir source
COPY requirements.txt .
COPY /source /source
COPY runetime.txt /source
WORKDIR /source
RUN pip install -r requirements.txt
# ENTRYPOINT ["python3"]
WORKDIR /
CMD export PYTHONPATH="${PYTHONPATH}:/" ;python3 source/app.py
# RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
#     locale-gen
# ENV LANG en_US.UTF-8  
# ENV LANGUAGE en_US:en  
# ENV LC_ALL en_US.UTF-8