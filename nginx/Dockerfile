FROM public.ecr.aws/nginx/nginx:stable-perl

COPY ./nginx.conf.template /etc/nginx/templates/nginx.conf.template
COPY ./docker/entrypoint.sh /
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]