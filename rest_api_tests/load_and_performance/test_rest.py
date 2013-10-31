import unittest
import json
import random
import logging
import ConfigParser
from funkload.utils import Data
from funkload.FunkLoadTestCase import FunkLoadTestCase
from keystoneclient.v2_0 import client as ksclient


logging.basicConfig()
LOG = logging.getLogger(' REST service tests')


class TestSuite(FunkLoadTestCase):

    def setUp(self):
        self.clearHeaders()
        self.url = self.conf_get('main', 'url')
        config = ConfigParser.RawConfigParser()
        config.read('config.ini')
        user = config.get('keystone', 'user')
        password = config.get('keystone', 'password')
        tenant = config.get('keystone', 'tenant')
        keystone_url = config.get('keystone', 'url')
        keystone_client = ksclient.Client(username=user, password=password,
                                    tenant_name=tenant, auth_url=keystone_url)
        token = str(keystone_client.auth_token)
        self.environments = []
        self.setHeader('X-Auth-Token', token)

    def tearDown(self):
        for i in self.environments:
            try:
                self.action_delete_environment(i)
            except:
                pass

    def generate_num(self): 
        p=""
        for i in xrange(10):
            p += str(random.randint(0,10))
        return p

    def action_create_environment(self):
        self.setHeader('Content-Type', 'application/json')
        name = "Environment" + self.generate_num()
        body = '{"name": "%s"}' % name

        response = self.post(self.url, params=Data('application/json', body),
                             description="Create Environment")
        assert response.code == 200
        
        result = json.loads(self.getBody())
        return str(result['id'])

    def action_delete_environment(self, env_id):
        url = self.url + '/' + str(env_id)
        response = self.delete(url, description="Delete Environment")
        assert response.code == 200

    def action_get_session_for_environment(self, env_id):
        self.setHeader('Content-Type', 'application/json')

        url = self.url + '/' + str(env_id) + '/configure'
        response = self.post(url, description="Get Session For Environment")
        assert response.code == 200

        result = json.loads(self.getBody())
        return str(result['id'])


    def action_create_service_ad(self, env_id, session_id, name='ad'):
        self.setHeader('Content-Type', 'application/json')
        self.setHeader('X-Configuration-Session', str(session_id))

        body = ('{"type": "activeDirectory", "name": "%s",'
                '"adminPassword": "P@ssw0rd", "domain": "%s.local",'
                '"availabilityZone": "nova", "unitNamingPattern": "",'
                '"flavor": "m1.medium", "osImage": {"type": "ws-2012-std",'
                '"name": "ws-2012-std",'
                '"title": "Windows Server 2012 Standard"},'
                '"configuration": "standalone",'
                '"units": [{"isMaster": "True", "recoveryPassword": "P@ssw0rd",'
                '"location": "west-dc"}]}') % (name,name)

        url = self.url + '/' + env_id + '/services'

        response = self.post(url, params=Data('application/json', body),
                             description="Create AD service")
        assert response.code == 200

    def action_create_service_iis(self, env_id, session_id, name='iis'):
        self.setHeader('Content-Type', 'application/json')
        self.setHeader('X-Configuration-Session', str(session_id))

        body = ('{"type": "webServer", "domain": "",'
                '"availabilityZone": "nova", "name": "%s",'
                '"adminPassword": "P@ssw0rd", "unitNamingPattern": "",'
                '"osImage": {"type": "ws-2012-std", "name": "ws-2012-std",'
                '"title": "Windows Server 2012 Standard"},'
                '"units": [{}], "credentials": {"username": "Administrator",'
                '"password": "P@ssw0rd"},'
                '"flavor": "m1.medium"}') % name

        url = self.url + '/' + env_id + '/services'
        response = self.post(url, params=Data('application/json', body),
                             description="Create IIS service")
        assert response.code == 200

    def action_create_service_aspnet(self, env_id, session_id, name='aspnet'):
        self.setHeader('Content-Type', 'application/json')
        self.setHeader('X-Configuration-Session', str(session_id))

        body = ('{"type": "aspNetApp", "domain": "",'
                '"availabilityZone": "nova", "name": "%s", "repository":'
                '"git://github.com/Mirantis/murano-mvc-demo.git",'
                '"adminPassword": "P@ssw0rd", "unitNamingPattern": "",'
                '"osImage": {"type": "ws-2012-std", "name": "ws-2012-std",'
                '"title": "Windows Server 2012 Standard"},'
                '"units": [{}], "credentials": {"username": "Administrator",'
                '"password": "P@ssw0rd"},'
                '"flavor": "m1.medium"}') % name

        url = self.url + '/' + env_id + '/services'
        response = self.post(url, params=Data('application/json', body),
                             description="Create ASP.Net service")
        assert response.code == 200

    def action_create_service_iis_farm(self, env_id, session_id, name='iis_farm'):
        self.setHeader('Content-Type', 'application/json')
        self.setHeader('X-Configuration-Session', str(session_id))

        body = ('{"type": "webServerFarm", "domain": "",'
                '"availabilityZone": "nova", "name": "%s",'
                '"adminPassword": "P@ssw0rd", "loadBalancerPort": 80,'
                '"unitNamingPattern": "",'
                '"osImage": {"type": "ws-2012-std", "name": "ws-2012-std",'
                '"title": "Windows Server 2012 Standard"},'
                '"units": [{}, {}],'
                '"credentials": {"username": "Administrator",'
                '"password": "P@ssw0rd"}, "flavor": "m1.medium"}') % name

        url = self.url + '/' + env_id + '/services'
        response = self.post(url, params=Data('application/json', body),
                             description="Create IIS farm service")
        assert response.code == 200

    def action_create_service_aspnet_farm(self, env_id, session_id,
                                          name='aspnet_farm'):
        self.setHeader('Content-Type', 'application/json')
        self.setHeader('X-Configuration-Session', str(session_id))

        body = ('{"type": "aspNetAppFarm", "domain": "",'
                '"availabilityZone": "nova", "name": "%s",'
               '"repository": "git://github.com/Mirantis/murano-mvc-demo.git",'
                '"adminPassword": "P@ssw0rd", "loadBalancerPort": 80,'
                '"unitNamingPattern": "",'
                '"osImage": {"type": "ws-2012-std", "name": "ws-2012-std",'
                '"title": "Windows Server 2012 Standard"},'
                '"units": [{}, {}],'
                '"credentials":  {"username": "Administrator",'
                '"password": "P@ssw0rd"}, "flavor": "m1.medium"}') % name

        url = self.url + '/' + env_id + '/services'
        response = self.post(url, params=Data('application/json', body),
                             description="Create ASP.Net farm service")
        assert response.code == 200

    def action_create_service_sql(self, env_id, session_id, name='sql'):
        self.setHeader('Content-Type', 'application/json')
        self.setHeader('X-Configuration-Session', str(session_id))

        body = ('{"type": "msSqlServer", "domain": "",'
                '"availabilityZone": "nova", "name": "%s",'
                '"adminPassword": "P@ssw0rd", "unitNamingPattern": "",'
                '"saPassword": "P@ssw0rd", "mixedModeAuth": "True",'
                '"osImage": {"type": "ws-2012-std", "name": "ws-2012-std",'
                '"title": "Windows Server 2012 Standard"},"units": [{}],'
                '"credentials": {"username": "Administrator",'
                '"password": "P@ssw0rd"}, "flavor": "m1.medium"}') % name

        url = self.url + '/' + env_id + '/services'
        response = self.post(url, params=Data('application/json', body),
                             description="Create MSSQL service")
        assert response.code == 200

    def action_create_service_linux_agent(self, env_id, session_id,
                                          name='linuxAgent'):
        self.setHeader('Content-Type', 'application/json')
        self.setHeader('X-Configuration-Session', str(session_id))

        body = ('{"availabilityZone": "nova", "name": "%s",'
                '"deployTelnet": "True", "unitNamingPattern": "",'
                '"osImage": {"type": "linux",'
                '"name": "F18-x86_64-cfntools-MURANO",'
                '"title": "Linux with vNext agent"}, "units": [{}],'
                '"flavor": "m1.medium", "type": "linuxTelnetService"}') % name

        url = self.url + '/' + env_id + '/services'
        response = self.post(url, params=Data('application/json', body),
                             description="Create Linux Agent service")
        assert response.code == 200

    def test_create_and_delete_environment(self):
        env_id = self.action_create_environment()
        self.environments.append(env_id)
        self.action_delete_environment(env_id)
        self.environments.pop(self.environments.index(env_id))

    def test_get_list_of_environments(self):
        response = self.get(self.url, description="Get List Of Environments")
        assert response.code == 200

    def test_create_environment_with_ad(self):
        env_id = self.action_create_environment()
        self.environments.append(env_id)
        session_id = self.action_get_session_for_environment(env_id)
        self.action_create_service_ad(env_id, session_id, 'test1')
        self.action_create_service_ad(env_id, session_id, 'test2')
        self.action_create_service_ad(env_id, session_id, 'test3')
        self.action_delete_environment(env_id)
        self.environments.pop(self.environments.index(env_id))

    def test_create_environment_with_iis(self):
        env_id = self.action_create_environment()
        self.environments.append(env_id)
        session_id = self.action_get_session_for_environment(env_id)
        self.action_create_service_iis(env_id, session_id, 'test1')
        self.action_create_service_iis(env_id, session_id, 'test2')
        self.action_create_service_iis(env_id, session_id, 'test3')
        self.action_delete_environment(env_id)
        self.environments.pop(self.environments.index(env_id))

    def test_create_environment_with_aspnet(self):
        env_id = self.action_create_environment()
        self.environments.append(env_id)
        session_id = self.action_get_session_for_environment(env_id)
        self.action_create_service_aspnet(env_id, session_id, 'test1')
        self.action_delete_environment(env_id)
        self.environments.pop(self.environments.index(env_id))

    def test_create_environment_with_iis_farm(self):
        env_id = self.action_create_environment()
        self.environments.append(env_id)
        session_id = self.action_get_session_for_environment(env_id)
        self.action_create_service_iis_farm(env_id, session_id, 'test1')
        self.action_delete_environment(env_id)
        self.environments.pop(self.environments.index(env_id))

    def test_create_environment_with_aspnet_farm(self):
        env_id = self.action_create_environment()
        self.environments.append(env_id)
        session_id = self.action_get_session_for_environment(env_id)
        self.action_create_service_aspnet_farm(env_id, session_id, 'test1')
        self.action_delete_environment(env_id)
        self.environments.pop(self.environments.index(env_id))

    def test_create_environment_with_sql(self):
        env_id = self.action_create_environment()
        self.environments.append(env_id)
        session_id = self.action_get_session_for_environment(env_id)
        self.action_create_service_sql(env_id, session_id, 'test1')
        self.action_delete_environment(env_id)
        self.environments.pop(self.environments.index(env_id))

    def test_create_environment_with_linux_agent(self):
        env_id = self.action_create_environment()
        self.environments.append(env_id)
        session_id = self.action_get_session_for_environment(env_id)
        self.action_create_service_linux_agent(env_id, session_id, 'test1')
        self.action_delete_environment(env_id)
        self.environments.pop(self.environments.index(env_id))

    def mix_for_load_testing(self):
        k = random.randint(0,100)
        if k < 5:
            return self.test_create_and_delete_environment()
        elif k < 10:
            return self.test_get_list_of_environments()
        elif k < 23:
            return self.test_create_environment_with_ad()
        elif k < 36:
            return self.test_create_environment_with_iis()
        elif k < 49:
            return self.test_create_environment_with_aspnet()
        elif k < 62:
            return self.test_create_environment_with_iis_farm()
        elif k < 75:
            return self.test_create_environment_with_aspnet_farm()
        elif k < 88:
            return self.test_create_environment_with_sql()
        elif k < 100:
            return self.test_create_environment_with_linux_agent()


if __name__ == '__main__':
    unittest.main()
