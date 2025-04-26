FROM public.ecr.aws/docker/library/node:18.19.1-buster-slim AS build-stage

ARG VITE_HOSTNAME
ARG VITE_API_HOSTNAME
ARG VITE_SPOTIFY_CALLBACK_URI

ENV VITE_HOSTNAME=$VITE_HOSTNAME
ENV VITE_API_HOSTNAME=$VITE_API_HOSTNAME
ENV VITE_SPOTIFY_CALLBACK_URI=$VITE_SPOTIFY_CALLBACK_URI

WORKDIR /usr/src/frontend

COPY . .

RUN npm ci
RUN npx update-browserslist-db@latest
RUN npm run build-prod

FROM public.ecr.aws/nginx/nginx:1.27-alpine3.21-slim AS serve-stage

RUN apk add --no-cache curl
# Remove the default nginx.conf and add a custom one
COPY nginx.conf /etc/nginx/nginx.conf

# Copy static files from the build stage
COPY --from=build-stage /usr/src/frontend/dist /usr/share/nginx/html

EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
