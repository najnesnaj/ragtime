version: '3'

services:

  nginx:

    image: nginx:latest

    container_name: nginx_proxy

    ports:

      - "9443:9443"

    volumes:

      - ./nginx.conf:/etc/nginx/nginx.conf

      - /etc/letsencrypt:/etc/letsencrypt  # Mount certs

    networks:

      - proxy



  certbot:

    image: certbot/certbot

    container_name: certbot

    command: certonly --webroot --webroot-path=/var/www/certbot -d www.melborp.solutions

    volumes:

      - /etc/letsencrypt:/etc/letsencrypt  # Persist certs

      - /var/www/certbot:/var/www/certbot

    networks:

      - proxy



  app:

    image: your_app_image

    container_name: your_app

    expose:

      - "8080"  # Internal port

    networks:

      - proxy



networks:

  proxy:

    external: true


