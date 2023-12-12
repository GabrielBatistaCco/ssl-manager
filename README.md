## Backend
## Instalação e execução

```
apt install python3 -y
pip3 install django djangorestframework pandas pyOpenSSL django-cors-headers python-dotenv

```

```
mkdir -p /var/www/ssl/
git clone https://github.com/GabrielBatistaCco/ssl.git /var/www/ssl/
cd /var/www/ssl/django/

# Criar o banco de dados
python3 manage.py makemigrations app_ssl
python3 manage.py migrate
```

### Configure as variaveis de ambiente
```
nano .env
```
_Nela você deve declarar a variavel SERVER_IP com o ip da sua maquina_

# Executar em desenvolvimento
```
python3 manage.py runserver
```

# Executar em produção

```
echo "[Unit]
Description='SSL Manager'
After=network.target

[Service]
WorkingDirectory=/var/www/ssl/
ExecStart=/usr/bin/python3 django/manage.py runserver 0.0.0.0:8000

# Restart=always

# StandardOutput=file:/var/log/ssl/django.log
# StandardError=file:/var/log/ssl/django-error.log
StandardOutput=journal
StandardError=journal

SyslogIdentifier=ssl-manager

[Install]
WantedBy=default.target">/etc/systemd/system/ssl-django.service;
```

```
systemctl daemon-reload;
systemctl start ssl-django.service;
```

# Frontend 
_Todos os comandos devem ser executados a partir da pasta ./front_
## Executar em desenvolvimento
```
npm install
npm run dev
```

## Executar em produção

```
cd /var/www/ssl/front
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
source ~/.bashrc
nvm install node
apt install npm
npm install
npm install -g nuxt
nuxt generate
cd dist
```

### Configure as variaveis de ambiente
```
nano .env
```
_Nela você deve declarar a variavel VITE_API_URL com a url da api ex.: http://localhost:8000_



### Instalar o NGinx

```
apt-get install nginx
rm -rf /etc/nginx/sites-enabled/default 
nano /etc/nginx/sites-enabled/default 
```
_Cole esse conteudo no arquivo_

```
server {
    listen 80;
    server_name dominio.com;

    location / {
        root /var/www/ssl/front/dist;
        try_files $uri $uri/ /index.html;
    }
}

service nginx restart
```


# Fluxo de entrega do software

Cada etapa do fluxo é uma ramificação no desenvolvimento do software:

<img src="django/projeto_ssl/images/release-flow.png">

- **Front-end e Back-end**: Ramificações distintas, pois os desenvolvimentos são isolados, permitindo serem execudados em paralelo com segurança de que um não afatará no outro.

- **Teste**: Versão unificada do front-end com o back-end, onde podemos testar sua integração e as funcionlidades programadas.

- **Produção**: A versão disponibilizada para os usuários utilizarem.