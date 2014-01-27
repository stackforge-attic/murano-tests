import testtools
import ConfigParser

from selenium import webdriver
import selenium.webdriver.common.by as by
import config.config as cfg
from selenium.common.exceptions import NoSuchElementException

from keystoneclient.v2_0 import client as ksclient
from muranoclient.client import Client as mclient


class UITestCase(testtools.TestCase):


    @classmethod
    def setUpClass(cls):

        super(UITestCase, cls).setUpClass()

        keystone_client = ksclient.Client(username=cfg.common.user,
                                          password=cfg.common.password,
                                          tenant_name=cfg.common.tenant,
                                          auth_url=cfg.common.keystone_url)

        cls.murano_client = mclient('1', endpoint=cfg.common.murano_url,
                                    token=keystone_client.auth_token)

        cls.demo_image = cfg.common.demo_image
        cls.linux_image = cfg.common.linux_image
        cls.windows_image = cfg.common.windows_image

        cls.elements = ConfigParser.RawConfigParser()
        cls.elements.read('common.ini')

    def setUp(self):
        super(UITestCase, self).setUp()
        self.driver = webdriver.Firefox()
        self.driver.get(cfg.common.horizon_url + '/')
        self.driver.implicitly_wait(5)

    def tearDown(self):
        super(UITestCase, self).tearDown()
        self.driver.quit()

        for env in self.murano_client.environments.list():
            self.murano_client.environments.delete(env.id)

    def log_in(self):
        self.find_clean_send(by.By.ID, 'id_username', cfg.common.user)
        self.find_clean_send(by.By.ID, 'id_password', cfg.common.password)
        sign_in = self.elements.get('button', 'ButtonSubmit')
        self.driver.find_element_by_xpath(sign_in).click()
        self.navigate_to_environments()

    def find_clean_send(self, by_find, find_element, send):
        self.driver.find_element(by=by_find, value=find_element).clear()
        self.driver.find_element(by=by_find, value=find_element).send_keys(send)

    def confirm_deletion(self):
        confirm_deletion = self.elements.get('button', 'ConfirmDeletion')
        self.driver.find_element_by_xpath(confirm_deletion).click()

    def create_environment(self, env_name):
        self.driver.find_element_by_id(
            'murano__action_CreateEnvironment').click()
        self.find_clean_send(by.By.ID, 'id_name', env_name)
        create = self.elements.get('button', 'InputSubmit')
        self.driver.find_element_by_xpath(create).click()

    def delete_environment(self):
        self.driver.find_element_by_link_text('Environments').click()
        self.click_on_more()
        self.click_on_delete()
        self.confirm_deletion()

    def edit_environment(self, new_name):
        self.click_on_more()
        self.click_on_edit()
        self.find_clean_send(by.By.ID, 'id_name', new_name)
        save = self.elements.get('button', 'InputSubmit')
        self.driver.find_element_by_xpath(save).click()

    def click_on_more(self):
        more = self.elements.get('button', 'More')
        self.driver.find_element_by_xpath(more).click()

    def click_on_edit(self):
        self.driver.find_element_by_link_text('Edit Environment').click()

    def click_on_delete(self):
        delete = self.elements.get('button', 'ButtonSubmit')
        self.driver.find_element_by_xpath(delete).click()

    def navigate_to_environments(self):
        self.driver.find_element_by_link_text('Murano').click()
        self.driver.find_element_by_link_text('Environments').click()

    def navigate_to_images(self):
        self.driver.find_element_by_link_text('Murano').click()
        self.driver.find_element_by_link_text('Images').click()

    def select_from_list(self, list_name, value):
        self.driver.find_element_by_xpath(
            "//select[@name='%s']/option[text()='%s']" %
            (list_name, value)).click()

    def check_element_on_page(self, method, value):
        try:
            self.driver.find_element(method, value)
        except NoSuchElementException:
            return False
        return True

    def create_demo_service(self, service_name):
        self.driver.find_element_by_link_text('Services').click()
        self.driver.find_element_by_id('services__action_CreateService').click()

        self.select_from_list('service_choice-service', 'Demo Service')
        Next = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(Next).click()

        self.find_clean_send(by.By.ID, 'id_demoService-0-name', service_name)
        Next = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(Next).click()

        self.select_from_list('demoService-1-osImage', self.demo_image)
        Next = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(Next).click()
<<<<<<< HEAD
=======

    def delete_service(self, service_name):
        service = self.driver.find_element_by_link_text(service_name)
        id = service.get_attribute("href").split('/')[-2]
        self.driver.find_element_by_id('services__row_%s__action_delete'
                                       % id).click()
        self.driver.find_element_by_link_text('Delete Service').click()
>>>>>>> f3efa1b... Add 'create demo service' dashboard test
