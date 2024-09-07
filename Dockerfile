FROM python:alpine3.20

ARG ENVIRONMENT=default


  # Sane defaults for pip
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # Python logs to STDOUT
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt


RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r /tmp/requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY . .

CMD [ "python","app/manage.py","runserver","0.0.0.0:8000" ]
