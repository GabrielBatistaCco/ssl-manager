FROM python:3.11.7-alpine3.19

ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
ENV TZ=America/Sao_Paulo

COPY . /app/django/
COPY ./server/start.sh /usr/bin/start
COPY ./server/ixc_cert.* /etc/ssl/certs/

WORKDIR /app/django/

RUN rm Dockerfile server -R && \
    apk update && \
    apk add --no-cache gcc musl-dev && \
    apk add --no-cache pkgconfig && \
    apk add --no-cache mariadb-dev && \
    pip install --upgrade pip && \
    pip install -r requeriments.txt && \
    chmod -R +x /usr/bin/start && \
    ln -s /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    python manage.py crontab add

EXPOSE 8000
ENTRYPOINT [ "start" ]
