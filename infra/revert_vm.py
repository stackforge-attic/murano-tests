# Copyright 2013 OpenStack Foundation
# Copyright 2013 Mirantis Inc
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
import argparse
import novaclient.v1_1.client as nvclient
from keystoneclient.v2_0 import client as ksclient

parser = argparse.ArgumentParser(description="Script for Jobs")
parser.add_argument("-openstack_user", dest='openstack_user', type=str,
                    help="Openstack username", default='admin')
parser.add_argument("-openstack_password", dest='openstack_password',
                    type=str, help="Openstack password", default='password')
parser.add_argument("-openstack_tenant", dest='openstack_tenant', type=str,
                    help="Openstack tenant", default='admin')
parser.add_argument("-keystone_url", dest='keystone_url', type=str,
                    help="Keystone url",
                    default='http://localhost:5000/v2.0/')
parser.add_argument("-instance_name", dest='instance_name', type=str,
                    help="Name of reverting instance", default='VM')
parser.add_argument("-snapshot_name", dest='snapshot_name', type=str,
                    help="Name of using snapshot", default="VM_snapshot")
parser.add_argument("-flavor_name", dest='flavor_name', type=str,
                    help="Name of using flavor", default="t1.test_node")
parser.add_argument("-user", dest='user', type=str, default="root")
parser.add_argument("-openstack_ip", dest='openstack_ip',  type=str,
                    default="localhost")
parser.add_argument("-branch_name", dest='branch_name',
                    type=str, default="master")
parser.add_argument("-rabbitmq_port", dest='rabbitmq_port', type=str,
                    help="Port of RabbitMQ", default="5672")
args = parser.parse_args()

user = args.openstack_user
password = args.openstack_password
tenant = args.openstack_tenant
keystone_url = args.keystone_url

keystone_client = ksclient.Client(username=user, password=password,
                                  tenant_name=tenant, auth_url=keystone_url)

nova = nvclient.Client(user, password, tenant, keystone_url,
                       service_type = "compute")

server = nova.servers.find(name=args.instance_name)
server.delete()

while 1:
    try:
        server = nova.servers.find(name=args.instance_name)
    except:
        break

image = nova.images.find(name=args.snapshot_name)
flavor = nova.flavors.find(name=args.flavor_name)
instance = nova.servers.create(name=args.instance_name,
                               image=image, flavor=flavor)
server = nova.servers.find(name=args.instance_name)

while server.status != "ACTIVE":
    server = nova.servers.find(name=args.instance_name)

print dir(server)
## Excuse me for this code :) I will fix it
os.system("nova show " + str(server.id) + " | grep private > log.txt")
f = open("log.txt").read().split()[-2]

cmd = "expect infra/deploy_vm.sh %s %s %s %s %s"
os.system(cmd % (args.user, f, args.openstack_ip,
                 args.branch_name, args.rabbitmq_port))
