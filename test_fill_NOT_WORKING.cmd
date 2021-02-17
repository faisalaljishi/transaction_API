:: THIS DOES NOT WORK
del alias:curl -Force
doskey curl=C:\Program Files\Git\mingw64\bin\curl.exe
curl -i -X POST http://django-points-api.herokuapp.com/api/create/ -H "Content-Type:application/json" -d "{ \"user\":\"Joe Schmoe\",\"payer\":\"DANNON\",\"points\":300}"
curl -i -X POST http://django-points-api.herokuapp.com/api/create/ -H "Content-Type:application/json" -d "{\"user\": \"Joe Schmoe\", \"payer\": \"UNILEVER\", \"points\": 200}" 
curl -i -X POST http://django-points-api.herokuapp.com/api/deduct/ -H "Content-Type:application/json" -d "{\"user\": \"Joe Schmoe\",  \"points\": -200}"
curl -i -X POST http://django-points-api.herokuapp.com/api/create/ -H "Content-Type:application/json" -d "{\"user\": \"Joe Schmoe\", \"payer\": \"MILLER COORS\", \"points\": 10000}" 
curl -i -X POST http://django-points-api.herokuapp.com/api/create/ -H "Content-Type:application/json" -d "{\"user\": \"Joe Schmoe\", \"payer\": \"DANNON\", \"points\": 1000}" 
curl -i -X POST http://django-points-api.herokuapp.com/api/deduct/ -H "Content-Type:application/json" -d "{\"user\": \"Joe Schmoe\",  \"points\": -5000}"

curl -i -X POST http://django-points-api.herokuapp.com/api/create/ -H "Content-Type:application/json" -d "{\"user\": \"Jane Schmoe\", \"payer\": \"DANNON\", \"points\": 600}" 
curl -i -X POST http://django-points-api.herokuapp.com/api/create/ -H "Content-Type:application/json" -d "{\"user\": \"Jane Schmoe\", \"payer\": \"DANNON\", \"points\": 600}" 
curl -i -X POST http://django-points-api.herokuapp.com/api/deduct/ -H "Content-Type:application/json" -d "{\"user\": \"Jane Schmoe\",  \"points\": -1200}"
curl -i -X POST http://django-points-api.herokuapp.com/api/create/ -H "Content-Type:application/json" -d "{\"user\": \"Jane Schmoe\", \"payer\": \"MILLER COORS\", \"points\": 800}" 
curl -i -X POST http://django-points-api.herokuapp.com/api/create/ -H "Content-Type:application/json" -d "{\"user\": \"Jane Schmoe\", \"payer\": \"DANNON\", \"points\": 500}" 
curl -i -X POST http://django-points-api.herokuapp.com/api/create/ -H "Content-Type:application/json" -d "{\"user\": \"Jane Schmoe\", \"payer\": \"MILLER COORS\", \"points\": 400}" 
curl -i -X POST http://django-points-api.herokuapp.com/api/create/ -H "Content-Type:application/json" -d "{\"user\": \"Jane Schmoe\", \"payer\": \"UNILEVER\", \"points\": 800}" 
curl -i -X POST http://django-points-api.herokuapp.com/api/deduct/ -H "Content-Type:application/json" -d "{\"user\": \"Jane Schmoe\",  \"points\": -2500}"
