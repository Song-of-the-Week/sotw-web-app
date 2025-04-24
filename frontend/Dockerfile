FROM public.ecr.aws/docker/library/node:18.19.1-buster-slim AS build-stage

ARG VITE_HOSTNAME
ARG VITE_API_HOSTNAME
ARG VITE_SPOTIFY_CALLBACK_URI

ENV VITE_HOSTNAME=$VITE_HOSTNAME
ENV VITE_API_HOSTNAME=$VITE_API_HOSTNAME
ENV VITE_SPOTIFY_CALLBACK_URI=$VITE_SPOTIFY_CALLBACK_URI

WORKDIR /usr/src/frontend

COPY . .

RUN npm install
RUN npx update-browserslist-db@latest
RUN npm run build-prod

FROM public.ecr.aws/docker/library/alpine:3.21 AS serve-stage

# darkhttpd serves the content and curl is used for health checks in AWS
RUN adduser -D static \
    && apk add --no-cache darkhttpd curl

USER static
WORKDIR /home/static
COPY --from=build-stage /usr/src/frontend/dist .

EXPOSE 8080
CMD ["darkhttpd", ".", "--port", "8080", "--no-server-id"]