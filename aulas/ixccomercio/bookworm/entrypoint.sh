#!/bin/bash

curl -fsSL https://atualizacoes.ixcsoft.com.br/atualizacoes/5_3/BKP_estrutura.zip -o BKP_estrutura.zip && \
unzip BKP_estrutura.zip -d /var/www/ && \
rm BKP_estrutura.zip && \
chown www-data:www-data /var/www/ -R && \
rm install.php

ARQUIVO="/var/www/includes/ixc_parametros.php"
USER_DB="${USER_DB}"
HOST_DB="${HOST_DB}"
PASS_DB="${PASS_DB}"

PASSWORD=$(< /dev/urandom tr -dc 'A-Za-z0-9' | head -c 20)

echo "root:$PASSWORD" | chpasswd

sed -i "s/define(\"SERVIDOR\",\"host_db\");/define(\"SERVIDOR\",\"$HOST_DB\");/" "$ARQUIVO"
sed -i "s/define(\"USUARIO\",\"user_db\");/define(\"USUARIO\",\"$USER_DB\");/" "$ARQUIVO"
sed -i "s/define(\"SENHA\",\"pass_db\");/define(\"SENHA\",\"$PASS_DB\");/" "$ARQUIVO"
sed -i "s/define(\"SENHA_ROOT\",\"pass_root\");/define(\"SENHA_ROOT\",\"$PASSWORD\");/" "$ARQUIVO"

# Iniciar o Memcached
service memcached start

# Iniciar o PHP-FPM
service php7.4-fpm start

# Iniciar o sshd-server
service ssh start

# Iniciar o Nginx
nginx -g "daemon off;"
