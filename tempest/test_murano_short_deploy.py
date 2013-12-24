# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Mirantis, Inc.
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

from tempest.api.murano import base
from tempest.test import attr


class SanityMuranoTest(base.MuranoTest):

    def test_short_deploy_ad(self):
        flag = 0
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.create_AD(env['id'], sess['id'])
        self.deploy_session(env['id'], sess['id'])
        self.get_session_info(env['id'], sess['id'])
        env.update({'status': None})
        k = 0
        while env['status'] != "ready" or flag != 1:
            time.sleep(15)
            k += 1
            resp, env = self.get_environment_by_id(env['id'])
            if 'status' not in env:
                env.update({'status': None})
            if k > 4:
                flag = 1
        assert flag == 1
        self.delete_environment(env['id'])

    def test_short_deploy_iis(self):
        flag = 0
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.create_IIS(env['id'], sess['id'])
        self.deploy_session(env['id'], sess['id'])
        self.get_session_info(env['id'], sess['id'])
        env.update({'status': None})
        k = 0
        while env['status'] != "ready" or flag != 1:
            time.sleep(15)
            k += 1
            resp, env = self.get_environment_by_id(env['id'])
            if 'status' not in env:
                env.update({'status': None})
            if k > 4:
                flag = 1
        assert flag == 1
        self.delete_environment(env['id'])

    def test_short_deploy_aspnet(self):
        flag = 0
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.create_apsnet(env['id'], sess['id'])
        self.deploy_session(env['id'], sess['id'])
        self.get_session_info(env['id'], sess['id'])
        env.update({'status': None})
        k = 0
        while env['status'] != "ready" or flag != 1:
            time.sleep(15)
            k += 1
            resp, env = self.get_environment_by_id(env['id'])
            if 'status' not in env:
                env.update({'status': None})
            if k > 4:
                flag = 1
        assert flag == 1
        self.delete_environment(env['id'])

    def test_short_deploy_sql(self):
        flag = 0
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.create_SQL(env['id'], sess['id'])
        self.deploy_session(env['id'], sess['id'])
        self.get_session_info(env['id'], sess['id'])
        env.update({'status': None})
        k = 0
        while env['status'] != "ready" or flag != 1:
            time.sleep(15)
            k += 1
            resp, env = self.get_environment_by_id(env['id'])
            if 'status' not in env:
                env.update({'status': None})
            if k > 4:
                flag = 1
        assert flag == 1
        self.delete_environment(env['id'])