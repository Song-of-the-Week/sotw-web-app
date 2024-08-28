FROM node:18.19.1-buster-slim

WORKDIR /usr/src/frontend

COPY . .

RUN npm install
RUN npx update-browserslist-db@latest
RUN npm run build-prod