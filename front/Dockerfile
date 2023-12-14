# ssl-nginx
FROM nginx:stable-alpine

COPY .output/public/ /var/www/
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

WORKDIR /var/www/

EXPOSE 80
