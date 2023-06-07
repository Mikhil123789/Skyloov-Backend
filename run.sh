python manage.py makemigrations
python manage.py migrate 

#celery -A Skyloov worker --loglevel=info
#celery -A Skyloov beat -l info

python manage.py runserver 8800
