FROM node:18-alpine

WORKDIR /frontend
COPY package.json yarn.lock* /frontend/

RUN yarn --no-progress && rm -rf /tmp/*

COPY . /frontend

RUN yarn build

EXPOSE 3000 6006
CMD ["yarn", "start:prod"]
