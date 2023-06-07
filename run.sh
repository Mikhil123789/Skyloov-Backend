python manage.py makemigratipons
python manage.py migrate 
celery -A Skyloov beat -l info
celery -A Skyloov worker --loglevel=info
python manage.py runserver
