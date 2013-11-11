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

config = ConfigParser.RawConfigParser()
config.read('config.ini')
user = config.get('keystone', 'user')
password = config.get('keystone', 'password')
tenant = config.get('keystone', 'tenant')
keystone_url = config.get('keystone', 'url')
keystone_client = ksclient.Client(username=user, password=password,
                                  tenant_name=tenant, auth_url=keystone_url)
token = str(keystone_client.auth_token)

class TestMeta(FunkLoadTestCase):

    def setUp(self):
        self.clearHeaders()
        self.url = self.conf_get('main', 'meta_url')
        self.setHeader('X-Auth-Token', token)

    def generate_num(self):
        p=""
        for i in xrange(10):
            p += str(random.randint(0, 10))
        return p

    def test_get_ui_definitions(self):
        url = self.url + "/" + "v1/client/ui"
        resp = self.get(url, description="Get UI definitions")
        assert resp.code == 200

    def test_get_conductor_metadata(self):
        url = self.url + "/" + "v1/client/conductor"
        resp = self.get(url, description="Get conductor metadata")
        assert resp.code == 200

    def test_get_list_metadata_objects_workflows(self):
        url = self.url + "/" + "v1/admin/workflows"
        resp = self.get(url, description="Get list metadata objects(workflows)")
        assert resp.code == 200

    def test_get_list_metadata_objects_ui(self):
        url = self.url + "/" + "v1/admin/ui"
        resp = self.get(url, description="Get list metadata objects(ui)")
        assert resp.code == 200

    def test_get_list_metadata_objects_heat(self):
        url = self.url + "/" + "v1/admin/heat"
        resp = self.get(url, description="Get list metadata objects(heat)")
        assert resp.code == 200

    def test_get_list_metadata_objects_agent(self):
        url = self.url + "/" + "v1/admin/agent"
        resp = self.get(url, description="Get list metadata objects(agent)")
        assert resp.code == 200

    def test_get_list_metadata_objects_scripts(self):
        url = self.url + "/" + "v1/admin/scripts"
        resp = self.get(url, description="Get list metadata objects(scripts)")
        assert resp.code == 200

    def test_create_and_delete_dir(self):
        typ = ['ui', 'workflows', 'agent', 'heat', 'scripts']
        random.shuffle(typ)
        url = self.url + "/v1/admin/" + typ[1] + "/" + "folder" +\
              self.generate_num()
        resp = self.put(url, description="Create folder")
        response = self.delete(url, description="Delete folder")
        assert resp.code == 200
        assert response.code == 200

    def mix_for_load_testing(self):
        k = random.randint(0,100)
        if k < 12:
            return self.test_get_ui_definitions()
        elif k < 24:
            return self.test_get_conductor_metadata()
        elif k < 36:
            return self.test_get_list_metadata_objects_workflows()
        elif k < 48:
            return self.test_get_list_metadata_objects_ui()
        elif k < 60:
            return self.test_get_list_metadata_objects_heat()
        elif k < 72:
            return self.test_get_list_metadata_objects_agent()
        elif k < 84:
            return self.test_get_list_metadata_objects_scripts()
        elif k < 100:
            return self.test_create_and_delete_dir()


if __name__ == '__main__':
    unittest.main()
