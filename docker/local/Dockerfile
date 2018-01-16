FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /app

ADD . /app/
ADD docker/local/start.sh /start.sh
RUN chmod +x /start.sh

WORKDIR /app

RUN pip install pipenv
RUN pipenv install --dev

ENTRYPOINT ["docker/entrypoint.sh"]

