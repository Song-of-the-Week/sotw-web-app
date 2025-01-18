FROM nginx

RUN apt update
RUN apt install -y certbot python3-certbot-dns-route53

COPY ./nginx.conf.template /etc/nginx/templates/nginx.conf.template
COPY ./docker/docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]