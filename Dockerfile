# Image having basic core os requirements

FROM python:3.7.9-stretch

# Django app
ADD . /app/

ARG DJANGO_SETTINGS_MODULE=restaurant_rater.settings

WORKDIR /app/

RUN apt-get update \
    && apt-get install vim less python3-dev -y \
    && apt-get install libpq-dev -y \
    && pip --disable-pip-version-check install --cache-dir=/.pip -r requirements.txt \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /libs/ \
    && rm -rf /.pip

CMD [ "gunicorn", "-c", "/app/restaurant_rater/gunicorn.conf.py", "restaurant_rater.wsgi:application"]
