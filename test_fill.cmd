curl -i -X POST -H "Content-Type:application/json" -d "{\"user\": \"Joe Schmoe\", \"payer\": \"DANNON\", \"points\": 300}" http://django-points-api.herokuapp.com/api/create/
curl -i -X POST -H "Content-Type:application/json" -d "{\"user\": \"Joe Schmoe\", \"payer\": \"UNILEVER\", \"points\": 200}" http://django-points-api.herokuapp.com/api/create/
curl -i -X POST -H "Content-Type:application/json" -d "{\"user\": \"Joe Schmoe\",  \"points\": -200}" http://django-points-api.herokuapp.com/api/deduct/
curl -i -X POST -H "Content-Type:application/json" -d "{\"user\": \"Joe Schmoe\", \"payer\": \"MILLER COORS\", \"points\": 10000}" http://django-points-api.herokuapp.com/api/create/
curl -i -X POST -H "Content-Type:application/json" -d "{\"user\": \"Joe Schmoe\", \"payer\": \"DANNON\", \"points\": 1000}" http://django-points-api.herokuapp.com/api/create/
curl -i -X POST -H "Content-Type:application/json" -d "{\"user\": \"Joe Schmoe\",  \"points\": -5000}" http://django-points-api.herokuapp.com/api/deduct/

curl -i -X POST -H "Content-Type:application/json" -d "{\"user\": \"Jane Schmoe\", \"payer\": \"DANNON\", \"points\": 600}" http://django-points-api.herokuapp.com/api/create/
curl -i -X POST -H "Content-Type:application/json" -d "{\"user\": \"Jane Schmoe\", \"payer\": \"DANNON\", \"points\": 600}" http://django-points-api.herokuapp.com/api/create/
curl -i -X POST -H "Content-Type:application/json" -d "{\"user\": \"Jane Schmoe\",  \"points\": -1200}" http://django-points-api.herokuapp.com/api/deduct/
curl -i -X POST -H "Content-Type:application/json" -d "{\"user\": \"Jane Schmoe\", \"payer\": \"MILLER COORS\", \"points\": 800}" http://django-points-api.herokuapp.com/api/create/
curl -i -X POST -H "Content-Type:application/json" -d "{\"user\": \"Jane Schmoe\", \"payer\": \"DANNON\", \"points\": 500}" http://django-points-api.herokuapp.com/api/create/
curl -i -X POST -H "Content-Type:application/json" -d "{\"user\": \"Jane Schmoe\", \"payer\": \"MILLER COORS\", \"points\": 400}" http://django-points-api.herokuapp.com/api/create/
curl -i -X POST -H "Content-Type:application/json" -d "{\"user\": \"Jane Schmoe\", \"payer\": \"UNILEVER\", \"points\": 800}" http://django-points-api.herokuapp.com/api/create/
curl -i -X POST -H "Content-Type:application/json" -d "{\"user\": \"Jane Schmoe\",  \"points\": -2500}" http://django-points-api.herokuapp.com/api/deduct/

