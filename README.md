# Instalação e execução

```
apt install python3 -y
pip3 install django djangorestframework pandas pyOpenSSL
```

```
mkdir -p /var/www/ssl/
git clone https://github.com/GabrielBatistaCco/ssl.git /var/www/ssl/
cd /var/www/ssl/python

# Criar o banco de dados
python3 manage.py makemigrations app_ssl
python3 manage.py migrate

# Executar server
python3 manage.py runserver
```

# Fluxo de entrega do software

Cada etapa do fluxo é uma ramificação no desenvolvimento do software:

<img src="python/projeto_ssl/Fluxo-entrega.png">

- **Front-end e Back-end**: Ramificações distintas, pois os desenvolvimentos são isolados, permitindo serem execudados em paralelo com segurança de que um não afatará no outro.

- **Teste**: Versão unificada do front-end com o back-end, onde podemos testar sua integração e as funcionlidades programadas.

- **Produção**: A versão disponibilizada para os usuários utilizarem.