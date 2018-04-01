FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /app

ADD docker/local/start.sh /start.sh
RUN chmod +x /start.sh

ADD docker/local/start_celeryworker.sh /start_celeryworker.sh
RUN chmod +x /start_celeryworker.sh

WORKDIR /app

RUN pip install pipenv -q
RUN pipenv install --dev

ENTRYPOINT ["docker/entrypoint.sh"]

