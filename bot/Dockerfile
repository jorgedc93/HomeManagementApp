FROM python:3.6

RUN apt-get -y update && apt-get -y install python-dev build-essential && apt-get -y clean

COPY . /opt/app

WORKDIR /opt/app

RUN pip install -r requirements.txt

ENV PYTHONPATH /opt/app

CMD python -m flat.main