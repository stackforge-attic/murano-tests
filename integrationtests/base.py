from keystoneclient.v2_0 import client as ksclient
from muranoclient.v1.client import Client as murano_client
from glanceclient import Client as gclient
from metadataclient.v1.client import Client as metadata_client
import testtools
import testresources
import config as cfg
import json
import time


class MuranoBase(testtools.TestCase, testtools.testcase.WithAttributes,
                 testresources.ResourcedTestCase):

    @classmethod
    def setUpClass(cls):
        super(MuranoBase, cls).setUpClass()

        cls.auth = ksclient.Client(username=cfg.murano.user,
                                   password=cfg.murano.password,
                                   tenant_name=cfg.murano.tenant,
                                   auth_url=cfg.murano.auth_url)

        cls.murano = murano_client(endpoint=cfg.murano.murano_url,
                                   token=cls.auth.auth_token)

        cls.murano_repo = metadata_client(endpoint=cfg.murano.metadata_url,
                                          token=cls.auth.auth_token)

    def setUp(self):
        super(MuranoBase, self).setUp()

        self.environments_id = []

    def tearDown(self):
        super(MuranoBase, self).tearDown()

        for environment_id in self.environments_id:

            try:
                self.murano.environments.delete(environment_id)

            except Exception:
                pass

    def create_demo_service(self, environment_id, session_id,
                            image_name="demo"):
        post_body = {"availabilityZone": "nova", "name": "demo",
                     "unitNamingPattern": "host",
                     "osImage": {"type": "cirros.demo", "name": image_name,
                                 "title": "Demo"},
                     "units": [{}], "flavor": "m1.small",
                     "configuration": "standalone", "type": "demoService"}

        return self.murano.services.post(environment_id,
                                         path='/',
                                         data=post_body,
                                         session_id=session_id)

    def create_linux_telnet(self, environment_id, session_id,
                            image_name="linux"):
        post_body = {"availabilityZone": "nova", "name": "LinuxTelnet",
                     "deployTelnet": True, "unitNamingPattern": "telnet",
                     "keyPair": "murano-lb-key",
                     "osImage": {"type": "linux", "name": image_name,
                                 "title": "Linux Image"},
                     "units": [{}],
                     "flavor": "m1.small", "type": "linuxTelnetService"}

        return self.murano.services.post(environment_id,
                                         path='/',
                                         data=post_body,
                                         session_id=session_id)

    def create_linux_apache(self, environment_id, session_id,
                            image_name="linux"):
        post_body = {"availabilityZone": "nova", "name": "LinuxApache",
                     "deployApachePHP": True, "unitNamingPattern": "apache",
                     "keyPair": "murano-lb-key",
                     "instanceCount": [{}],
                     "osImage": {"type": "linux", "name": image_name,
                                 "title": "Linux Image"},
                     "units": [{}],
                     "flavor": "m1.small", "type": "linuxApacheService"}

        return self.murano.services.post(environment_id,
                                         path='/',
                                         data=post_body,
                                         session_id=session_id)

    def create_windows_active_directory(self, environment_id, session_id,
                                        image_name="windows"):
        post_body = {"type": "activeDirectory", "name": "ad.local",
                     "adminPassword": "P@ssw0rd", "domain": "ad.local",
                     "availabilityZone": "nova",
                     "unitNamingPattern": "adinstance",
                     "flavor": "m1.medium", "osImage":
                     {"type": "ws-2012-std", "name": image_name,
                      "title": "Windows Server 2012 Standard"},
                     "configuration": "standalone",
                     "units": [{"isMaster": True,
                                "recoveryPassword": "P@ssw0rd",
                                "location": "west-dc"}]}

        return self.murano.services.post(environment_id,
                                         path='/',
                                         data=post_body,
                                         session_id=session_id)

    def create_windows_iis(self, environment_id, session_id, domain_name="",
                           image_name="windows"):
        post_body = {"type": "webServer", "domain": domain_name,
                     "availabilityZone": "nova", "name": "IisService",
                     "adminPassword": "P@ssw0rd",
                     "unitNamingPattern": "iisinstance",
                     "osImage": {"type": "ws-2012-std", "name": image_name,
                                 "title": "Windows Server 2012 Standard"},
                     "units": [{}],
                     "credentials": {"username": "Administrator",
                                     "password": "P@ssw0rd"},
                     "flavor": "m1.medium"}

        return self.murano.services.post(environment_id,
                                         path='/',
                                         data=post_body,
                                         session_id=session_id)

    def create_windows_aspnet(self, environment_id, session_id,
                              domain_name="", image_name="windows"):
        post_body = {"type": "aspNetApp", "domain": domain_name,
                     "availabilityZone": "nova",
                     "name": "someasp", "repository":
                     "git://github.com/Mirantis/murano-mvc-demo.git",
                     "adminPassword": "P@ssw0rd",
                     "unitNamingPattern": "aspnetinstance",
                     "osImage": {"type": "ws-2012-std", "name": image_name,
                                 "title": "Windows Server 2012 Standard"},
                     "units": [{}],
                     "credentials": {"username": "Administrator",
                                     "password": "P@ssw0rd"},
                     "flavor": "m1.medium"}

        return self.murano.services.post(environment_id,
                                         path='/',
                                         data=post_body,
                                         session_id=session_id)

    def create_windows_iis_farm(self, environment_id, session_id,
                                domain_name="", image_name="windows"):
        post_body = {"type": "webServerFarm", "domain": domain_name,
                     "availabilityZone": "nova", "name": "someIISFARM",
                     "adminPassword": "P@ssw0rd", "loadBalancerPort": 80,
                     "unitNamingPattern": "",
                     "osImage": {"type": "ws-2012-std", "name": image_name,
                                 "title": "Windows Server 2012 Standard"},
                     "units": [{}, {}],
                     "credentials": {"username": "Administrator",
                                     "password": "P@ssw0rd"},
                     "flavor": "m1.medium"}

        return self.murano.services.post(environment_id,
                                         path='/',
                                         data=post_body,
                                         session_id=session_id)

    def create_windows_aspnet_farm(self, environment_id, session_id,
                                   domain_name="", image_name="windows"):
        post_body = {"type": "aspNetAppFarm", "domain": domain_name,
                     "availabilityZone": "nova", "name": "SomeApsFarm",
                     "repository":
                             "git://github.com/Mirantis/murano-mvc-demo.git",
                     "adminPassword": "P@ssw0rd", "loadBalancerPort": 80,
                     "unitNamingPattern": "",
                     "osImage": {"type": "ws-2012-std", "name": image_name,
                                 "title": "Windows Server 2012 Standard"},
                     "units": [{}, {}],
                     "credentials": {"username": "Administrator",
                                     "password": "P@ssw0rd"},
                     "flavor": "m1.medium"}

        return self.murano.services.post(environment_id,
                                         path='/',
                                         data=post_body,
                                         session_id=session_id)

    def create_windows_sql(self, environment_id, session_id, domain_name="",
                           image_name="windows"):
        post_body = {"type": "msSqlServer", "domain": domain_name,
                     "availabilityZone": "nova", "name": "SQLSERVER",
                     "adminPassword": "P@ssw0rd",
                     "unitNamingPattern": "sqlinstance",
                     "saPassword": "P@ssw0rd", "mixedModeAuth": True,
                     "osImage": {"type": "ws-2012-std", "name": image_name,
                                 "title": "Windows Server 2012 Standard"},
                     "units": [{}],
                     "credentials": {"username": "Administrator",
                                     "password": "P@ssw0rd"},
                     "flavor": "m1.medium"}

        return self.murano.services.post(environment_id,
                                         path='/',
                                         data=post_body,
                                         session_id=session_id)

    def create_windows_sql_cluster(self, environment_id, session_id,
                                   domain_name="", image_name="windows"):
        post_body = {"domain": domain_name, "domainAdminPassword": "P@ssw0rd",
                     "externalAD": False,
                     "sqlServiceUserName": "Administrator",
                     "sqlServicePassword": "P@ssw0rd",
                     "osImage": {"type": "ws-2012-std", "name": image_name,
                                 "title": "Windows Server 2012 Standard"},
                     "agListenerName": "SomeSQL_AGListner",
                     "flavor": "m1.medium",
                     "agGroupName": "SomeSQL_AG",
                     "domainAdminUserName": "Administrator",
                     "agListenerIP": "10.0.0.150",
                     "clusterIP": "10.0.0.155",
                     "type": "msSqlClusterServer", "availabilityZone": "nova",
                     "adminPassword": "P@ssw0rd",
                     "clusterName": "SomeSQL", "mixedModeAuth": True,
                     "unitNamingPattern": "",
                     "units": [{"isMaster": True, "name": "node1",
                                "isSync": True},
                               {"isMaster": False, "name": "node2",
                                "isSync": True}],
                     "name": "Sqlname", "saPassword": "P@ssw0rd",
                     "databases": ['NewDB']}

        return self.murano.services.post(environment_id,
                                         path='/',
                                         data=post_body,
                                         session_id=session_id)

    def transform_returned_list_of_files(self, list_):
        list_of_objects = []
        for obj in list_:
            object_ = str(obj).split('/')[1]
            list_of_objects.append(object_)
        return list_of_objects

    def form_service_list(self, list_):
        list_of_objects = []
        for obj in list_:
            object_ = str(obj).split('(')[0]
            list_of_objects.append(object_)
        return list_of_objects


