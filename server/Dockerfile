FROM ubuntu:17.04

ENV DB_DIR=/var/db
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV FLASK_APP=/src/app/__init__.py
ENV FLASK_DEBUG=1

EXPOSE 80
WORKDIR /src
RUN apt-get update && apt-get -y upgrade
RUN apt-get install python3-pip -y

ADD server /src
RUN pip3 install -r /src/requirements.txt

CMD ["python3", "/src/run.py"]
