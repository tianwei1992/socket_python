import requests

r = requests.get('http://127.0.0.1:8000/')
if r and r.status_code == 200:
    print(r.text)
else:
    print(r.status_code)
