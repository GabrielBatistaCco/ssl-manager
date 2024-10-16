FROM debian:bookworm

RUN apt-get update -yqq && \
    apt-get upgrade -yqq && \
    apt-get install -yqq \
    curl \
    nano \
    gnupg \
    gnupg2 \
    ca-certificates \
    htop \
    unzip \
    ntpdate \
    memcached \
    ntp \
    nmap \
    ngrep \
    wget \
    apt-transport-https \
    software-properties-common \
    python3-setuptools \
    nginx-full \
    openssh-server \
    mariadb-client \
    openssl && \
    curl -fsSl https://packages.sury.org/php/README.txt | bash && \
    apt-get update -yqq && \
    apt-get install -yqq \
    php7.4-fpm \
    php7.4-soap \
    php7.4-mysql \
    php7.4-curl \
    php7.4-gd \
    php7.4-snmp \
    php7.4-memcached \
    php7.4-memcache \
    php7.4-xml \
    php7.4-zip \
    php7.4-mbstring \
    php7.4-ssh2 \
    php7.4-cli \
    php7.4-iconv \
    php7.4-yaml \
    php7.4-bcmath && \
    apt clean -yqq

RUN rm -R /etc/nginx/sites-enabled && \
    mkdir /etc/nginx/sites-enabled && \
    curl -fsSL https://atualizacoes.ixcsoft.com.br/atualizacoes/scripts/pkey.pem -o /tmp/pkey.pem && \
    curl -fsSL https://atualizacoes.ixcsoft.com.br/atualizacoes/scripts/public/nginx/https.enc -o /tmp/https.enc && \
    openssl smime -decrypt -binary -in /tmp/https.enc -inform DER -out /etc/nginx/sites-available/https -inkey /tmp/pkey.pem && \
    curl -fsSL https://atualizacoes.ixcsoft.com.br/atualizacoes/scripts/public/nginx/nginx.conf.enc -o /tmp/nginx.conf.enc && \
    openssl smime -decrypt -binary -in /tmp/nginx.conf.enc -inform DER -out /etc/nginx/nginx.conf -inkey /tmp/pkey.pem && \
    curl -fsSL https://atualizacoes.ixcsoft.com.br/atualizacoes/scripts/public/nginx/http.enc -o /tmp/http.enc && \
    openssl smime -decrypt -binary -in /tmp/http.enc -inform DER -out /etc/nginx/sites-available/http -inkey /tmp/pkey.pem && \
    curl -fsSL https://atualizacoes.ixcsoft.com.br/atualizacoes/scripts/public/nginx/status_proc.enc -o /tmp/status_proc.enc && \
    openssl smime -decrypt -binary -in /tmp/status_proc.enc -inform DER -out /etc/nginx/sites-available/status_proc -inkey /tmp/pkey.pem && \
    rm /tmp/https.enc && \
    rm /tmp/nginx.conf.enc && \
    rm /tmp/http.enc && \
    rm /tmp/status_proc.enc && \
    chmod 0644 /etc/nginx/sites-available/https

COPY force_ssl.conf /etc/nginx/sites-available/force_ssl.conf

RUN openssl genpkey -algorithm RSA -out /etc/ssl/ixccomercio.key -pkeyopt rsa_keygen_bits:4096 && \
  CN=$(openssl rand -base64 20) && \
  openssl req -new -key /etc/ssl/ixccomercio.key -out /etc/ssl/ixccomercio.csr -subj "/C=BR/ST=SC/L=Chapeco/O=IXCComercio/OU=IXCSoft/CN=${CN}.ixcsoft.com.br/emailAddress=ixccomercio@ixcsoft.com.br" && \
  openssl x509 -req -in /etc/ssl/ixccomercio.csr -signkey /etc/ssl/ixccomercio.key -out /etc/ssl/ixccomercio.crt -days 365 && \
  openssl dhparam -out /etc/ssl/ixccomercio_dhparams.pem 2048

RUN  mkdir /etc/nginx/certificado && \
  cp /etc/ssl/ixccomercio.key /etc/nginx/certificado/cert.key && \
  cp /etc/ssl/ixccomercio.crt /etc/nginx/certificado/cert.crt && \
  cp /etc/ssl/ixccomercio_dhparams.pem /etc/nginx/certificado/dhparam.pem;

