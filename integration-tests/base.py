from v1.murano_client import murano_client as Client
import etc.config as cfg
import testtools
import testresources


class MuranoBase(testtools.TestCase, testtools.testcase.WithAttributes,
                 testresources.ResourcedTestCase):

    @classmethod
    def setUpClass(cls):
        super(MuranoBase, cls).setUpClass()
        cls.client = Client(user=cfg.murano.user, password=cfg.murano.password,
                            tenant=cfg.murano.tenant,
                            auth_url=cfg.murano.auth_url,
                            base_url=cfg.murano.murano_url)
        cls.environments = []

    def tearDown(self):
        super(MuranoBase, self).tearDown()
        for env in self.environments:
            try:
                self.client.delete_environment(env)
            except Exception:
                pass

