FROM ubuntu:latest
RUN apt-get update -y \
	&& apt-get install -y python3-pip \
	&& rm -rf /var/lib/apt/lists/*
RUN mkdir src
COPY src /src
WORKDIR /src
RUN pip3 install -r requirements.txt

# When prefixing src to py imports and running python in root /
#WORKDIR /
#CMD export PYTHONPATH="${PYTHONPATH}:/" ; python3 source/app.py

# When not prefixing src in py imports and running python in root / 
WORKDIR /
CMD python3 src/app.py


