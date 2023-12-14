# django-backend
FROM python:3.11.7-alpine3.19

ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

COPY . /app/django/
COPY scripts /scripts

WORKDIR /app/django/

RUN rm Dockerfile scripts -R && \
    pip install --upgrade pip && \
    pip install django djangorestframework pandas pyOpenSSL django-cors-headers python-dotenv djongo==1.3.6 pymongo==3.12.3 && \
    chmod -R +x /scripts

ENV PATH="/scripts:$PATH"

EXPOSE 8000
ENTRYPOINT [ "start.sh" ]
