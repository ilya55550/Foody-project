### Описание проекта:
Сайт ресторана с блогом

### Инструменты разработки

**Стек:**
- Python >= 3.9
- Django >= 3
- Django REST Framework >= 3.13.1
- PostgreSQL == 13
- Celery == 5.2.7

## Установка

##### 1) Создать виртуальное окружение

    python -m venv venv
    
##### 2) Активировать виртуальное окружение

##### 3) Установить зависимости

    pip install -r requirements.txt

##### 4) Выполнить команду для создания миграций

    python manage.py makemigrations

##### 5) Выполнить команду для выполнения миграций

    python manage.py migrate

##### 6) Скачать образ redis и запустить контейнер в docker(Также можно установить redis без докера и отконфигурировать на локальной машине)

    sudo docker run -d -p 6379:6379 redis

##### 7) Запустить worker

    celery -A sitefoody worker -l info

##### 8) Запустить beat

    celery -A sitefoody beat -l info

##### 9) Запустить сервер

    python manage.py runserver


## License

[BSD 3-Clause License](https://opensource.org/licenses/BSD-3-Clause)

Copyright (c) 2022-present, ilya55550



