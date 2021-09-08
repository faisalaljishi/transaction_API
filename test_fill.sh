#Requires httpie to run
http --json POST https://django-transaction-api.herokuapp.com/api/create/ user="Joe Schmoe" payer="DANNON" points="300"  --ignore-stdin --check-status --timeout 15
http --json POST https://django-transaction-api.herokuapp.com/api/create/ user="Joe Schmoe" payer="UNILEVER" points="200"  --ignore-stdin --check-status --timeout 15
http --json POST https://django-transaction-api.herokuapp.com/api/deduct/ user="Joe Schmoe" points="-200" --ignore-stdin --check-status --timeout 15
http --json POST https://django-transaction-api.herokuapp.com/api/create/ user="Joe Schmoe" payer="MILLER COORS" points="10000" --ignore-stdin --check-status --timeout 15
http --json POST https://django-transaction-api.herokuapp.com/api/create/ user="Joe Schmoe" payer="DANNON" points="1000" --ignore-stdin --check-status --timeout 15
http --json POST https://django-transaction-api.herokuapp.com/api/deduct/ user="Joe Schmoe" points="-5000" --ignore-stdin --check-status --timeout 15

http --json POST https://django-transaction-api.herokuapp.com/api/create/ user="Jane Schmoe" payer="DANNON" points="600" --ignore-stdin --check-status --timeout 15
http --json POST https://django-transaction-api.herokuapp.com/api/create/ user="Jane Schmoe" payer="DANNON" points="600" --ignore-stdin --check-status --timeout 15
http --json POST https://django-transaction-api.herokuapp.com/api/deduct/ user="Jane Schmoe" points="-1200" --ignore-stdin --check-status --timeout 15
http --json POST https://django-transaction-api.herokuapp.com/api/create/ user="Jane Schmoe" payer="MILLER COORS" points="800" --ignore-stdin --check-status --timeout 15
http --json POST https://django-transaction-api.herokuapp.com/api/create/ user="Jane Schmoe" payer="DANNON" points="500" --ignore-stdin --check-status --timeout 15
http --json POST https://django-transaction-api.herokuapp.com/api/create/ user="Jane Schmoe" payer="MILLER COORS" points="400" --ignore-stdin --check-status --timeout 15
http --json POST https://django-transaction-api.herokuapp.com/api/create/ user="Jane Schmoe" payer="UNILEVER" points="800" --ignore-stdin --check-status --timeout 15
http --json POST https://django-transaction-api.herokuapp.com/api/deduct/ user="Jane Schmoe" points="-2500" --ignore-stdin --check-status --timeout 15
