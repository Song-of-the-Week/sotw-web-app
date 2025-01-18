#!/bin/bash

envsubst '${DOMAIN_NAME}' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/nginx.conf
while [ ! -f /etc/letsencrypt/live/example.com/fullchain.pem ]; do
    echo "Waiting for SSL certificates..."
    sleep 5
done
echo "Certificates available. Starting NGINX..."
exec nginx -g "daemon off;"