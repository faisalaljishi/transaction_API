cd points
python manage.py makemigrations
python manage.py migrate
export DJANGO_DEBUG=False
::python manage.py makemessages -l zh
::python manage.py compilemessages
::python manage.py test
:: python manage.py collectstatic