class MuranoEnvironments(MuranoBase):

    def test_create_and_delete_environment(self):
        environment = self.murano.environments.create('testenv')
        self.environments_id.append(environment.id)

        self.assertIn(environment, self.murano.environments.list())
        self.murano.environments.delete(environment.id)
        self.assertNotIn(environment, self.murano.environments.list())

        self.environments_id.pop(self.environments_id.index(environment.id))

    def test_get_environments_list(self):
        environments_list = self.murano.environments.list()
        self.assertTrue(isinstance(environments_list, list))

    def test_update_environment(self):
        environment = self.murano.environments.create('testenv')
        self.environments_id.append(environment.id)

        new_environment = self.murano.environments.update(environment.id,
                                                          'testenvupdated')

        self.assertEqual(new_environment.name, 'testenvupdated')

    def test_get_environment(self):
        environment = self.murano.environments.create('testenv')
        self.environments_id.append(environment.id)

        gotten_environment = self.murano.environments.get(environment.id)

        self.assertEqual(environment, gotten_environment)


class MuranoSessions(MuranoBase):

    def test_create_and_delete_session(self):
        environment = self.murano.environments.create('testenv')
        self.environments_id.append(environment.id)

        session = self.murano.sessions.configure(environment.id)
        self.assertEqual(session.environment_id, environment.id)

        self.murano.sessions.delete(environment.id, session.id)

    def test_get_session(self):
        environment = self.murano.environments.create('testenv')
        self.environments_id.append(environment.id)

        session = self.murano.sessions.configure(environment.id)

        gotten_session = self.murano.sessions.get(environment.id, session.id)

        self.assertEqual(session, gotten_session)


