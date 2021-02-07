# Django-HW

架設於 GCP，網址 https://hw.maxlist.xyz/

## 1. 使用套件
* django 3.1.5
* django-q 1.3.4
* djangorestframework 3.12.2
* gunicorn 20.0.4
* whitenoise 5.2.0
* black 20.8b1
* flake8 3.8.4

## 2. Prerequisite Setup
建立 `/app/django-prod.env` 
```
$ cd app
$ vim django-prod.env
```
貼上環境變數
```
DJANGO_SECRET_KEY="the secret key never know"
DEBUG_SETTING=False
ALLOWED_HOSTS=*
```
建立 `ssl.key` & `ssl.csr`
```
$ cd ./nginx.conf
$ openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout ssl.key -out ssl.csr
```

## 3. Launch on local runtime
▍方法 1 - Docker
```
$ docker-compose -f docker-compose.yml up --build
```

▍方法 2 - Python Built-in venv

- Create your virtual environment
```
$ cd app
$ python3 -m venv venv
```
- And enable virtual environment
```
$ . venv/bin/activate
```
- Install requirements
```
$ pip install -r requirements.txt 
```
- Run Django
```
$ python3 manager.py runserver
```

▍方法 3 - Poetry
- Install requirements
```
$ cd app
$ poetry install
```
- And enable virtual environment
```
$ poetry shell
```
- Run Django
```
$ python3 manager.py runserver
```

## 3. 單元測試
```
$ cd app
$ python3 manager.py test
```
