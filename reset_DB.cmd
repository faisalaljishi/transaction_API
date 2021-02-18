::Used to reset the database to an empty state
heroku pg:reset DATABASE_URL
heroku run rake db:migrate