FROM python:3.10.7-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Additional dependencies
  && apt-get install -y telnet netcat \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./docker/start_api.sh /start_api.sh
RUN chmod +x /start_api.sh

COPY ./docker/start_celery_worker.sh /start_celery_worker.sh
RUN chmod +x /start_celery_worker.sh

COPY ./docker/start_celery_beat.sh /start_celery_beat.sh
RUN chmod +x /start_celery_beat.sh

COPY ./docker/start_celery_flower.sh /start_celery_flower.sh
RUN chmod +x /start_celery_flower.sh

COPY ./docker/start_db.sh /start_db.sh
RUN chmod +x /start_db.sh

WORKDIR /app

COPY . .

ENTRYPOINT [ "/entrypoint.sh" ]