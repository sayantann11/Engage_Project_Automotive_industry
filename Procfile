web: gunicorn Engage_project_carsamjho-main.wsgi
python manage.py collectstatic --noinput
manage.py migrate
web: python manage.py runserver 0.0.0.0:5000
