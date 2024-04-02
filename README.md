# Foodgram
«Фудграм» — сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также будет доступен сервис «Список покупок». Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

# Технологии
- Python 3.9
- Django
- Django REST Framework
- PostgreSQL
- Nginx
- Docker
- Gunicorn
- React

# Локальный запуск бэкенда
Клонировать репозиторий и перейти в папку бэкенда:

```bash
git clone <https or SSH URL>

cd foodgram-project-react/backend
```

Создать .env файл со следующим содержанием:

```
# Django settings
SECRET_KEY=<secret_key>
DEBUG=False
ALLOWED_HOSTS=<host_ip_address>;127.0.0.1;localhost;<domain.name>

# Заменить на False, если будет использоваться Postgres
USE_SQLITE=True

# POSTGRES data
POSTGRES_USER=<user>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<db name>
DB_HOST=<db host>
DB_PORT=<db port>
```

Cоздать виртуальное окружение:

Здесь и далее для **Windows** вместо `python3` нужно писать `python`. Для **Linux** и **macOS** команда остаётся такой же.

```bash
python3 -m venv venv
```

Активировать виртуальное окружение:

для Linux и macOS:
```bash
source venv/bin/activate
```

для Windows:
```bash
source venv/scripts/activate
```

Установить зависимости из файла requirements.txt:

```bash
python3 -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```
Выполнить миграции:

```bash
python3 manage.py migrate
```

Заполнить базу данных контентом можно командами:

```bash
python3 manage.py load_tags

python3 manage.py load_ingredients
```

Запустить проект:

```bash
python3 manage.py runserver
```

Для проверки работоспособности API можно запустить тесты:
```bash
pytest
```

# Локальный запуск через Docker

Клонировать репозиторий:

```bash
git clone <https or SSH URL>
```

Создать в корневой директории .env файл со следующим содержанием:

```
# Django settings
SECRET_KEY=<secret_key>
DEBUG=False
ALLOWED_HOSTS=<host_ip_address>;127.0.0.1;localhost;<domain.name>

USE_SQLITE=False

# POSTGRES data
POSTGRES_USER=<user>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<db name>
DB_HOST=<db host>
DB_PORT=<db port>
```

Запуск:

```bash
sudo docker compose -f docker-compose.develop.yml up
```

После  запуска проект доступен на локальном IP 127.0.0.1:8080.
Сайт предварительно заполнен демонстрационными данными.

# Запуск на сервере
Клонировать репозиторий:

```bash
git clone git@github.com:Chernovasilenko/kittygram_final
```

Перейти в каталог проекта:

```bash
cd foodgram-project-react
```

Создать .env файл со следующим содержанием:

```
# Django settings
SECRET_KEY=<secret_key>
DEBUG=False
ALLOWED_HOSTS=<host_ip_address>;127.0.0.1;localhost;<domain.name>

USE_SQLITE=False

# POSTGRES data
POSTGRES_USER=<user>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<db name>
DB_HOST=<db host>
DB_PORT=<db port>

# Admin
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@admin.com
ADMIN_PASSWORD=admin

# Docker 
DOCKER_USERNAME=<docker_username>
```

Создать docker images образы:

```bash
sudo docker build -t <username>/food_back backend/
sudo docker build -t <username>/food_front  frontend/
sudo docker build -t <username>/food_gateway  gateway/
```

Загрузить образы на Docker Hub:

```bash
sudo docker push <username>/food_back
sudo docker push <username>/food_front
sudo docker push <username>/food_gateway
```

Перенести на сервер файлы .env и docker-compose.production.yml

Выполнить сборку приложений:
```bash
sudo docker compose -f docker-compose.production.yml up -d
```

Настроить конфиг nginx на сервере, чтобы все зпросы на порт `8080` перенаправлялись в докер:

```bash
sudo nano /etc/nginx/sites-enabled/default
```

```
location / {
    proxy_set_header Host $http_host;
    proxy_pass http://127.0.0.1:8080;
}
```

Перезапустить nginx:
```bash
sudo systemctl reload nginx
```

# CI/CD

Для использования CI/CD через GitHub Actions необходимо добавить следующие значения в Actions secrets:
- `DOCKER_USERNAME` | Никнейм в Docker
- `DOCKER_PASSWORD` | Пароль в Docker
- `HOST` | ip-адрес сервера
- `USER` | Имя юзера на сервере
- `SSH_KEY` | SSH_KEY
- `SSH_PASSPHRASE` | SSH пароль
- `TELEGRAM_TO` | id телеграм-аккаунта
- `TELEGRAM_TOKEN` | токен телеграм-бота

При использовании `git push` в ветку `main` будет происходить автоматическое тестирование кода, сборка и загрузка образов, деплой на сервер и отправка сообщения в телеграм при успешном деплое.

# Демонстрационный сайт:

Сайт доступен по адресу: https://fudgram.ddns.net

Данные для доступа:

``` 
login - admin@admin.com
pass - admin
```
