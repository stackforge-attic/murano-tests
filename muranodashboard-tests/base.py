import datetime
import os
import random

import ConfigParser
import json
import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import selenium.webdriver.common.by as by
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import testtools
import time

from keystoneclient.v2_0 import client as ksclient
from muranoclient.client import Client as mclient
from glanceclient import Client as gclient
import config.config as cfg

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())


class ImageException(Exception):
    message = "Image doesn't exist"

    def __init__(self, type):
        self._error_string = (self.message + '\nDetails: {0} image is '
                                             'not found,'.format(type))

    def __str__(self):
        return self._error_string


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

        glance_endpoint = keystone_client.service_catalog.url_for(
            service_type='image', endpoint_type='publicURL')
        glance = gclient('1', endpoint=glance_endpoint,
                         token=keystone_client.auth_token)

        image_list = []
        for i in glance.images.list():
            image_list.append(i)

        cls.demo_image = cls.get_image_name('demo', image_list)
        cls.linux_image = cls.get_image_name('linux', image_list)
        cls.windows_image = cls.get_image_name('windows', image_list)
        cls.keypair = cfg.common.keypair_name
        cls.asp_git_repository = cfg.common.asp_git_repository
        cls.tomcat_repository = cfg.common.tomcat_repository

        cls.elements = ConfigParser.RawConfigParser()
        cls.elements.read('common.ini')
        cls.logger = logging.getLogger(__name__)

    def setUp(self):
        super(UITestCase, self).setUp()

        self.driver = webdriver.Remote(
            command_executor=cfg.common.selenium_server,
            desired_capabilities=DesiredCapabilities.FIREFOX)

        self.driver.get(cfg.common.horizon_url + '/')
        self.driver.implicitly_wait(30)
        self.log_in()

    def tearDown(self):
        super(UITestCase, self).tearDown()
        self.addOnException(self.take_screenshot(self._testMethodName))
        self.driver.quit()

        for env in self.murano_client.environments.list():
            self.murano_client.environments.delete(env.id)

    def take_screenshot(self, test_name):
        screenshot_dir = './screenshots'
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        date = datetime.datetime.now().strftime('%H%M%S')
        filename = '{0}/{1}-{2}.png'.format(screenshot_dir, test_name, date)
        self.driver.get_screenshot_as_file(filename)
        log.debug("\nScreenshot {0} was saved".format(filename))

    @classmethod
    def get_image_name(cls, type_of_image, list_of_images):
        for i in list_of_images:
            if 'murano_image_info' in i.properties.keys():
                if type_of_image in json.loads(
                        i.properties['murano_image_info'])['type']:
                    return json.loads(i.properties[
                        'murano_image_info'])['title']
        raise ImageException(type_of_image)

    def log_in(self):
        self.fill_field(by.By.ID, 'id_username', cfg.common.user)
        self.fill_field(by.By.ID, 'id_password', cfg.common.password)
        sign_in = self.elements.get('button', 'ButtonSubmit')
        self.driver.find_element_by_xpath(sign_in).click()
        self.driver.find_element_by_link_text('Murano').click()

    def fill_field(self, by_find, field, value):
        self.driver.find_element(by=by_find, value=field).clear()
        self.driver.find_element(by=by_find, value=field).send_keys(value)

    def confirm_deletion(self):
        confirm_deletion = self.elements.get('button', 'ConfirmDeletion')
        self.driver.find_element_by_xpath(confirm_deletion).click()

    def create_environment(self, env_name):
        self.driver.find_element_by_id(
            'murano__action_CreateEnvironment').click()
        self.fill_field(by.By.ID, 'id_name', env_name)
        create = self.elements.get('button', 'InputSubmit')
        self.driver.find_element_by_xpath(create).click()

    def delete_environment(self, env_name):
        self.driver.find_element_by_link_text('Environments').click()
        self.click_on_more(env_name)
        self.select_action_for_environment(env_name, 'delete')
        self.confirm_deletion()

    def edit_environment(self, old_name, new_name):
        self.click_on_more(old_name)
        self.select_action_for_environment(old_name, 'edit')
        self.fill_field(by.By.ID, 'id_name', new_name)
        save = self.elements.get('button', 'InputSubmit')
        self.driver.find_element_by_xpath(save).click()

    def click_on_more(self, env_name):
        element_id = self.get_element_id(env_name)
        self.driver.find_element_by_xpath(
            ".//*[@id='murano__row__{0}']/td[4]/div/a[2]".
            format(element_id)).click()

    def select_action_for_environment(self, env_name, action):
        element_id = self.get_element_id(env_name)
        self.driver.find_element_by_id(
            "murano__row_{0}__action_{1}".format(element_id, action)).click()

    def navigate_to(self, link):
        self.driver.find_element_by_link_text('Murano').click()
        self.driver.find_element_by_link_text('%s' % link).click()

    def select_from_list(self, list_name, value):
        self.driver.find_element_by_xpath(
            "//select[@name='{0}']/option[text()='{1}']".
            format(list_name, value)).click()

    def check_element_on_page(self, method, value):
        try:
            self.driver.find_element(method, value)
        except NoSuchElementException:
            return False
        return True

    def env_to_service(self, env_name):
        element_id = self.get_element_id(env_name)
        self.driver.find_element_by_id(
            "murano__row_{0}__action_show".format(element_id)).click()

    def create_demo_service(self, service_name):
        self.driver.find_element_by_id(
            'services__action_CreateService').click()

        self.select_from_list('service_choice-service', 'Demo Service')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        self.fill_field(by.By.ID, 'id_demoService-0-name', service_name)
        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()

        self.select_from_list('demoService-1-osImage', self.demo_image)
        next_button = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(next_button).click()

    def create_linux_telnet(self, service_name):
        self.driver.find_element_by_id(
            'services__action_CreateService').click()

        self.select_from_list('service_choice-service', 'Linux Telnet')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        self.fill_field(by.By.ID, 'id_linuxTelnetService-0-name',
                        service_name)
        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()

        self.select_from_list('linuxTelnetService-1-osImage',
                              self.linux_image)
        self.select_from_list('linuxTelnetService-1-keyPair',
                              self.keypair)
        next_button = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(next_button).click()

    def create_linux_apache(self, service_name):
        self.driver.find_element_by_id(
            'services__action_CreateService').click()

        self.select_from_list('service_choice-service', 'Linux Apache')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        self.fill_field(by.By.ID, 'id_linuxApacheService-0-name', service_name)
        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()
        self.select_from_list('linuxApacheService-1-osImage',
                              self.linux_image)
        self.select_from_list('linuxApacheService-1-keyPair',
                              self.keypair)
        next_button = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(next_button).click()

    def create_ad_service(self, service_name):
        self.driver.find_element_by_id(
            'services__action_CreateService').click()

        self.select_from_list('service_choice-service', 'Active Directory')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        ad = 'id_activeDirectory-0'

        self.fill_field(by.By.ID, '{0}-name'.format(ad), service_name)
        self.fill_field(by.By.ID, '{0}-adminPassword'.format(ad), 'P@ssw0rd')
        self.fill_field(by.By.ID,
                        '{0}-adminPassword-clone'.format(ad),
                        'P@ssw0rd')
        self.fill_field(by.By.ID,
                        '{0}-recoveryPassword'.format(ad),
                        'P@ssw0rd')
        self.fill_field(by.By.ID,
                        '{0}-recoveryPassword-clone'.format(ad),
                        'P@ssw0rd')
        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()

        self.select_from_list('activeDirectory-1-osImage', self.windows_image)
        next_button = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(next_button).click()

    def create_iis_service(self, service_name):
        self.driver.find_element_by_id(
            'services__action_CreateService').click()

        self.select_from_list(
            'service_choice-service', 'Internet Information Services')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        iis = 'id_webServer-0'

        self.fill_field(by.By.ID, '{0}-name'.format(iis), service_name)
        self.fill_field(by.By.ID, '{0}-adminPassword'.format(iis), 'P@ssw0rd')
        self.fill_field(by.By.ID,
                        '{0}-adminPassword-clone'.format(iis),
                        'P@ssw0rd')
        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()

        self.select_from_list('webServer-1-osImage', self.windows_image)
        next_button = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(next_button).click()

    def create_asp_service(self, service_name):
        self.driver.find_element_by_id(
            'services__action_CreateService').click()

        self.select_from_list('service_choice-service', 'ASP.NET Application')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        asp = 'id_aspNetApp-0'

        self.fill_field(by.By.ID, '{0}-name'.format(asp), service_name)
        self.fill_field(by.By.ID, '{0}-adminPassword'.format(asp), 'P@ssw0rd')
        self.fill_field(by.By.ID,
                        '{0}-adminPassword-clone'.format(asp),
                        'P@ssw0rd')
        self.fill_field(by.By.ID,
                        '{0}-repository'.format(asp),
                        self.asp_git_repository)

        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()

        self.select_from_list('aspNetApp-1-osImage', self.windows_image)
        next_button = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(next_button).click()

    def create_iisfarm_service(self, service_name):
        self.driver.find_element_by_id(
            'services__action_CreateService').click()

        self.select_from_list('service_choice-service',
                              'Internet Information Services Web Farm')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        iis_farm = 'id_webServerFarm-0'

        self.fill_field(by.By.ID, '{0}-name'.format(iis_farm), service_name)
        self.fill_field(by.By.ID,
                        '{0}-adminPassword'.format(iis_farm),
                        'P@ssw0rd')
        self.fill_field(by.By.ID,
                        '{0}-adminPassword-clone'.format(iis_farm),
                        'P@ssw0rd')

        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()

        self.select_from_list('webServerFarm-1-osImage', self.windows_image)
        next_button = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(next_button).click()

    def create_aspfarm_service(self, service_name):
        self.driver.find_element_by_id(
            'services__action_CreateService').click()

        self.select_from_list(
            'service_choice-service', 'ASP.NET Application Web Farm')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        asp_farm = 'id_aspNetAppFarm-0'

        self.fill_field(by.By.ID, '{0}-name'.format(asp_farm), service_name)
        self.fill_field(by.By.ID,
                        '{0}-adminPassword'.format(asp_farm),
                        'P@ssw0rd')
        self.fill_field(by.By.ID,
                        '{0}-adminPassword-clone'.format(asp_farm),
                        'P@ssw0rd')
        self.fill_field(by.By.ID,
                        '{0}-repository'.format(asp_farm),
                        self.asp_git_repository)

        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()

        self.select_from_list('aspNetAppFarm-1-osImage', self.windows_image)
        next_button = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(next_button).click()

    def create_mssql_service(self, service_name):
        self.driver.find_element_by_id(
            'services__action_CreateService').click()

        self.select_from_list('service_choice-service', 'MS SQL Server')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        mssql = 'id_msSqlServer-0'

        self.fill_field(by.By.ID, '{0}-name'.format(mssql), service_name)
        self.fill_field(by.By.ID, '{0}-adminPassword'.format(mssql), 'P@ssw0rd')
        self.fill_field(by.By.ID,
                        '{0}-adminPassword-clone'.format(mssql),
                        'P@ssw0rd')
        self.fill_field(by.By.ID, '{0}-saPassword'.format(mssql), 'P@ssw0rd')
        self.fill_field(by.By.ID,
                        '{0}-saPassword-clone'.format(mssql),
                        'P@ssw0rd')
        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()

        self.select_from_list('msSqlServer-1-osImage', self.windows_image)
        next_button = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(next_button).click()

    def create_sql_cluster_service(self, service_name, domain_name):
        self.driver.find_element_by_id(
            'services__action_CreateService').click()

        self.select_from_list('service_choice-service',
                              'MS SQL Server Cluster')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        sql_cluster = 'id_msSqlClusterServer'

        self.fill_field(by.By.ID,
                        '{0}-0-name'.format(sql_cluster),
                        service_name)
        self.fill_field(by.By.ID,
                        '{0}-0-adminPassword'.format(sql_cluster),
                        'P@ssw0rd')
        self.fill_field(by.By.ID,
                        '{0}-0-adminPassword-clone'.format(sql_cluster),
                        'P@ssw0rd')
        self.select_from_list('msSqlClusterServer-0-domain', domain_name)
        self.fill_field(by.By.ID,
                        '{0}-0-saPassword'.format(sql_cluster),
                        'P@ssw0rd')
        self.fill_field(by.By.ID,
                        '{0}-0-saPassword-clone'.format(sql_cluster),
                        'P@ssw0rd')
        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()

        self.fill_field(by.By.ID,
                        '{0}-1-clusterIp'.format(sql_cluster),
                        '1.1.1.1')
        self.fill_field(by.By.ID,
                        '{0}-1-clusterName'.format(sql_cluster),
                        'cluster')
        self.fill_field(by.By.ID,
                        '{0}-1-agGroupName'.format(sql_cluster),
                        'ag-name')
        self.fill_field(by.By.ID,
                        '{0}-1-agListenerName'.format(sql_cluster),
                        'listener_name')
        self.fill_field(by.By.ID,
                        '{0}-1-agListenerIP'.format(sql_cluster),
                        'listener_name')
        self.fill_field(by.By.ID,
                        '{0}-1-sqlServiceUserName'.format(sql_cluster),
                        'admin')
        self.fill_field(by.By.ID,
                        '{0}-1-sqlServicePassword'.format(sql_cluster),
                        'P@ssw0rd')
        self.fill_field(by.By.ID,
                        '{0}-1-sqlServicePassword-clone'.format(sql_cluster),
                        'P@ssw0rd')
        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()

        cluster_ip = self.get_env_subnet()
        self.fill_field(by.By.ID,
                        '{0}-1-clusterIp'.format(sql_cluster),
                        cluster_ip)
        listener_ip = self.get_env_subnet()
        self.fill_field(by.By.ID,
                        '{0}-1-agListenerIP'.format(sql_cluster),
                        listener_ip)
        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()

        self.fill_field(by.By.ID,
                        '{0}-2-databases'.format(sql_cluster),
                        'testbase')
        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()

        self.select_from_list('msSqlClusterServer-3-osImage',
                              self.windows_image)
        next_button = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(next_button).click()

    def create_tomcat_service(self, service_name, database):
        self.driver.find_element_by_id(
            'services__action_CreateService').click()

        self.select_from_list('service_choice-service', 'Tomcat')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        tomcat = 'id_tomcat-0'

        self.fill_field(by.By.ID, '{0}-name'.format(tomcat), service_name)
        self.fill_field(by.By.ID,
                        '{0}-repository'.format(tomcat),
                        self.tomcat_repository)
        self.select_from_list('tomcat-0-psqlDatabase', database)
        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()

        self.select_from_list('tomcat-1-osImage', self.linux_image)

        next_button = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(next_button).click()

    def create_postgreSQL_service(self, service_name):
        self.driver.find_element_by_id(
            'services__action_CreateService').click()

        self.select_from_list('service_choice-service', 'PostgreSQL')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        psql = 'id_postgreSql-0'

        self.fill_field(by.By.ID, '{0}-name'.format(psql), service_name)
        self.fill_field(by.By.ID, '{0}-database'.format(psql), 'psql-base')
        self.fill_field(by.By.ID, '{0}-username'.format(psql), 'admin')
        self.fill_field(by.By.ID, '{0}-password'.format(psql), 'P@ssw0rd')
        self.fill_field(by.By.ID, '{0}-password-clone'.format(psql), 'P@ssw0rd')

        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()

        self.select_from_list('postgreSql-1-osImage', self.linux_image)

        next_button = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(next_button).click()

    def get_element_id(self, element_name):
        path = self.driver.find_element_by_link_text(
            element_name).get_attribute("href")
        return path.split('/')[-2]

    def delete_service(self, service_name):
        service_id = self.get_element_id(service_name)
        self.driver.find_element_by_id(
            'services__row_{0}__action_delete'.format(service_id)).click()
        self.driver.find_element_by_link_text('Delete Service').click()

    def get_env_subnet(self):
        help_text = self.driver.find_element_by_xpath(
            "(.//span[@class = 'help-inline'])[1]").text
        subnet = help_text.split('.')[-2]
        num = random.randint(0, 255)
        return '10.0.{0}.{1}'.format(subnet, num)

    def check_that_error_message_is_correct(self, error_message, num):
        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()
        time.sleep(3)
        appeared_text = self.driver.find_element_by_xpath(
            "(.//div[@class = 'control-group form-field clearfix error'][%d])"
            % num).text
        index = appeared_text.find(error_message)

        if index != -1:
            return True
        else:
            return False

    def check_that_alert_message_is_appeared(self, error_message):
        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()

        xpath = ".//*[@id='create_service_form']/div[2]/input[2]"
        WebDriverWait(self.driver, 10).until(lambda s: s.find_element(
            by.By.XPATH, xpath).is_displayed())

        appeared_text = self.driver.find_element_by_xpath(
            "(.//div[@class = 'alert alert-message alert-error'])").text
        index = appeared_text.find(error_message)

        if index != -1:
            return True
        else:
            return False

    def click_on_service_catalog_action(self, action):
        self.driver.find_element_by_xpath(
            ".//*[@id='service_catalog__action_{0}']".format(action)).click()

    def compose_trivial_service(self, name):
        self.click_on_service_catalog_action(action='compose_service')

        self.fill_field(by.By.ID, 'id_service_display_name', name)
        self.fill_field(by.By.ID,
                        'id_full_service_name',
                        '{0}Service'.format(name))
        self.fill_field(by.By.ID, 'id_author', cfg.common.user)
        self.fill_field(by.By.ID, 'id_description', 'New Service')

        self.driver.find_element_by_link_text('UI Files').click()
        self.select_and_click_element('ui##Demo.yaml')
        self.driver.find_element_by_link_text('Workflows').click()
        self.driver.find_element_by_xpath(
            ".//*[@name = 'workflows@@workflows##Demo.xml@@selected']").click()
        self.driver.find_element_by_link_text('Heat Templates').click()
        self.driver.find_element_by_xpath(
            ".//*[@name = 'heat@@heat##Demo.template@@selected']").click()

        submit_button = self.elements.get('button', 'InputSubmit')
        self.driver.find_element_by_xpath(submit_button).click()

    def select_action_for_service(self, service, action):
        time.sleep(2)
        if action == 'more':
            self.driver.find_element_by_xpath(
                ".//*[@id='service_catalog__row__{0}']/td[7]/div/a[2]".
                format(service)).click()
            WebDriverWait(self.driver, 10).until(lambda s: s.find_element(
                by.By.XPATH,
                ".//*[@id='service_catalog__row_{0}__action_manage_service']".
                format(service)).is_displayed())
        else:
            self.driver.find_element_by_xpath(
                ".//*[@id='service_catalog__row_{0}__action_{1}']".
                format(service, action)).click()

    def check_service_parameter(self, page, service, column, value):

        result = self.driver.find_element_by_xpath(
            ".//*[@id='{0}__row__{1}']/td[{2}]".
            format(page, service, column)).text
        if result == value:
            return True
        else:
            return False

    def select_and_click_element(self, element):
        self.driver.find_element_by_xpath(
            ".//*[@value = '{0}']".format(element)).click()

    def choose_and_upload_files(self, name):
        __location = os.path.realpath(os.path.join(os.getcwd(),
                                                   os.path.dirname(__file__)))
        self.driver.find_element_by_xpath(".//*[@id='id_file']").click()
        self.driver.find_element_by_id('id_file').send_keys(
            os.path.join(__location, name))

    def check_the_status_of_env(self, env_name, status):
        env_id = self.get_element_id(env_name)

        env_status = self.driver.find_element_by_xpath(
            ".//*[@id='murano__row__{0}']/td[3]".format(env_id))
        k = 0
        while env_status.text != status:
            time.sleep(15)
            k += 1
            self.driver.refresh()
            env_status = self.driver.find_element_by_xpath(
                ".//*[@id='murano__row__{0}']/td[3]".format(env_id))
            if k > 160:
                log.error('\nTimeout has expired')
                break

    def check_that_deploy_finished(self, env_name):
        self.navigate_to('Environments')
        self.click_on_more(env_name)
        self.select_action_for_environment(env_name, 'show_deployments')
        status = self.driver.find_element_by_xpath(
            "/html/body/div/div[2]/div[3]/form/table/tbody/tr/td[3]").text

        self.driver.find_element_by_link_text("Show Details").click()
        self.driver.find_element_by_link_text("Logs").click()
        self.take_screenshot(self._testMethodName)

        self.navigate_to('Environments')
        self.click_on_more(env_name)
        self.select_action_for_environment(env_name, 'show_deployments')

        self.assertEqual('Successful', status, 'Deploy finished with errors')
