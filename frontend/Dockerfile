FROM node:18-alpine

WORKDIR /frontend
COPY package.json yarn.lock* /frontend/

COPY . /frontend

RUN yarn build

EXPOSE 5173
CMD ["yarn", "dev"]
