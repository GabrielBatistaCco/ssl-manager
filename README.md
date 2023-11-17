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

# Modelo de desenvolvimento

Branchs

<img src="/assets/img/branchs.gif">
