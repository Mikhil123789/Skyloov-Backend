python manage.py makemigrations
python manage.py migrate 
celery -A Skyloov beat -l info
celery -A Skyloov worker --loglevel=info
python manage.py runserver 8800
