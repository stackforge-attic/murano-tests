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

    @attr(type='positive')
    def test_alternate_service_create1(self):
        """ Check alternate creating and deleting services
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create session
            4. Send request to create session
            5. Send request to create AD(session1)
            6. Send request to create IIS(session1)
            7. Send request to create SQL(session1)
            8. Send request to create IIS(session3)
            9. Send request to create aspnet farm(session3)
            10. Send request to create AD(session3)
            11. Send request to create IIS farm(session3)
            12. Send request to create SQL cluster(session3)
            13. Send request to delete IIS(session1)
            14. Send request to create IIS(session2)
            15. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess1 = self.create_session(env['id'])
        resp, sess2 = self.create_session(env['id'])
        resp, sess3 = self.create_session(env['id'])
        resp, serv1 = self.create_AD(env['id'], sess1['id'])
        resp, infa = self.get_list_services(env['id'], sess1['id'])
        assert len(infa) == 1
        resp, serv2 = self.create_IIS(env['id'], sess1['id'], serv1['domain'])
        resp, infa = self.get_list_services(env['id'], sess1['id'])
        assert len(infa) == 2
        resp, serv3 = self.create_SQL(env['id'], sess1['id'], serv1['domain'])
        resp, infa = self.get_list_services(env['id'], sess1['id'])
        assert len(infa) == 3
        resp, serv31 = self.create_IIS(env['id'], sess3['id'])
        resp, infa = self.get_list_services(env['id'], sess3['id'])
        assert len(infa) == 1
        resp, serv32 = self.create_apsnet_farm(env['id'], sess3['id'])
        resp, infa = self.get_list_services(env['id'], sess3['id'])
        assert len(infa) == 2
        resp, serv33 = self.create_AD(env['id'], sess3['id'])
        resp, infa = self.get_list_services(env['id'], sess3['id'])
        assert len(infa) == 3
        resp, serv34 = self.create_IIS_farm(env['id'], sess3['id'],
                                            serv33['domain'])
        resp, infa = self.get_list_services(env['id'], sess3['id'])
        assert len(infa) == 4
        resp, serv35 = self.create_SQL_cluster(env['id'], sess3['id'],
                                       serv33['domain'])
        resp, infa = self.get_list_services(env['id'], sess3['id'])
        assert len(infa) == 5
        resp = self.delete_service(env['id'], sess1['id'], serv2['id'])
        resp, infa = self.get_list_services(env['id'], sess1['id'])
        assert len(infa) == 2
        resp, serv21 = self.create_IIS(env['id'], sess2['id'])
        resp, infa = self.get_list_services(env['id'], sess2['id'])
        assert len(infa) == 1
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='positive')
    def test_alternate_service_create2(self):
        """ Check alternate creating and deleting services
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create IIS
            4. Send request to create aspnet farm
            5. Send request to create AD
            6. Send request to create IIS
            7. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv1 = self.create_IIS(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 1
        resp, serv2 = self.create_apsnet_farm(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 2
        resp, serv3 = self.create_AD(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 3
        resp, serv4 = self.create_IIS(env['id'], sess['id'], serv3['domain'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 4
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='positive')
    def test_alternate_service_create3(self):
        """ Check alternate creating and deleting services
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create aspnet farm
            4. Send request to create SQL cluster
            5. Send request to create SQL
            6. Send request to create AD
            7. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv1 = self.create_apsnet_farm(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 1
        resp, serv2 = self.create_SQL_cluster(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 2
        resp, serv3 = self.create_SQL(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 3
        resp, serv4 = self.create_AD(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 4
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='positive')
    def test_alternate_service_create4(self):
        """ Check alternate creating and deleting services
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create IIS
            4. Send request to create AD
            5. Send request to create SQL
            6. Send request to create SQL cluster
            7. Send request to create aspnet farm
            8. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)                     
        resp, sess = self.create_session(env['id'])
        resp, serv1 = self.create_IIS(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 1
        resp, serv2 = self.create_AD(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 2
        resp, serv3 = self.create_SQL(env['id'], sess['id'], serv2['domain'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 3
        resp, serv4 = self.create_SQL_cluster(env['id'], sess['id'],
                                      serv2['domain'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 4
        resp, serv5 = self.create_apsnet_farm(env['id'], sess['id'],
                                              serv2['domain'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 5
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='positive')
    def test_alternate_service_create5(self):
        """ Check alternate creating and deleting services
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create aspnet
            4. Send request to create IIS
            5. Send request to delete aspnet
            6. Send request to create AD
            7. Send request to delete IIS
            8. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv1 = self.create_apsnet(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 1
        resp, serv2 = self.create_IIS(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 2
        resp = self.delete_service(env['id'], sess['id'], serv1['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 1
        resp, serv1 = self.create_AD(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 2
        resp = self.delete_service(env['id'], sess['id'], serv2['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 1
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='positive')
    def test_alternate_service_create6(self):
        """ Check alternate creating and deleting services
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create SQL cluster
            4. Send request to create SQL cluster
            5. Send request to create SQL cluster
            6. Send request to create SQL cluster
            7. Send request to create SQL cluster
            8. Send request to create IIS
            9. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)                     
        resp, sess = self.create_session(env['id'])
        for i in xrange(5):
            resp, serv1 = self.create_SQL_cluster(env['id'], sess['id'])
            resp, infa = self.get_list_services(env['id'], sess['id'])
            assert len(infa) == i + 1
        resp, serv2 = self.create_IIS(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 6
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='positive')
    def test_alternate_service_create7(self):
        """ Check alternate creating and deleting services
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create aspnet
            4. Send request to create SQL
            5. Send request to create IIS
            6. Send request to create SQL
            7. Send request to create aspnet
            8. Send request to create IIS
            7. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)                     
        resp, sess = self.create_session(env['id'])
        resp, serv1 = self.create_apsnet(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 1
        resp, serv2 = self.create_SQL(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 2
        resp, serv3 = self.create_IIS(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 3
        resp, serv4 = self.create_SQL(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 4
        resp, serv5 = self.create_apsnet(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 5
        resp, serv6 = self.create_IIS(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 6
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='positive')
    def test_alternate_service_create8(self):
        """ Check alternate creating and deleting services
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create IIS
            4. Send request to create SQL
            5. Send request to create aspnet farm
            6. Send request to delete IIS
            7. Send request to create IIS
            8. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)                     
        resp, sess = self.create_session(env['id'])
        resp, serv1 = self.create_IIS(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 1
        resp, serv2 = self.create_SQL(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 2
        resp, serv3 = self.create_apsnet_farm(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 3
        resp = self.delete_service(env['id'], sess['id'], serv1['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 2
        resp, serv1 = self.create_IIS(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 3
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_double_delete_service(self):
        """ Try to double delete service
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create IIS
            4. Send request to delete IIS
            5. Send request to delete IIS
            6. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv1 = self.create_IIS(env['id'], sess['id'])
        resp = self.delete_service(env['id'], sess['id'], serv1['id'])
        self.assertRaises(Exception, self.delete_service, env['id'],
                          sess['id'], serv1['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))
