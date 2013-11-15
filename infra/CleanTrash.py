from keystoneclient.v2_0 import client as ksclient
from neutronclient.neutron import client as netclient
from muranoclient.v1.client import Client as murano_client
import novaclient.v1_1.client as nvclient
import time
import argparse

parser = argparse.ArgumentParser(description="Script for cleaning trash")
parser.add_argument("-openstack_user",  dest='openstack_user',  type=str,
               help="Openstack username",  default='sergey_demo_user')
parser.add_argument("-openstack_password",  dest='openstack_password',
                    type=str, help="Openstack password",
                    default='111')
parser.add_argument("-openstack_tenant",  dest='openstack_tenant',  type=str,
                    help="Openstack tenant",  default='ForTests')
parser.add_argument("-keystone_url",  dest='keystone_url',  type=str,
               help="Keystone url", default='http://172.18.124.201:5000/v2.0/')
parser.add_argument("-murano_url",  dest='murano_url',  type=str,
               help="Murano url", default='http://172.18.78.92:8082')
parser.add_argument("-neutron_url",  dest='neutron_url',  type=str,
               help="Neutron url", default='http://172.18.124.202:9696/')
args = parser.parse_args()

user = args.openstack_user
password = args.openstack_password
tenant = args.openstack_tenant
keystone_url = args.keystone_url
keystone_client = ksclient.Client(username=user, password=password,
                                  tenant_name=tenant, auth_url=keystone_url)
nova = nvclient.Client(user, password, tenant, keystone_url,
                       service_type = "compute")
token = keystone_client.auth_token
murano_url = args.murano_url
muranoclient = murano_client(endpoint=murano_url, token=token)
quantum_endpoint = args.neutron_url
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
                        print "All is bad"
                    try:
                        neutron.remove_interface_router(m['id'], body)
                    except:
                        print "all is bad:("
                    try:
                        neutron.delete_router(m['id'])
                    except:
                        print "All is bad"
        try:
            neutron.delete_network(i['id'])
        except:
            print "All is bad"

for i in nova.servers.list():
    if i.tenant_id == cool:
        try:
            nova.servers.delete(i)
            time.sleep(5)
        except:
            print "All is bad"

for i in nova.security_groups.list():
    if i.tenant_id == cool and i.name !='default':
        nova.security_groups.delete(i)
