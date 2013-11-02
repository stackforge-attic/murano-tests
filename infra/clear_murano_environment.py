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

import argparse
from keystoneclient.v2_0 import client as ksclient
from muranoclient.client import Client as mclient

parser = argparse.ArgumentParser()
parser.add_argument('--user', type=str)
parser.add_argument('--password', type=str)
parser.add_argument('--tenant', type=str)
parser.add_argument('--keystone_url', type=str,
                    default='http://localhost:5000/v2.0/')
parser.add_argument('--murano_url', type=str)
args = parser.parse_args()

keystone_client = ksclient.Client(username=args.user,
                                  password=args.password,
                                  tenant_name=args.tenant,
                                  auth_url=args.keystone_url)

murano_client = mclient('1', endpoint=args.murano_url,
                        token=keystone_client.auth_token)

for env in murano_client.environments.list():
    murano_client.environments.delete(env.id)