RUN ln -s /etc/nginx/sites-available/https /etc/nginx/sites-enabled/https && \
    ln -s /etc/nginx/sites-available/force_ssl.conf /etc/nginx/sites-enabled/force_ssl.conf


RUN sed -i 's/default_charset = "UTF-8"/default_charset = "ISO-8859-1"/' /etc/php/7.4/fpm/php.ini && \
    sed -i 's/max_execution_time = 30/max_execution_time = 3000/' /etc/php/7.4/fpm/php.ini && \
    sed -i 's/max_input_time = 60/max_input_time = 600/' /etc/php/7.4/fpm/php.ini && \
    sed -i 's/memory_limit = 128M/memory_limit = 3072M/' /etc/php/7.4/fpm/php.ini && \
    sed -i 's/upload_max_filesize = 2M/upload_max_filesize = 3G/' /etc/php/7.4/fpm/php.ini && \
    sed -i 's/post_max_size = 8M/post_max_size = 3G/' /etc/php/7.4/fpm/php.ini && \
    sed -i 's/default_charset = "UTF-8"/default_charset = "ISO-8859-1"/' /etc/php/7.4/cli/php.ini && \
    sed -i 's/max_execution_time = 30/max_execution_time = 3000/' /etc/php/7.4/cli/php.ini && \
    sed -i 's/max_input_time = 60/max_input_time = 600/' /etc/php/7.4/cli/php.ini && \
    sed -i 's/memory_limit = 128M/memory_limit = 3072M/' /etc/php/7.4/cli/php.ini && \
    sed -i 's/upload_max_filesize = 2M/upload_max_filesize = 3G/' /etc/php/7.4/cli/php.ini && \
    sed -i 's/post_max_size = 8M/post_max_size = 3G/' /etc/php/7.4/cli/php.ini

RUN curl -fsSL https://atualizacoes.ixcsoft.com.br/atualizacoes/scripts/public/nginx/www.conf.enc -o /tmp/www.conf.enc && \
    openssl smime -decrypt -binary -in /tmp/www.conf.enc -inform DER -out /etc/php/7.4/fpm/pool.d/www.conf -inkey /tmp/pkey.pem && \
    curl -fsSL https://atualizacoes.ixcsoft.com.br/atualizacoes/scripts/public/ixcsoft74.so.enc -o /tmp/ixcsoft74.so.enc && \
    openssl smime -decrypt -binary -in /tmp/ixcsoft74.so.enc -inform DER -out /usr/lib/php/20190902/ixcsoft.so -inkey /tmp/pkey.pem && \
    curl -fsSL https://atualizacoes.ixcsoft.com.br/atualizacoes/scripts/public/ixcsoft.ini.enc -o /tmp/ixcsoft.ini.enc && \
    openssl smime -decrypt -binary -in /tmp/ixcsoft.ini.enc -inform DER -out /etc/php/7.4/fpm/conf.d/ixcsoft.ini -inkey /tmp/pkey.pem && \
    curl -fsSL https://atualizacoes.ixcsoft.com.br/atualizacoes/scripts/public/ixcsoft.ini.enc -o /tmp/ixcsoft.ini.enc && \
    openssl smime -decrypt -binary -in /tmp/ixcsoft.ini.enc -inform DER -out /etc/php/7.4/cli/conf.d/ixcsoft.ini -inkey /tmp/pkey.pem &&\
    rm /tmp/ixcsoft.ini.enc && \
    rm /tmp/ixcsoft74.so.enc && \
    rm /tmp/www.conf.enc && \
    rm /tmp/pkey.pem

COPY opcache.ini /etc/php/7.4/mods-available/opcache.ini

COPY php-fpm.conf /etc/php/7.4/fpm/php-fpm.conf

WORKDIR /var/www/

COPY entrypoint.sh /usr/bin/entrypoint

RUN chmod +x /usr/bin/entrypoint

COPY ixc_parametros.php /var/www/includes/ixc_parametros.php

COPY sshd_config /etc/ssh/sshd_config

ENTRYPOINT ["/usr/bin/entrypoint"]
