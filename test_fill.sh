https --form POST http://django-points-api.herokuapp.com/api/create/ code="print(123)"
{
        "user": "Joe Schmoe",
        "payer": "DANNON",
        "points": 300
}
https --form POST http://django-points-api.herokuapp.com/api/create/ code="print(123)"
{
        "user": "Joe Schmoe",
        "payer": "UNILEVER",
        "points": 200
}
https --form POST http://django-points-api.herokuapp.com/api/deduct/ code="print(123)"
{
        "user": "Joe Schmoe",
        "points": -200
}
https --form POST http://django-points-api.herokuapp.com/api/create/ code="print(123)"
{
        "user": "Joe Schmoe",
        "payer": "MILLER COORS",
        "points": 10000
}
https --form POST http://django-points-api.herokuapp.com/api/create/ code="print(123)"
{
        "user": "Joe Schmoe",
        "payer": "DANNON",
        "points": 1000

}
https --form POST http://django-points-api.herokuapp.com/api/deduct/ code="print(123)"
{
        "user": "Joe Schmoe",
        "points": -5000
}
,
https --form POST http://django-points-api.herokuapp.com/api/create/ code="print(123)"
{
        "user": "Jane Schmoe",
        "payer": "DANNON",
        "points": 600
}
https --form POST http://django-points-api.herokuapp.com/api/create/ code="print(123)"
{
        "user": "Jane Schmoe",
        "payer": "DANNON",
        "points": 600
}
https --form POST http://django-points-api.herokuapp.com/api/deduct/ code="print(123)"
{
        "user": "Jane Schmoe",
        "points": -1200
}
https --form POST http://django-points-api.herokuapp.com/api/create/ code="print(123)"
{
        "user": "Jane Schmoe",
        "payer": "MILLER COORS",
        "points": 800
}
https --form POST http://django-points-api.herokuapp.com/api/create/ code="print(123)"
{
        "user": "Jane Schmoe",
        "payer": "DANNON",
        "points": 500
}
https --form POST http://django-points-api.herokuapp.com/api/create/ code="print(123)"
{
        "user": "Jane Schmoe",
        "payer": "MILLER COORS",
        "points": 400
}
https --form POST http://django-points-api.herokuapp.com/api/create/ code="print(123)"
{
        "user": "Jane Schmoe",
        "payer": "UNILEVER",
        "points": 800
}
https --form POST http://django-points-api.herokuapp.com/api/deduct/ code="print(123)"
{
        "user": "Jane Schmoe",
        "points": -2500
}
