release: python manage.py migrate
web: gunicorn config.wsgi --workers 2 --log-file -