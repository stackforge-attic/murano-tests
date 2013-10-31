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

import testtools

from tempest import exceptions
from tempest.test import attr
from tempest.tests.murano import base

class SanityMuranoTest(base.MuranoTest):

    @testtools.skip('It is look as a bug')
    @attr(type='negative')
    def test_create_IIS_farm_wo_env_id(self):
        """ Try to create IIS farm without env id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add IIS farm using wrong environment id
            4. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.assertRaises(Exception, self.create_IIS_farm,
                          None, sess['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_create_IIS_farm_wo_sess_id(self):
        """ Try to create IIS farm without session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create IIS farm using wrong session id
            4. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.assertRaises(Exception, self.create_IIS_farm,
                          env['id'], "")
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @testtools.skip("It is look like a bug")
    @attr(type='negative')
    def test_delete_IIS_farm_wo_env_id(self):
        """ Try to delete IIS farm without env id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add IIS farm
            4. Send request to delete IIS farm using wrong environment id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_IIS_farm(env['id'], sess['id'])
        self.assertRaises(Exception, self.delete_service,
                          None, sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_delete_IIS_farm_wo_session_id(self):
        """ Try to delete IIS farm without session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add IIS farm
            4. Send request to delete IIS farm using wrong environment id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_IIS_farm(env['id'], sess['id'])
        self.assertRaises(Exception, self.delete_service,
                          env['id'], "", serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='smoke')
    def test_create_and_delete_apsnet_farm(self):
        """ Create and delete apsnet farm
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add apsnet farm
            4. Send request to remove apsnet farm
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_apsnet_farm(env['id'], sess['id'])
        resp = self.delete_service(env['id'], sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @testtools.skip('It is look as a bug')
    @attr(type='negative')
    def test_create_apsnet_farm_wo_env_id(self):
        """ Try to create aspnet farm without env id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create aspnet farm using wrong environment id
            4. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.assertRaises(Exception, self.create_apsnet_farm,
                          None, sess['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_create_apsnet_farm_wo_sess_id(self):
        """ Try to create aspnet farm without sess id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create aspnet farm using wrong session id
            4. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.assertRaises(Exception, self.create_apsnet_farm,
                          env['id'], "")
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @testtools.skip("It is look like a bug")
    @attr(type='negative')
    def test_delete_apsnet_farm_wo_env_id(self):
        """ Try to delete aspnet farm without env id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add aspnet farm
            4. Send request to delete aspnet farm using wrong environment id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_apsnet_farm(env['id'], sess['id'])
        self.assertRaises(Exception, self.delete_service,
                          None, sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_delete_apsnet_farm_wo_session_id(self):
        """ Try to delete aspnet farm without session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add aspnet farm
            4. Send request to delete aspnet farm using wrong session id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_apsnet_farm(env['id'], sess['id'])
        self.assertRaises(Exception, self.delete_service,
                          env['id'], "", serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='smoke')
    def test_create_and_delete_SQL(self):
        """ Create and delete SQL
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add SQL
            4. Send request to remove SQL
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_SQL(env['id'], sess['id'])
        resp = self.delete_service(env['id'], sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @testtools.skip('It is look as a bug')
    @attr(type='negative')
    def test_create_SQL_wo_env_id(self):
        """ Try to create SQL without env id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create SQL using wrong environment id
            4. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.assertRaises(Exception, self.create_SQL,
                          None, sess['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_create_SQL_wo_sess_id(self):
        """ Try to create SQL without session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create SQL using wrong session id
            4. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.assertRaises(Exception, self.create_SQL,
                          env['id'], "")
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @testtools.skip("It is look like a bug")
    @attr(type='negative')
    def test_delete_SQL_wo_env_id(self):
        """ Try to delete SQL without env id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add SQL
            4. Send request to delete SQL using wrong environment id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_SQL(env['id'], sess['id'])
        self.assertRaises(Exception, self.delete_service,
                          None, sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_delete_SQL_wo_session_id(self):
        """ Try to delete SQL without session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add SQL
            4. Send request to delete SQL using wrong session id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_SQL(env['id'], sess['id'])
        self.assertRaises(Exception, self.delete_service,
                          env['id'], "", serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

