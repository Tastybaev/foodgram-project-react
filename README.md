# Foodgram
Cервис для публикаций и обмена рецептами.

Авторизованные пользователи могут подписываться на понравившихся авторов, добавлять рецепты в избранное, в покупки, скачивать список покупок. Неавторизованным пользователям доступна регистрация, авторизация, просмотр рецептов других пользователей.


## Установка на сервер

#### Установка Docker
Для запуска проекта вам потребуется установить следующие программы:
```
sudo apt update
sudo apt upgrade -y
sudo apt install python3-pip python3-venv git -y
sudo apt install curl
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh 
sudo apt install docker-compose
```

### Установка проекта на сервер
1. Клонировать репозиторий и перейти в папку /infra/:
```
 git clone git@github.com:Tastybaev/foodgram-project-react.git
 cd infra/
```

2. Создайте файл .env командой touch .env и добавьте в него переменные окружения для работы с базой данных:
```
SECRET_KEY=любой_секретный_ключ_на_ваш_выбор
DEBUG=False
ALLOWED_HOSTS=*,или,ваши,хосты,через,запятые,без,пробелов
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=пароль_к_базе_данных_на_ваш_выбор
DB_HOST=db  # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД

```

### Настройка проекта
1. Запустите docker compose:
```bash
docker-compose up -d
```
2. Примените миграции:
```bash
sudo docker exec -it <name или id контейнера backend> python manage.py migrate
```
3. Заполните базу начальными данными:
```bash
sudo docker exec -it <name или id контейнера backend> python manage.py loaddata data/ingredients.json
```
4. Создайте администратора:
```bash
sudo docker exec -it <name или id контейнера backend> python manage.py createsuperuser
```
5. Соберите статику:
```bash
sudo docker exec -it <name или id контейнера backend> python manage.py collectstatic
```

## Сайт
Сайт доступен по ссылке: http://51.250.2.129/

Админка доступна по адресу: http://51.250.2.129/admin/

Вход в панель администратора: email: Tastybaev@mail.ru
                              password: Admin123456

Пользователи: 

login: User@mail.ru password: User123

login: Lory@mail.ru password: Lory123456

login: Cage@mail.ru password: Cage123456
