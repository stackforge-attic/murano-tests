import requests
import json
from keystoneclient.v2_0 import client as ksclient

class Client(object):
    def __init__(self, user, password, tenant, auth_url, base_url):
        self.auth = ksclient.Client(username=user, password=password,
                                    tenant_name=tenant, auth_url=auth_url)
        self.headers = {'X-Auth-Token': self.auth.auth_token}
        if base_url[-1] == '/':
            self.url = base_url
        else:
            self.url = base_url + '/'
        self.TYPE = 'json'

    def get(self, path, headers=None, TYPE=None):
        if headers is None:
            headers = self.headers
        if TYPE is None:
            headers.update({'Content-Type': 'application/%s' % self.TYPE})
        else:
            headers.update({'Content-Type': self.TYPE})
        url = self.url + path
        resp = requests.get(url, headers=headers)
        return resp

    def delete(self, path, headers=None, TYPE=None):
        if headers is None:
            headers = self.headers
        if TYPE is None:
            headers.update({'Content-Type': 'application/%s' % self.TYPE})
        else:
            headers.update({'Content-Type': self.TYPE})
        url = self.url + path
        resp = requests.delete(url, headers=headers)
        return resp

    def post(self, path, body=None, files=None, headers=None, TYPE=None):
        if headers is None:
            headers = self.headers
        if TYPE is None:
            headers.update({'Content-Type': 'application/%s' % self.TYPE})
        else:
            headers.update({'Content-Type': self.TYPE})
        url = self.url + path
        resp = requests.post(url, data=body, files=files, headers=headers)
        return resp

    def put(self, path, body=None, files=None, headers=None, TYPE=None):
        if headers is None:
            headers = self.headers
        if TYPE is None:
            headers.update({'Content-Type': 'application/%s' % self.TYPE})
        else:
            headers.update({'Content-Type': self.TYPE})
        url = self.url + path
        resp = requests.put(url, data=body, files=files, headers=headers)
        return resp

class murano_client(Client):

    def __init__(self, user, password, tenant, auth_url, base_url):
        super(murano_client, self).__init__(user, password, tenant, auth_url,
                                            base_url)

    def create_environment(self, name):
        post_body = {'name': name}
        post_body = json.dumps(post_body)
        resp = self.post('environments', body=post_body, headers=self.headers)
        return resp

    def delete_environment(self, environment_id):
        resp = self.delete('environments/%s' % environment_id,
                           headers=self.headers)
        return resp

    def get_list_environments(self):
        resp = self.get('environments', headers=self.headers)
        return resp

