FROM python:3.7.1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV PYTHONPATH=/usr/src/app/

COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

COPY datadog datadog
COPY tests tests

EXPOSE 8080