class MuranoServices(MuranoBase):

    def test_create_and_delete_demo_service(self):
        environment = self.murano.environments.create('testenv')
        session = self.murano.sessions.configure(environment.id)
        self.environments_id.append(environment.id)

        service = self.create_demo_service(environment.id, session.id)

        gotten_environment = self.murano.environments.get(environment.id,
                                                          session.id)

        services = [(x['name'], x['id']) for x in gotten_environment.services]
        self.assertIn((service.name, service.id), services)

        self.murano.services.delete(environment.id,
                                    '/' + service.id,
                                    session.id)

        gotten_environment = self.murano.environments.get(environment.id,
                                                          session.id)

        services = [(x['name'], x['id']) for x in gotten_environment.services]
        self.assertNotIn((service.name, service.id), services)

    def test_create_and_delete_linux_telnet_service(self):
        environment = self.murano.environments.create('testenv')
        session = self.murano.sessions.configure(environment.id)
        self.environments_id.append(environment.id)

        service = self.create_linux_telnet(environment.id, session.id)

        gotten_environment = self.murano.environments.get(environment.id,
                                                          session.id)

        services = [(x['name'], x['id']) for x in gotten_environment.services]
        self.assertIn((service.name, service.id), services)

        self.murano.services.delete(environment.id,
                                    '/' + service.id,
                                    session.id)

        gotten_environment = self.murano.environments.get(environment.id,
                                                          session.id)

        services = [(x['name'], x['id']) for x in gotten_environment.services]
        self.assertNotIn((service.name, service.id), services)

    def test_create_and_delete_linux_apache_service(self):
        environment = self.murano.environments.create('testenv')
        session = self.murano.sessions.configure(environment.id)
        self.environments_id.append(environment.id)

        service = self.create_linux_apache(environment.id, session.id)

        gotten_environment = self.murano.environments.get(environment.id,
                                                          session.id)

        services = [(x['name'], x['id']) for x in gotten_environment.services]
        self.assertIn((service.name, service.id), services)

        self.murano.services.delete(environment.id,
                                    '/' + service.id,
                                    session.id)

        gotten_environment = self.murano.environments.get(environment.id,
                                                          session.id)

        services = [(x['name'], x['id']) for x in gotten_environment.services]
        self.assertNotIn((service.name, service.id), services)

    def test_create_and_delete_windows_active_directory_service(self):
        environment = self.murano.environments.create('testenv')
        session = self.murano.sessions.configure(environment.id)
        self.environments_id.append(environment.id)

        service = self.create_windows_active_directory(environment.id,
                                                       session.id)

        gotten_environment = self.murano.environments.get(environment.id,
                                                          session.id)

        services = [(x['name'], x['id']) for x in gotten_environment.services]
        self.assertIn((service.name, service.id), services)

        self.murano.services.delete(environment.id,
                                    '/' + service.id,
                                    session.id)

        gotten_environment = self.murano.environments.get(environment.id,
                                                          session.id)

        services = [(x['name'], x['id']) for x in gotten_environment.services]
        self.assertNotIn((service.name, service.id), services)

    def test_create_and_delete_windows_iis_service(self):
        environment = self.murano.environments.create('testenv')
        session = self.murano.sessions.configure(environment.id)
        self.environments_id.append(environment.id)

        service = self.create_windows_iis(environment.id, session.id)

        gotten_environment = self.murano.environments.get(environment.id,
                                                          session.id)

        services = [(x['name'], x['id']) for x in gotten_environment.services]
        self.assertIn((service.name, service.id), services)

        self.murano.services.delete(environment.id,
                                    '/' + service.id,
                                    session.id)

        gotten_environment = self.murano.environments.get(environment.id,
                                                          session.id)

        services = [(x['name'], x['id']) for x in gotten_environment.services]
        self.assertNotIn((service.name, service.id), services)

    def test_create_and_delete_windows_aspnet_service(self):
        environment = self.murano.environments.create('testenv')
        session = self.murano.sessions.configure(environment.id)
        self.environments_id.append(environment.id)

        service = self.create_windows_aspnet(environment.id, session.id)

        gotten_environment = self.murano.environments.get(environment.id,
                                                          session.id)

        services = [(x['name'], x['id']) for x in gotten_environment.services]
        self.assertIn((service.name, service.id), services)

        self.murano.services.delete(environment.id,
                                    '/' + service.id,
                                    session.id)

        gotten_environment = self.murano.environments.get(environment.id,
                                                          session.id)

        services = [(x['name'], x['id']) for x in gotten_environment.services]
        self.assertNotIn((service.name, service.id), services)

    def test_create_and_delete_windows_iis_farm_service(self):
        environment = self.murano.environments.create('testenv')
        session = self.murano.sessions.configure(environment.id)
        self.environments_id.append(environment.id)

        service = self.create_windows_iis_farm(environment.id, session.id)

        gotten_environment = self.murano.environments.get(environment.id,
                                                          session.id)

        services = [(x['name'], x['id']) for x in gotten_environment.services]
        self.assertIn((service.name, service.id), services)

        self.murano.services.delete(environment.id,
                                    '/' + service.id,
                                    session.id)

        gotten_environment = self.murano.environments.get(environment.id,
                                                          session.id)

        services = [(x['name'], x['id']) for x in gotten_environment.services]
        self.assertNotIn((service.name, service.id), services)

    def test_create_and_delete_windows_aspnet_farm_service(self):
        environment = self.murano.environments.create('testenv')
        session = self.murano.sessions.configure(environment.id)
        self.environments_id.append(environment.id)

        service = self.create_windows_aspnet_farm(environment.id, session.id)

        gotten_environment = self.murano.environments.get(environment.id,
                                                          session.id)

        services = [(x['name'], x['id']) for x in gotten_environment.services]
        self.assertIn((service.name, service.id), services)

        self.murano.services.delete(environment.id,
                                    '/' + service.id,
                                    session.id)

        gotten_environment = self.murano.environments.get(environment.id,
                                                          session.id)

        services = [(x['name'], x['id']) for x in gotten_environment.services]
        self.assertNotIn((service.name, service.id), services)

    def test_create_and_delete_windows_sql_service(self):
        environment = self.murano.environments.create('testenv')
        session = self.murano.sessions.configure(environment.id)
        self.environments_id.append(environment.id)

        service = self.create_windows_sql(environment.id, session.id)

        gotten_environment = self.murano.environments.get(environment.id,
                                                          session.id)

        services = [(x['name'], x['id']) for x in gotten_environment.services]
        self.assertIn((service.name, service.id), services)

        self.murano.services.delete(environment.id,
                                    '/' + service.id,
                                    session.id)

        gotten_environment = self.murano.environments.get(environment.id,
                                                          session.id)

        services = [(x['name'], x['id']) for x in gotten_environment.services]
        self.assertNotIn((service.name, service.id), services)

    def test_create_and_delete_windows_sql_cluster_service(self):
        environment = self.murano.environments.create('testenv')
        session = self.murano.sessions.configure(environment.id)
        self.environments_id.append(environment.id)

        service = self.create_windows_sql_cluster(environment.id, session.id)

        gotten_environment = self.murano.environments.get(environment.id,
                                                          session.id)

        services = [(x['name'], x['id']) for x in gotten_environment.services]
        self.assertIn((service.name, service.id), services)

        self.murano.services.delete(environment.id,
                                    '/' + service.id,
                                    session.id)

        gotten_environment = self.murano.environments.get(environment.id,
                                                          session.id)

        services = [(x['name'], x['id']) for x in gotten_environment.services]
        self.assertNotIn((service.name, service.id), services)


