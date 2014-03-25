import testtools
import testresources
import requests


class MuranoRepository(testtools.TestCase, testtools.testcase.WithAttributes,
                       testresources.ResourcedTestCase):
    @classmethod
    def setUpClass(cls):
        super(MuranoRepository, cls).setUpClass()

        cls.url = "http://muranorepositoryapi.apiary-mock.com/v2"

    def get_list_packages(self):
        return requests.get('{0}{1}'.format(self.url, '/catalog/packages'))

    def get_package(self, id):
        return requests.get('{0}{1}'.format(self.url + '/catalog/packages/',
                                            id))

    def update_package(self, id):
        post_body = {
            "description":
                "This is full description of The Active Directory Service"
        }
        return requests.patch('{0}{1}'.format(self.url + '/catalog/packages/',
                                              id), data=post_body)

    def delete_package(self, id):
        return requests.delete('{0}{1}'.format(self.url + '/catalog/packages/',
                                               id))

    def download_package(self, id):
        return requests.get('{0}{1}'.format(self.url + '/catalog/packages/',
                                            id + '/download'))

    def get_ui_definition(self, id):
        return requests.get(('{0}{1}'.format(self.url + '/catalog/packages/',
                                             id + '/ui')))

    def get_logo(self, id):
        return requests.get(('{0}{1}'.format(self.url + '/catalog/packages/',
                                             id + '/logo')))

    def list_categories(self):
        return requests.get('{0}{1}'.format(self.url,
                                            '/catalog/packages/categories'))


class MuranoRepositoryTests(MuranoRepository):
    def test_get_list_packages(self):
        resp = self.get_list_packages()

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(isinstance(resp.json(), list))

    def test_get_package(self):
        package = self.get_list_packages().json()[0]

        resp = self.get_package(package['id'])

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), package)

    def test_update_package(self):
        package = self.get_list_packages().json()[0]
        resp = self.update_package(package['id'])

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['description'],
                         " ".join(resp.request.body.split('=')[1].split('+')))

    def test_delete_package(self):
        package = self.get_list_packages().json()[0]

        resp = self.delete_package(package['id'])

        self.assertEqual(resp.status_code, 200)

    def test_download_package(self):
        package = self.get_list_packages().json()[0]

        resp = self.download_package(package['id'])

        self.assertEqual(resp.status_code, 200)

    def test_get_ui_definition(self):
        package = self.get_list_packages().json()[0]

        resp = self.get_ui_definition(package['id'])

        self.assertEqual(resp.status_code, 200)

    def test_get_logo(self):
        package = self.get_list_packages().json()[0]

        resp = self.get_logo(package['id'])

        self.assertEqual(resp.status_code, 200)

    def test_list_categories(self):
        resp = self.list_categories()

        self.assertEqual(resp.status_code, 200)
        #Need to additional assertion after fix
        #https://bugs.launchpad.net/murano/+bug/1297262