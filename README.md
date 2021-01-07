# Python Test Assignment

## Порядок запуска Django-приложения
```
Установка виртуального окружения
python3 -m venv myenv && source myenv/bin/activate

создание requirements.txt
pip freeze > requirements.txt

выполнение миграций и запись их в БД
python3 manage.py migrate

запуск механизма миграций 
python3 manage.py makemigrations

создание админа
python manage.py createsuperuser

запустить приложение
python3 manage.py runserver
```