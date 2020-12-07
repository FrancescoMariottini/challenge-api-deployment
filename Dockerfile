FROM ubuntu:latest
RUN apt-get update -y \
	&& apt-get install -y python3-pip \
	&& rm -rf /var/lib/apt/lists/*
RUN mkdir source
COPY source /source
WORKDIR /source
RUN pip3 install -r requirements.txt
WORKDIR /
CMD export PYTHONPATH="${PYTHONPATH}:/" ; python3 source/app.py

