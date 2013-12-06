from tempest.api.murano import base
from tempest.test import attr


class SanityMuranoTest(base.MuranoTest):

    @attr(type='negative')
    def test_create_environment_wo_token(self):
        resp = self.create_environment_wo_token('test')
        assert resp.status_code == 401

    @attr(type='negative')
    def test_delete_environment_wo_token(self):
        _, env = self.create_environment('test')
        self.environments.append(env)
        resp = self.delete_environment_wo_token(env['id'])
        assert resp.status_code == 401
        self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_update_environment_wo_token(self):
        _, env = self.create_environment('test')
        self.environments.append(env)
        resp = self.update_environment_wo_token(env['id'], env['name'])
        assert resp.status_code == 401
        self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_create_session_wo_token(self):
        _, env = self.create_environment('test')
        self.environments.append(env)
        resp = self.create_session_wo_token(env['id'])
        assert resp.status_code == 401
        self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_delete_session_wo_token(self):
        _, env = self.create_environment('test')
        self.environments.append(env)
        _, sess = self.create_session(env['id'])
        resp = self.delete_session_wo_token(env['id'], sess['id'])
        assert resp.status_code == 401
        self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_create_service_wo_token(self):
        _, env = self.create_environment('test')
        self.environments.append(env)
        _, sess = self.create_session(env['id'])
        resp = self.create_service_wo_token(env['id'], sess['id'])
        assert resp.status_code == 401
        self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_delete_service_wo_token(self):
        _, env = self.create_environment('test')
        self.environments.append(env)
        _, sess = self.create_session(env['id'])
        _, serv = self.create_AD(env['id'], sess['id'])
        resp = self.delete_service_wo_token(env['id'], sess['id'], serv['id'])
        assert resp.status_code == 401
        self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_deploy_session_wo_token(self):
        _, env = self.create_environment('test')
        self.environments.append(env)
        _, sess = self.create_session(env['id'])
        resp = self.deploy_session_wo_token(env['id'], sess['id'])
        assert resp.status_code == 401
        self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_get_list_environments_wo_token(self):
        resp = self.get_list_environments_wo_token()
        assert resp.status_code == 401

    @attr(type='negative')
    def test_get_environment_wo_token(self):
        _, env = self.create_environment('test')
        self.environments.append(env)
        resp = self.get_environment_wo_token(env['id'])
        assert resp.status_code == 401
        self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_get_session_wo_token(self):
        _, env = self.create_environment('test')
        self.environments.append(env)
        _, sess = self.create_session(env['id'])
        resp = self.get_session_wo_token(env['id'], sess['id'])
        assert resp.status_code == 401
        self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_get_service_wo_token(self):
        _, env = self.create_environment('test')
        self.environments.append(env)
        _, sess = self.create_session(env['id'])
        _, serv = self.create_AD(env['id'], sess['id'])
        resp = self.get_service_wo_token(env['id'], sess['id'], serv['id'])
        assert resp.status_code == 401
        self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_get_list_services_wo_token(self):
        _, env = self.create_environment('test')
        self.environments.append(env)
        _, sess = self.create_session(env['id'])
        resp = self.get_list_services_wo_token(env['id'], sess['id'])
        assert resp.status_code == 401
        self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))