class ImageException(Exception):
    message = "Image doesn't exist"

    def __init__(self, type):
        self._error_string = self.message + '\nDetails: %s' \
                                            ' image is not found,' % str(type)

    def __str__(self):
        return self._error_string


class MuranoDeploy(MuranoBase):

    @classmethod
    def setUpClass(cls):
        super(MuranoDeploy, cls).setUpClass()

        if not cfg.murano.deploy:
            raise cls.skipException("Murano deployment tests are disabled")

        glance_endpoint = cls.auth.service_catalog.url_for(
            service_type='image', endpoint_type='publicURL')
        glance = gclient('1', endpoint=glance_endpoint,
                         token=cls.auth.auth_token)

        image_list = []
        for i in glance.images.list():
            image_list.append(i)

        cls.demo_image = cls.get_image_name('demo', image_list)
        cls.linux_image = cls.get_image_name('linux', image_list)
        cls.windows_image = cls.get_image_name('windows', image_list)

    @classmethod
    def get_image_name(cls, type_of_image, list_of_images):
        for i in list_of_images:
            if 'murano_image_info' in i.properties.keys():
                if type_of_image in json.loads(
                        i.properties['murano_image_info'])['type']:
                    return i.name
        raise ImageException(type_of_image)

    def test_deploy_demo_service(self):
        environment = self.murano.environments.create('testenv')
        session = self.murano.sessions.configure(environment.id)
        self.environments_id.append(environment.id)

        self.create_demo_service(environment.id, session.id,
                                 image_name=self.demo_image)
        self.murano.sessions.deploy(environment.id, session.id)

        time_start = time.time()
        gotten_environment = self.murano.environments.get(environment.id)

        while gotten_environment.status != 'ready':
            if time.time() - time_start > 1000:
                break
            gotten_environment = self.murano.environments.get(environment.id)

        deployments = self.murano.deployments.list(environment.id)
        self.assertEqual(deployments[0].state, 'success')

    def test_deploy_linux_telnet_service(self):
        environment = self.murano.environments.create('testenv')
        session = self.murano.sessions.configure(environment.id)
        self.environments_id.append(environment.id)

        self.create_linux_telnet(environment.id, session.id,
                                 image_name=self.linux_image)
        self.murano.sessions.deploy(environment.id, session.id)

        time_start = time.time()
        gotten_environment = self.murano.environments.get(environment.id)

        while gotten_environment.status != 'ready':
            if time.time() - time_start > 1800:
                break
            gotten_environment = self.murano.environments.get(environment.id)

        deployments = self.murano.deployments.list(environment.id)
        self.assertEqual(deployments[0].state, 'success')

    def test_deploy_linux_apache_service(self):
        environment = self.murano.environments.create('testenv')
        session = self.murano.sessions.configure(environment.id)
        self.environments_id.append(environment.id)

        self.create_linux_apache(environment.id, session.id,
                                 image_name=self.linux_image)
        self.murano.sessions.deploy(environment.id, session.id)

        time_start = time.time()
        gotten_environment = self.murano.environments.get(environment.id)

        while gotten_environment.status != 'ready':
            if time.time() - time_start > 1800:
                break
            gotten_environment = self.murano.environments.get(environment.id)

        deployments = self.murano.deployments.list(environment.id)
        self.assertEqual(deployments[0].state, 'success')

    def test_deploy_windows_ad_service(self):
        environment = self.murano.environments.create('testenv')
        session = self.murano.sessions.configure(environment.id)
        self.environments_id.append(environment.id)

        self.create_windows_active_directory(environment.id, session.id,
                                             image_name=self.windows_image)
        self.murano.sessions.deploy(environment.id, session.id)

        time_start = time.time()
        gotten_environment = self.murano.environments.get(environment.id)

        while gotten_environment.status != 'ready':
            if time.time() - time_start > 1800:
                break
            gotten_environment = self.murano.environments.get(environment.id)

        deployments = self.murano.deployments.list(environment.id)
        self.assertEqual(deployments[0].state, 'success')

    def test_deploy_windows_iis_service(self):
        environment = self.murano.environments.create('testenv')
        session = self.murano.sessions.configure(environment.id)
        self.environments_id.append(environment.id)

        self.create_windows_iis(environment.id, session.id,
                                image_name=self.windows_image)
        self.murano.sessions.deploy(environment.id, session.id)

        time_start = time.time()
        gotten_environment = self.murano.environments.get(environment.id)

        while gotten_environment.status != 'ready':
            if time.time() - time_start > 1800:
                break
            gotten_environment = self.murano.environments.get(environment.id)

        deployments = self.murano.deployments.list(environment.id)
        self.assertEqual(deployments[0].state, 'success')

    def test_deploy_windows_aspnet_service(self):
        environment = self.murano.environments.create('testenv')
        session = self.murano.sessions.configure(environment.id)
        self.environments_id.append(environment.id)

        self.create_windows_aspnet(environment.id, session.id,
                                   image_name=self.windows_image)
        self.murano.sessions.deploy(environment.id, session.id)

        time_start = time.time()
        gotten_environment = self.murano.environments.get(environment.id)

        while gotten_environment.status != 'ready':
            if time.time() - time_start > 1800:
                break
            gotten_environment = self.murano.environments.get(environment.id)

        deployments = self.murano.deployments.list(environment.id)
        self.assertEqual(deployments[0].state, 'success')

    def test_deploy_windows_iis_farm_service(self):
        environment = self.murano.environments.create('testenv')
        session = self.murano.sessions.configure(environment.id)
        self.environments_id.append(environment.id)

        self.create_windows_iis_farm(environment.id, session.id,
                                     image_name=self.windows_image)
        self.murano.sessions.deploy(environment.id, session.id)

        time_start = time.time()
        gotten_environment = self.murano.environments.get(environment.id)

        while gotten_environment.status != 'ready':
            if time.time() - time_start > 1800:
                break
            gotten_environment = self.murano.environments.get(environment.id)

        deployments = self.murano.deployments.list(environment.id)
        self.assertEqual(deployments[0].state, 'success')

    def test_deploy_windows_aspnet_farm_service(self):
        environment = self.murano.environments.create('testenv')
        session = self.murano.sessions.configure(environment.id)
        self.environments_id.append(environment.id)

        self.create_windows_aspnet_farm(environment.id, session.id,
                                        image_name=self.windows_image)
        self.murano.sessions.deploy(environment.id, session.id)

        time_start = time.time()
        gotten_environment = self.murano.environments.get(environment.id)

        while gotten_environment.status != 'ready':
            if time.time() - time_start > 1800:
                break
            gotten_environment = self.murano.environments.get(environment.id)

        deployments = self.murano.deployments.list(environment.id)
        self.assertEqual(deployments[0].state, 'success')

    def test_deploy_windows_sql_service(self):
        environment = self.murano.environments.create('testenv')
        session = self.murano.sessions.configure(environment.id)
        self.environments_id.append(environment.id)

        self.create_windows_sql(environment.id, session.id,
                                image_name=self.windows_image)
        self.murano.sessions.deploy(environment.id, session.id)

        time_start = time.time()
        gotten_environment = self.murano.environments.get(environment.id)

        while gotten_environment.status != 'ready':
            if time.time() - time_start > 1800:
                break
            gotten_environment = self.murano.environments.get(environment.id)

        deployments = self.murano.deployments.list(environment.id)
        self.assertEqual(deployments[0].state, 'success')

    def test_deploy_windows_sql_cluster_service(self):
        environment = self.murano.environments.create('testenv')
        session = self.murano.sessions.configure(environment.id)
        self.environments_id.append(environment.id)

        self.create_windows_active_directory(environment.id, session.id,
                                             image_name=self.windows_image)
        self.create_windows_sql_cluster(environment.id, session.id,
                                        domain_name="ad.local",
                                        image_name=self.windows_image)
        self.murano.sessions.deploy(environment.id, session.id)

        time_start = time.time()
        gotten_environment = self.murano.environments.get(environment.id)

        while gotten_environment.status != 'ready':
            if time.time() - time_start > 3000:
                break
            gotten_environment = self.murano.environments.get(environment.id)

        deployments = self.murano.deployments.list(environment.id)
        self.assertEqual(deployments[0].state, 'success')


