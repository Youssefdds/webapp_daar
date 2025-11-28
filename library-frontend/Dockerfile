FROM node:20-alpine

WORKDIR /app

RUN apk add --no-cache curl bash

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

# Disable host check
ENV DANGEROUSLY_DISABLE_HOST_CHECK=true
ENV HOST=0.0.0.0

CMD ["npm", "start"]
