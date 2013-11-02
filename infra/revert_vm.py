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

import time
import argparse
import novaclient.v1_1.client as nova_client

parser = argparse.ArgumentParser()
parser.add_argument('--user', type=str, default='admin')
parser.add_argument('--password', type=str, default='password')
parser.add_argument('--tenant', type=str, default='admin')
parser.add_argument('--keystone_url', type=str,
                    default='http://localhost:5000/v2.0/')
parser.add_argument('--instance_name', type=str)
parser.add_argument('--snapshot_name', type=str)
args = parser.parse_args()

nova = nova_client.Client(args.user, args.password, args.tenant,
                          args.keystone_url, service_type = 'compute')

image = nova.images.find(name=args.snapshot_name)
server = nova.servers.find(name=args.instance_name)

server.rebuild(image)
time.sleep(2)  # Wait until the start of recovery
server = nova.servers.find(name=args.instance_name)
while server.status == 'REBUILD':
    server = nova.servers.find(name=args.instance_name)

if server.status != 'ACTIVE':
    server.start()
server = nova.servers.find(name=args.instance_name)
while server.status != 'ACTIVE':
    server = nova.servers.find(name=args.instance_name)
