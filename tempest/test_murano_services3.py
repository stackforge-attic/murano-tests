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

    @attr(type='smoke')
    def test_create_and_delete_SQL_cluster(self):
        """ Create and delete SQL
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add SQL
            4. Send request to delete SQL
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_SQL_cluster(env['id'], sess['id'])
        resp = self.delete_service(env['id'], sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='smoke')
    def test_create_and_delete_linux_agent(self):
        """ Create and delete Linux Agent
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add linux agent
            4. Send request to delete linux agent
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_linux_agent(env['id'], sess['id'])
        resp = self.delete_service(env['id'], sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @testtools.skip('It is look as a bug')
    @attr(type='negative')
    def test_create_linux_agent_wo_env_id(self):
        """ Try create Linux Agent without env_id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add linux agent using wrong env_id
            4. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.assertRaises(Exception, self.create_linux_agent,
                          None, sess['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_create_linux_agent_wo_sess_id(self):
        """ Try to create Linux Agent without session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add linux agent using uncorrect session id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.assertRaises(Exception, self.create_linux_agent,
                          env['id'], "")
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @testtools.skip("It is look like a bug")
    @attr(type='negative')
    def test_delete_linux_agent_wo_env_id(self):
        """ Try to delete Linux Agent without environment id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add linux agent
            4. Send request to remove linux agent using uncorrect
               environment id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_linux_agent(env['id'], sess['id'])
        self.assertRaises(Exception, self.delete_service,
                          None, sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_delete_linux_agent_wo_session_id(self):
        """ Try to delete linux agent without session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add linux agent
            4. Send request to remove linux agent using wrong session id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_linux_agent(env['id'], sess['id'])
        self.assertRaises(Exception, self.delete_service,
                          env['id'], "", serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='smoke')
    def test_get_list_services(self):
        """ Get a list of services
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD
            4. Send request to get list of services
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_AD(env['id'], sess['id'])
        resp, somelist = self.get_list_services(env['id'], sess['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_get_list_of_services_wo_env_id(self):
        """ Try to get services list withoun env id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD
            4. Send request to get services list using wrong environment id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_AD(env['id'], sess['id'])
        self.assertRaises(Exception, self.get_list_services,
                          None, sess['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_get_list_of_services_wo_sess_id(self):
        """ Try to get services list withoun session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD
            4. Send request to get services list using wrong session id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_AD(env['id'], sess['id'])
        resp, somelist = self.get_list_services(env['id'], "")
        assert somelist == []
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_get_list_of_services_after_delete_env(self):
        """ Try to get services list after deleting env
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD
            4. Send request to delete environment
            5. Send request to get services list
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_AD(env['id'], sess['id'])
        resp = self.delete_environment(env['id'])
        self.assertRaises(Exception, self.get_list_services,
                          env['id'], sess['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_get_list_of_services_after_delete_session(self):
        """ Try to get services list after deleting session
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD
            4. Send request to delete session
            5. Send request to get services list
            6. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_AD(env['id'], sess['id'])
        resp = self.delete_session(env['id'], sess['id'])
        self.assertRaises(Exception, self.get_list_services,
                          env['id'], sess['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @testtools.skip("Service is not yet able to do it")
    @attr(type='smoke')
    def test_update_service(self):
        """ Update service
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD
            4. Send request to update service
            5. Send request to remove AD
            6. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_AD(env['id'], sess['id'])
        resp, updt = self.update_service(env['id'], sess['id'], serv['id'],
                                         serv)
        resp = self.delete_service(env['id'], sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='smoke')
    def test_get_service_info(self):
        """ Get service detailed info
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create AD
            4. Send request to get detailed info about service
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_AD(env['id'], sess['id'])
        resp, serv = self.get_service_info(env['id'], sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))
