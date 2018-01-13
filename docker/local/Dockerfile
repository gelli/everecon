FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app

ADD . /app/

RUN pip install pipenv
RUN pipenv install

