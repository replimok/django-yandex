FROM python:3.8-alpine as backend
ENV PYTHONUNBUFFERED 1
ENV DEBUG 'True'
WORKDIR /code

RUN apk --no-cache add bash

RUN apk add --no-cache openssl
ENV DOCKERIZE_VERSION v0.6.1
RUN wget "https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz" \
    && tar -C /usr/local/bin -xzvf "dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz" \
    && rm "dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz"

COPY requirements.txt .
RUN apk --no-cache add \
        --virtual .requirements-build-deps \
        jpeg \
        libffi \
        gcc \
        g++ \
        jpeg-dev \
        libffi-dev \
        musl-dev \
        postgresql-dev \
        postgresql-libs \
        zlib-dev \
        && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .requirements-build-deps


COPY entrypoint.sh /entrypoint.sh

COPY backend .
EXPOSE 8000
RUN chmod a+x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]