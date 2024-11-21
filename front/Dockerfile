FROM nginx:alpine

ENV TZ=America/Sao_Paulo

WORKDIR /app/nuxt/

COPY . /app/nuxt/temp/
COPY ./server/default.conf /etc/nginx/conf.d/default.conf
COPY ./server/ixc_cert.* /etc/ssl/certs/
COPY ./server/start.sh /usr/bin/start

RUN apk add nodejs npm && \
    cd temp/ && \
    npm install && \
    npm install -g nuxt && \
    cd /app/nuxt/temp/ && \
    chmod +x /usr/bin/start && \
    ln -s /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime

EXPOSE 443

CMD [ "start" ]