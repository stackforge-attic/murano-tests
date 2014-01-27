import testtools
import ConfigParser
import random

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
        cls.keypair = cfg.common.keypair_name
        cls.asp_git_repository = cfg.common.asp_git_repository

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

    def delete_environment(self, env_name):
        self.driver.find_element_by_link_text('Environments').click()
        self.click_on_more(env_name)
        self.click_on_delete(env_name)
        self.confirm_deletion()

    def edit_environment(self, old_name, new_name):
        self.click_on_more(old_name)
        self.click_on_edit(old_name)
        self.find_clean_send(by.By.ID, 'id_name', new_name)
        save = self.elements.get('button', 'InputSubmit')
        self.driver.find_element_by_xpath(save).click()

    def click_on_more(self, env_name):
        element_id = self.get_element_id(env_name)
        self.driver.find_element_by_xpath(
            ".//*[@id='murano__row__%s']/td[4]/div/a[2]" % element_id).click()

    def click_on_edit(self, env_name):
        element_id = self.get_element_id(env_name)
        self.driver.find_element_by_id(
            "murano__row_%s__action_edit" % element_id).click()

    def click_on_delete(self, env_name):
        element_id = self.get_element_id(env_name)
        self.driver.find_element_by_id(
            "murano__row_%s__action_delete" % element_id).click()

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

    def env_to_service(self, env_name):
        element_id = self.get_element_id(env_name)
        self.driver.find_element_by_id("murano__row_%s__action_show"
                                       % element_id).click()

    def create_demo_service(self, service_name):
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

    def create_linux_telnet(self, service_name):
        self.driver.find_element_by_id('services__action_CreateService').click()

        self.select_from_list('service_choice-service', 'Linux Telnet')
        Next = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(Next).click()

        self.find_clean_send(by.By.ID, 'id_linuxTelnetService-0-name',
                             service_name)
        Next = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(Next).click()

        self.select_from_list('linuxTelnetService-1-osImage',
                              self.linux_image)
        self.select_from_list('linuxTelnetService-1-keyPair',
                              self.keypair)
        Next = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(Next).click()

    def create_linux_apache(self, service_name):
        self.driver.find_element_by_id('services__action_CreateService').click()

        self.select_from_list('service_choice-service', 'Linux Apache')
        Next = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(Next).click()

        self.find_clean_send(by.By.ID, 'id_linuxApacheService-0-name',
                             service_name)
        Next = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(Next).click()
        self.select_from_list('linuxApacheService-1-osImage',
                              self.linux_image)
        self.select_from_list('linuxApacheService-1-keyPair',
                              self.keypair)
        Next = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(Next).click()

    def create_ad_service(self, service_name):
        self.driver.find_element_by_id('services__action_CreateService').click()

        self.select_from_list('service_choice-service', 'Active Directory')
        Next = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(Next).click()

        self.find_clean_send(
            by.By.ID, 'id_activeDirectory-0-name', service_name)
        self.find_clean_send(
            by.By.ID, 'id_activeDirectory-0-adminPassword', 'P@ssw0rd')
        self.find_clean_send(
            by.By.ID, 'id_activeDirectory-0-adminPassword-clone', 'P@ssw0rd')
        self.find_clean_send(
            by.By.ID, 'id_activeDirectory-0-recoveryPassword', 'P@ssw0rd')
        self.find_clean_send(
            by.By.ID, 'id_activeDirectory-0-recoveryPassword-clone', 'P@ssw0rd')
        Next = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(Next).click()

        self.select_from_list('activeDirectory-1-osImage', self.windows_image)
        Next = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(Next).click()

    def create_iis_service(self, service_name):
        self.driver.find_element_by_id('services__action_CreateService').click()

        self.select_from_list(
            'service_choice-service', 'Internet Information Services')
        Next = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(Next).click()

        self.find_clean_send(by.By.ID, 'id_webServer-0-name', service_name)
        self.find_clean_send(
            by.By.ID, 'id_webServer-0-adminPassword', 'P@ssw0rd')
        self.find_clean_send(
            by.By.ID, 'id_webServer-0-adminPassword-clone', 'P@ssw0rd')
        Next = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(Next).click()

        self.select_from_list('webServer-1-osImage', self.windows_image)
        Next = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(Next).click()

    def create_asp_service(self, service_name):
        self.driver.find_element_by_id('services__action_CreateService').click()

        self.select_from_list('service_choice-service', 'ASP.NET Application')
        Next = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(Next).click()

        self.find_clean_send(by.By.ID, 'id_aspNetApp-0-name', service_name)
        self.find_clean_send(
            by.By.ID, 'id_aspNetApp-0-adminPassword', 'P@ssw0rd')
        self.find_clean_send(
            by.By.ID, 'id_aspNetApp-0-adminPassword-clone', 'P@ssw0rd')
        self.find_clean_send(
            by.By.ID, 'id_aspNetApp-0-repository', self.asp_git_repository)
        Next = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(Next).click()

        self.select_from_list('aspNetApp-1-osImage', self.windows_image)
        Next = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(Next).click()

    def create_iisfarm_service(self, service_name):
        self.driver.find_element_by_id('services__action_CreateService').click()

        self.select_from_list(
            'service_choice-service', 'Internet Information Services Web Farm')
        Next = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(Next).click()

        self.find_clean_send(by.By.ID, 'id_webServerFarm-0-name', service_name)
        self.find_clean_send(
            by.By.ID, 'id_webServerFarm-0-adminPassword', 'P@ssw0rd')
        self.find_clean_send(
            by.By.ID, 'id_webServerFarm-0-adminPassword-clone', 'P@ssw0rd')
        Next = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(Next).click()

        self.select_from_list('webServerFarm-1-osImage', self.windows_image)
        Next = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(Next).click()

    def create_aspfarm_service(self, service_name):
        self.driver.find_element_by_id('services__action_CreateService').click()

        self.select_from_list(
            'service_choice-service', 'ASP.NET Application Web Farm')
        Next = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(Next).click()

        self.find_clean_send(by.By.ID, 'id_aspNetAppFarm-0-name', service_name)
        self.find_clean_send(
            by.By.ID, 'id_aspNetAppFarm-0-adminPassword', 'P@ssw0rd')
        self.find_clean_send(
            by.By.ID, 'id_aspNetAppFarm-0-adminPassword-clone', 'P@ssw0rd')
        self.find_clean_send(
            by.By.ID, 'id_aspNetAppFarm-0-repository', self.asp_git_repository)
        Next = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(Next).click()

        self.select_from_list('aspNetAppFarm-1-osImage', self.windows_image)
        Next = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(Next).click()

    def create_mssql_service(self, service_name):
        self.driver.find_element_by_id('services__action_CreateService').click()

        self.select_from_list('service_choice-service', 'MS SQL Server')
        Next = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(Next).click()

        self.find_clean_send(by.By.ID, 'id_msSqlServer-0-name', service_name)
        self.find_clean_send(
            by.By.ID, 'id_msSqlServer-0-adminPassword', 'P@ssw0rd')
        self.find_clean_send(
            by.By.ID, 'id_msSqlServer-0-adminPassword-clone', 'P@ssw0rd')
        self.find_clean_send(
            by.By.ID, 'id_msSqlServer-0-saPassword', 'P@ssw0rd')
        self.find_clean_send(
            by.By.ID, 'id_msSqlServer-0-saPassword-clone', 'P@ssw0rd')
        Next = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(Next).click()

        self.select_from_list('msSqlServer-1-osImage', self.windows_image)
        Next = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(Next).click()

    def create_sql_cluster_service(self, service_name, domain_name):
        self.driver.find_element_by_id('services__action_CreateService').click()

        self.select_from_list('service_choice-service', 'MS SQL Server Cluster')
        Next = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(Next).click()

        self.find_clean_send(
            by.By.ID, 'id_msSqlClusterServer-0-name', service_name)
        self.find_clean_send(
            by.By.ID, 'id_msSqlClusterServer-0-adminPassword', 'P@ssw0rd')
        self.find_clean_send(
            by.By.ID, 'id_msSqlClusterServer-0-adminPassword-clone', 'P@ssw0rd')
        self.select_from_list('msSqlClusterServer-0-domain', domain_name)
        self.find_clean_send(
            by.By.ID, 'id_msSqlClusterServer-0-saPassword', 'P@ssw0rd')
        self.find_clean_send(
            by.By.ID, 'id_msSqlClusterServer-0-saPassword-clone', 'P@ssw0rd')
        Next = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(Next).click()

        self.find_clean_send(
            by.By.ID, 'id_msSqlClusterServer-1-clusterIp', '1.1.1.1')
        self.find_clean_send(
            by.By.ID, 'id_msSqlClusterServer-1-clusterName', 'cluster')
        self.find_clean_send(
            by.By.ID, 'id_msSqlClusterServer-1-agGroupName', 'ag-name')
        self.find_clean_send(
            by.By.ID, 'id_msSqlClusterServer-1-agListenerName', 'listener_name')
        self.find_clean_send(
            by.By.ID, 'id_msSqlClusterServer-1-agListenerIP', 'listener_name')
        self.find_clean_send(
            by.By.ID, 'id_msSqlClusterServer-1-sqlServiceUserName', 'admin')
        self.find_clean_send(
            by.By.ID, 'id_msSqlClusterServer-1-sqlServicePassword', 'P@ssw0rd')
        self.find_clean_send(
            by.By.ID, 'id_msSqlClusterServer-1-sqlServicePassword-clone',
            'P@ssw0rd')
        Next = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(Next).click()

        cluster_ip = self.get_env_subnet()
        self.find_clean_send(
            by.By.ID, 'id_msSqlClusterServer-1-clusterIp', cluster_ip)
        listener_ip = self.get_env_subnet()
        self.find_clean_send(
            by.By.ID, 'id_msSqlClusterServer-1-agListenerIP', listener_ip)
        Next = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(Next).click()

        self.find_clean_send(
            by.By.ID, 'id_msSqlClusterServer-2-databases', 'testbase')
        Next = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(Next).click()

        self.select_from_list(
            'msSqlClusterServer-3-osImage', self.windows_image)
        Next = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(Next).click()

    def get_element_id(self, element_name):
        path = self.driver.find_element_by_link_text(
            element_name).get_attribute("href")
        return path.split('/')[-2]

    def delete_service(self, service_name):
        id = self.get_element_id(service_name)
        self.driver.find_element_by_id('services__row_%s__action_delete'
                                       % id).click()
        self.driver.find_element_by_link_text('Delete Service').click()

    def get_env_subnet(self):
        help_text = self.driver.find_element_by_xpath(
            "(.//span[@class = 'help-inline'])[1]").text
        subnet = help_text.split('.')[-2]
        num = random.randint(0, 255)
        return '10.0.%s.%d' % (subnet, num)