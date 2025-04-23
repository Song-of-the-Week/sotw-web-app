FROM public.ecr.aws/docker/library/node:18.19.1-buster-slim AS build-stage

ARG VITE_HOSTNAME
ARG VITE_API_HOSTNAME
ARG VITE_SPOTIFY_CALLBACK_URI

ENV VITE_HOSTNAME=$VITE_HOSTNAME
ENV VITE_API_HOSTNAME=$VITE_API_HOSTNAME
ENV VITE_SPOTIFY_CALLBACK_URI=$VITE_SPOTIFY_CALLBACK_URI

WORKDIR /usr/src/frontend

COPY . .

RUN apt update
RUN apt install -y curl

RUN npm install
RUN npx update-browserslist-db@latest
RUN npm run build-prod

FROM busybox:1.37
RUN adduser -D static
USER static
WORKDIR /home/static
COPY --from=build-stage /usr/src/frontend/dist .
CMD ["busybox", "httpd", "-f", "-v", "-p", "8080"]