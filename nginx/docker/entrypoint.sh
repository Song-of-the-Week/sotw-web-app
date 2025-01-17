#!/usr/bin/env sh
set -eu

envsubst '${DOMAIN_NAME}' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/conf.d/default.conf

exec "$@"