::Used to reset the database to an empty state
heroku pg:reset DATABASE_URL --confirm django-transaction-api
heroku run python manage.py migrate api
heroku run rake db:migrate