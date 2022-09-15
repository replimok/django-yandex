#!/bin/bash
set -o nounset -o pipefail -o errexit

if [ "${DB_HOST}" ]; then
    /usr/local/bin/dockerize -timeout 60s -wait tcp://"${DB_HOST}":"${DB_HOST_PORT}"
fi

echo 'running migrations to database'
/usr/local/bin/python3 manage.py migrate

echo 'running collecting static'
/usr/local/bin/python3 manage.py collectstatic --noinput

exec "$@"
