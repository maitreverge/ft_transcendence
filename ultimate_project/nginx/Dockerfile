FROM nginx:latest

ARG env=prod

COPY envv/local.crt /etc/nginx/ssl/local.crt
COPY envv/local.key /etc/nginx/ssl/local.key 
COPY config.${env}.conf /etc/nginx/conf.d/default.conf
