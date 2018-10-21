FROM node:8

RUN mkdir -p /mnt/app
COPY . /mnt/app
WORKDIR /mnt/app

RUN npm i @angular/cli -g

EXPOSE 4200