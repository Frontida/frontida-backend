python manage.py migrate
web: gunicorn frontida_backend.wsgi:application --preload --workers 1
python manage.py collectstatic --noinput
release: python manage.py makemigrations
release: python manage.py migrate