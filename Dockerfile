FROM matthewfeickert/docker-python3-ubuntu:latest
RUN mkdir source
COPY source/ /source
WORKDIR /source
RUN pip3 install -r requirements.txt
CMD ["python3", "app.py"]

