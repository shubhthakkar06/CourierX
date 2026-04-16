import requests
import json

s = requests.Session()
r = s.post('http://localhost:5000/api/admin/login', json={'userid': 'admin', 'password': 'admin'})
print("Login status:", r.status_code)

r2 = s.get('http://localhost:5000/api/admin/orders')
print("Orders status:", r2.status_code)
if r2.status_code == 200:
    print(r2.text)
else:
    print(r2.text)
