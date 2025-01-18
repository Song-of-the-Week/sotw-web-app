FROM nginx

COPY ./nginx.conf.template /etc/nginx/templates/nginx.conf.template
COPY ./docker/entrypoint.sh /
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]