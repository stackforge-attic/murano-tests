from keystoneclient.v2_0 import client as ksclient
from neutronclient.neutron import client as netclient
from muranoclient.v1.client import Client as murano_client
import novaclient.v1_1.client as nvclient
import time
user = 'sergey_demo_user'
password = '111'
tenant = 'ForTests'
keystone_url = 'http://172.18.124.202:5000/v2.0/'
keystone_client = ksclient.Client(username=user, password=password,
                                  tenant_name=tenant, auth_url=keystone_url)
nova = nvclient.Client(user, password, tenant, keystone_url,
                       service_type = "compute")
token = keystone_client.auth_token
murano_url = "http://172.18.78.92:8082"
muranoclient = murano_client(endpoint=murano_url, token=token)
quantum_endpoint = 'http://172.18.124.202:9696/'
neutron = netclient.Client('2.0', endpoint_url=quantum_endpoint, token=token)
networks = neutron.list_networks()
for i in keystone_client.tenants.list():                                        
    if i.name == tenant:
        cool =  i.id

for i in muranoclient.environments.list():
    muranoclient.environments.delete(i.id)

for i in networks['networks']:
    if i['tenant_id'] == cool:
        for j in i['subnets']:
            routers = neutron.list_routers()
            for m in routers['routers']:
                if m['tenant_id'] == cool:
                    body = {"subnet_id": str(j)}
                    try:
                        neutron.remove_gateway_router(m['id'])
                    except:
                        print "HUJ"
                    try:
                        neutron.remove_interface_router(m['id'], body)
                    except:
                        print "all is bad:("
                    try:
                        neutron.delete_router(m['id'])
                    except:
                        print "HUJ"
        try:
            neutron.delete_network(i['id'])
        except:
            print "HUJ"

for i in nova.servers.list():
    if i.tenant_id == cool:
        try:
            nova.servers.delete(i)
            time.sleep(5)
        except:
            print "All is bad"
