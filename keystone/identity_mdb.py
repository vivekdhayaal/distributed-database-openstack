import json
from magnetodbclient.v1 import client
#import pdb; pdb.set_trace()
#mdb = client.Client(username='admin',
#                    password='123',
#                    tenant_name='admin',
#                    auth_url= 'http://127.0.0.1:5000/v2.0/')
mdb = client.Client(endpoint_url='http://127.0.0.1:8480/v1/data/default_tenant',
                    auth_strategy='noauth')
tables = mdb.list_tables()

req = {}

def load_json(file):
    global req
    f = open(file)
    req[file.split('.')[0]] = json.loads(f.read())

def pp(obj):
    print json.dumps(obj, indent=2)
