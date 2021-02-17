http --json POST http://django-points-api.herokuapp.com/api/create/ user="Joe Schmoe" payer="DANNON" points=300
http --json POST http://django-points-api.herokuapp.com/api/create/ user="Joe Schmoe" payer="UNILEVER" points=200
http --json POST http://django-points-api.herokuapp.com/api/deduct/ user="Joe Schmoe" points="-200"
http --json POST http://django-points-api.herokuapp.com/api/create/ user="Joe Schmoe" payer="MILLER COORS" points=10000
http --json POST http://django-points-api.herokuapp.com/api/create/ user="Joe Schmoe" payer="DANNON" points=1000
http --json POST http://django-points-api.herokuapp.com/api/deduct/ user="Joe Schmoe" points="-5000"

http --json POST http://django-points-api.herokuapp.com/api/create/ user="Jane Schmoe" payer="DANNON" points=600
http --json POST http://django-points-api.herokuapp.com/api/create/ user="Jane Schmoe" payer="DANNON" points=600
http --json POST http://django-points-api.herokuapp.com/api/deduct/ user="Jane Schmoe" points="-1200"
http --json POST http://django-points-api.herokuapp.com/api/create/ user="Jane Schmoe" payer="MILLER COORS" points=800
http --json POST http://django-points-api.herokuapp.com/api/create/ user="Jane Schmoe" payer="DANNON" points=500
http --json POST http://django-points-api.herokuapp.com/api/create/ user="Jane Schmoe" payer="MILLER COORS" points=400
http --json POST http://django-points-api.herokuapp.com/api/create/ user="Jane Schmoe" payer="UNILEVER" points=800
http --json POST http://django-points-api.herokuapp.com/api/deduct/ user="Jane Schmoe" points="-2500"