FROM public.ecr.aws/docker/library/node:18.19.1-buster-slim

WORKDIR /usr/src/frontend

COPY . .

RUN apt update
RUN apt install -y curl

RUN npm install
RUN npx update-browserslist-db@latest
RUN npm run build-prod