class MuranoMetadata(MuranoBase):

    def test_get_list_of_availiable_services(self):
        services_list = self.murano_repo.metadata_admin.list_services()
        self.assertTrue(isinstance(services_list, list))

    def test_get_service_ui_file(self):
        files = self.murano_repo.metadata_admin.get_service_files(
            'ui', 'demoService')
        ui_files = self.transform_returned_list_of_files(files)
        self.assertIn('Demo.yaml', ui_files)

    def test_get_service_workflows(self):
        files = self.murano_repo.metadata_admin.get_service_files(
            'workflows', 'demoService')
        workflows = self.transform_returned_list_of_files(files)
        self.assertIn('Demo.xml', workflows)

    def test_get_service_heat_template(self):
        files = self.murano_repo.metadata_admin.get_service_files(
            'heat', 'demoService')
        heat_templates = self.transform_returned_list_of_files(files)
        self.assertIn('DemoSecurity.template', heat_templates)

    def test_get_service_agent_template(self):
        files = self.murano_repo.metadata_admin.get_service_files(
            'agent', 'demoService')
        agent_templates = self.transform_returned_list_of_files(files)
        self.assertIn('Demo.template', agent_templates)

    def test_get_service_info(self):
        service_info = self.murano_repo.metadata_admin.get_service_info(
            'activeDirectory')
        self.assertIn('<strong> The Active Directory Service </strong>',
                      service_info['description'])
        self.assertIn('Mirantis Inc.', service_info['author'])
        self.assertIn('Active Directory', service_info['service_display_name'])
        self.assertIn('activeDirectory', service_info['full_service_name'])

    def test_upload_delete_service(self):
        __location = os.path.realpath(os.path.join(os.getcwd(),
                                                   os.path.dirname(__file__)))
        service = os.path.join(__location, 'myService.tar.gz')
        file_ = open(service, 'rb')
        self.murano_repo.metadata_admin.upload_service(file_)
        list_of_services = self.murano_repo.metadata_admin.list_services()
        services = self.form_service_list(list_of_services)
        self.assertIn('myService', services)

        self.murano_repo.metadata_admin.delete_service('myService')
        list_of_services = self.murano_repo.metadata_admin.list_services()
        services = self.form_service_list(list_of_services)
        self.assertNotIn('myService', services)

    def test_toggle_active(self):
        self.murano_repo.metadata_admin.toggle_enabled('demoService')
        service_info = self.murano_repo.metadata_admin.get_service_info(
            'demoService')
        self.assertEqual(False, service_info['enabled'])

        self.murano_repo.metadata_admin.toggle_enabled('demoService')
        service_info = self.murano_repo.metadata_admin.get_service_info(
            'demoService')
        self.assertEqual(True, service_info['enabled'])

    def test_get_list_ui(self):
        list_ui = self.murano_repo.metadata_admin.list_ui()

        self.assertGreater(len(list_ui), 0)

        self.assertIn('Demo.yaml', list_ui['ui'])
        self.assertIn('ActiveDirectory.yaml', list_ui['ui'])

    def test_get_list_agent(self):
        list_agent = self.murano_repo.metadata_admin.list_agent()

        self.assertGreater(len(list_agent), 0)

        self.assertIn('JoinDomain.template', list_agent['agent'])
        self.assertIn('InstallIIS.template', list_agent['agent'])

    def test_get_list_heat(self):
        list_heat = self.murano_repo.metadata_admin.list_heat()

        self.assertGreater(len(list_heat), 0)

        self.assertIn('DefaultSecurity.template', list_heat['heat'])
        self.assertIn('FloatingIP.template', list_heat['heat'])

    def test_get_list_scripts(self):
        list_scripts = self.murano_repo.metadata_admin.list_scripts()

        self.assertGreater(len(list_scripts), 0)

        self.assertIn('Join-Domain.ps1', list_scripts['scripts'])
        self.assertIn('InstallIIS.ps1', list_scripts['scripts'])

    def test_get_list_workflows(self):
        list_workflows = self.murano_repo.metadata_admin.list_workflows()

        self.assertGreater(len(list_workflows), 0)

        self.assertIn('AD.xml', list_workflows['workflows'])
        self.assertIn('Networking.xml', list_workflows['workflows'])

    def test_get_list_manifests(self):
        list_manifests = self.murano_repo.metadata_admin.list_manifests()

        self.assertGreater(len(list_manifests), 0)

        self.assertIn('aspNetApp-manifest.yaml', list_manifests['manifests'])
        self.assertIn('webServer-manifest.yaml', list_manifests['manifests'])

    def test_upload_delete_file(self):
        __location = os.path.realpath(os.path.join(os.getcwd(),
                                                   os.path.dirname(__file__)))
        service_file = os.path.join(__location, 'myScript.ps1')
        file_ = open(service_file, 'rb')

        self.murano_repo.metadata_admin.upload_file(
            'scripts', file_, 'myScript.ps1')
        list_scripts = self.murano_repo.metadata_admin.list_scripts()
        self.assertIn('myScript.ps1', list_scripts['scripts'])

        self.murano_repo.metadata_admin.delete('scripts', 'myScript.ps1')
        list_scripts = self.murano_repo.metadata_admin.list_scripts()
        self.assertNotIn('myScript.ps1', list_scripts['scripts'])

    def test_upload_and_delete_file_from_the_service(self):
        __location = os.path.realpath(os.path.join(os.getcwd(),
                                                   os.path.dirname(__file__)))
        service_file = os.path.join(__location, 'myScript.ps1')
        file_ = open(service_file, 'rb')

        self.murano_repo.metadata_admin.upload_file_to_service(
            'scripts', file_, 'myScript.ps1', 'demoService')
        scripts = self.murano_repo.metadata_admin.get_service_files(
            'scripts', 'demoService')
        files = self.transform_returned_list_of_files(scripts)
        self.assertIn('myScript.ps1', files)

        self.murano_repo.metadata_admin.delete_from_service(
            'scripts', 'myScript.ps1', 'demoService')
        scripts = self.murano_repo.metadata_admin.get_service_files(
            'scripts', 'demoService')
        files = self.transform_returned_list_of_files(scripts)
        self.assertNotIn('myScript.ps1', files)
