FROM node:8

RUN mkdir -p /mnt/app
ADD . /mnt/app
WORKDIR /mnt/app

RUN npm i @angular/cli -g
RUN cd /mnt/app && npm install

EXPOSE 4200