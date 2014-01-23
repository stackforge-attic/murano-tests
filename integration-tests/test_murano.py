import sys
import os
sys.path.append(os.getcwd())
from base import MuranoBase


class MuranoEnvs(MuranoBase):

    def test_create_and_delete_environment(self):
        resp = self.client.create_environment('test')
        self.environments.append(resp.json()['id'])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['name'], 'test')
        env = self.client.get_list_environments().json()['environments'][0]['name']
        self.assertEqual(env, 'test')
        resp = self.client.delete_environment(resp.json()['id'])
        self.assertEqual(resp.status_code, 200)
