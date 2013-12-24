import requests
from keystoneclient.v2_0 import client
keystone = client.Client(username='admin', password='swordfish',
                         tenant_name='admin',
                         auth_url='http://172.18.124.203:5000/v2.0/')

headers = {'Content-Type': 'application/json',
           'X-Auth-Token': str(keystone.auth_token)}

r = requests.get('http://localhost:8989/', headers=headers)
print r.text
r = requests.get('http://localhost:8989/v1/', headers=headers)
print r.text
r = requests.get('http://localhost:8989/v1/workbooks', headers=headers)
print r.text

