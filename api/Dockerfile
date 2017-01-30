FROM python:3.6

RUN apt-get -y update && apt-get -y install python-dev build-essential && apt-get -y clean

COPY requirements.txt /opt/app
RUN pip install -r requirements.txt

COPY . /opt/app
WORKDIR /opt/app

ENV PYTHONPATH /opt/app

EXPOSE 5000
CMD python -m server
