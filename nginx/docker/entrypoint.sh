#!/bin/bash
if [ -z "$DOMAIN_NAME" ]; then
  echo "Error: DOMAIN_NAME environment variable is not set."
  exit 1
fi
envsubst '${DOMAIN_NAME}' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/nginx.conf
echo "Checking for SSL certificates for $DOMAIN_NAME..."

while [ ! -f "/etc/letsencrypt/live/$DOMAIN_NAME/fullchain.pem" ]; do
  echo "Waiting for SSL certificates to be generated for $DOMAIN_NAME..."
  sleep 5
done

echo "SSL certificates for $DOMAIN_NAME found. Starting NGINX..."
exec nginx -g "daemon off;"