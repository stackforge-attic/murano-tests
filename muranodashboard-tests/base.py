import testtools
import ConfigParser
import random
import time
import json
import datetime
import os
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

from selenium import webdriver
import selenium.webdriver.common.by as by
import config.config as cfg
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait

from keystoneclient.v2_0 import client as ksclient
from muranoclient.client import Client as mclient
from glanceclient import Client as gclient


class ImageException(Exception):
    message = "Image doesn't exist"

    def __init__(self, type):
        self._error_string = self.message + '\nDetails: %s' \
                                            ' image is not found,' % str(type)

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
        filename = '%s/%s-%s.png' % (
            screenshot_dir, test_name, date)
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
            ".//*[@id='murano__row__%s']/td[4]/div/a[2]" % element_id).click()

    def select_action_for_environment(self, env_name, action):
        element_id = self.get_element_id(env_name)
        self.driver.find_element_by_id(
            "murano__row_%s__action_%s" % (element_id, action)).click()

    def navigate_to(self, link):
        self.driver.find_element_by_link_text('Murano').click()
        self.driver.find_element_by_link_text('%s' % link).click()

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

        self.fill_field(
            by.By.ID, 'id_activeDirectory-0-name', service_name)
        self.fill_field(
            by.By.ID, 'id_activeDirectory-0-adminPassword', 'P@ssw0rd')
        self.fill_field(
            by.By.ID, 'id_activeDirectory-0-adminPassword-clone', 'P@ssw0rd')
        self.fill_field(
            by.By.ID, 'id_activeDirectory-0-recoveryPassword', 'P@ssw0rd')
        self.fill_field(
            by.By.ID,
            'id_activeDirectory-0-recoveryPassword-clone', 'P@ssw0rd')
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

        self.fill_field(by.By.ID, 'id_webServer-0-name', service_name)
        self.fill_field(
            by.By.ID, 'id_webServer-0-adminPassword', 'P@ssw0rd')
        self.fill_field(
            by.By.ID, 'id_webServer-0-adminPassword-clone', 'P@ssw0rd')
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

        self.fill_field(by.By.ID, 'id_aspNetApp-0-name', service_name)
        self.fill_field(
            by.By.ID, 'id_aspNetApp-0-adminPassword', 'P@ssw0rd')
        self.fill_field(
            by.By.ID, 'id_aspNetApp-0-adminPassword-clone', 'P@ssw0rd')
        self.fill_field(
            by.By.ID, 'id_aspNetApp-0-repository', self.asp_git_repository)
        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()

        self.select_from_list('aspNetApp-1-osImage', self.windows_image)
        next_button = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(next_button).click()

    def create_iisfarm_service(self, service_name):
        self.driver.find_element_by_id(
            'services__action_CreateService').click()

        self.select_from_list(
            'service_choice-service', 'Internet Information Services Web Farm')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        self.fill_field(by.By.ID, 'id_webServerFarm-0-name', service_name)
        self.fill_field(
            by.By.ID, 'id_webServerFarm-0-adminPassword', 'P@ssw0rd')
        self.fill_field(
            by.By.ID, 'id_webServerFarm-0-adminPassword-clone', 'P@ssw0rd')
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

        self.fill_field(by.By.ID, 'id_aspNetAppFarm-0-name', service_name)
        self.fill_field(
            by.By.ID, 'id_aspNetAppFarm-0-adminPassword', 'P@ssw0rd')
        self.fill_field(
            by.By.ID, 'id_aspNetAppFarm-0-adminPassword-clone', 'P@ssw0rd')
        self.fill_field(
            by.By.ID, 'id_aspNetAppFarm-0-repository', self.asp_git_repository)
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

        self.fill_field(by.By.ID, 'id_msSqlServer-0-name', service_name)
        self.fill_field(
            by.By.ID, 'id_msSqlServer-0-adminPassword', 'P@ssw0rd')
        self.fill_field(
            by.By.ID, 'id_msSqlServer-0-adminPassword-clone', 'P@ssw0rd')
        self.fill_field(
            by.By.ID, 'id_msSqlServer-0-saPassword', 'P@ssw0rd')
        self.fill_field(
            by.By.ID, 'id_msSqlServer-0-saPassword-clone', 'P@ssw0rd')
        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()

        self.select_from_list('msSqlServer-1-osImage', self.windows_image)
        next_button = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(next_button).click()

    def create_sql_cluster_service(self, service_name, domain_name):
        self.driver.find_element_by_id(
            'services__action_CreateService').click()

        self.select_from_list(
            'service_choice-service', 'MS SQL Server Cluster')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-0-name', service_name)
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-0-adminPassword', 'P@ssw0rd')
        self.fill_field(
            by.By.ID,
            'id_msSqlClusterServer-0-adminPassword-clone', 'P@ssw0rd')
        self.select_from_list('msSqlClusterServer-0-domain', domain_name)
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-0-saPassword', 'P@ssw0rd')
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-0-saPassword-clone', 'P@ssw0rd')
        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()

        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-1-clusterIp', '1.1.1.1')
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-1-clusterName', 'cluster')
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-1-agGroupName', 'ag-name')
        self.fill_field(
            by.By.ID,
            'id_msSqlClusterServer-1-agListenerName', 'listener_name')
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-1-agListenerIP', 'listener_name')
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-1-sqlServiceUserName', 'admin')
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-1-sqlServicePassword', 'P@ssw0rd')
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-1-sqlServicePassword-clone',
            'P@ssw0rd')
        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()

        cluster_ip = self.get_env_subnet()
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-1-clusterIp', cluster_ip)
        listener_ip = self.get_env_subnet()
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-1-agListenerIP', listener_ip)
        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()

        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-2-databases', 'testbase')
        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()

        self.select_from_list(
            'msSqlClusterServer-3-osImage', self.windows_image)
        next_button = self.elements.get('button', 'Create')
        self.driver.find_element_by_xpath(next_button).click()

    def get_element_id(self, element_name):
        path = self.driver.find_element_by_link_text(
            element_name).get_attribute("href")
        return path.split('/')[-2]

    def delete_service(self, service_name):
        service_id = self.get_element_id(service_name)
        self.driver.find_element_by_id('services__row_%s__action_delete'
                                       % service_id).click()
        self.driver.find_element_by_link_text('Delete Service').click()

    def get_env_subnet(self):
        help_text = self.driver.find_element_by_xpath(
            "(.//span[@class = 'help-inline'])[1]").text
        subnet = help_text.split('.')[-2]
        num = random.randint(0, 255)
        return '10.0.%s.%d' % (subnet, num)

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
            ".//*[@id='service_catalog__action_%s']" % action).click()

    def compose_trivial_service(self, name):
        self.click_on_service_catalog_action(action='compose_service')

        self.fill_field(by.By.ID, 'id_service_display_name', name)
        self.fill_field(by.By.ID, 'id_full_service_name', '%sService' % name)
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
                ".//*[@id='service_catalog__row__%s']/td[7]/div/a[2]"
                % service).click()
            WebDriverWait(self.driver, 10).until(lambda s: s.find_element(
                by.By.XPATH, ".//*[@id='service_catalog__row_%s__action_"
                             "manage_service']" % service).is_displayed())
        else:
            self.driver.find_element_by_xpath(
                ".//*[@id='service_catalog__row_%s__action_%s']"
                % (service, action)).click()

    def check_service_parameter(self, service, column, value):

        result = self.driver.find_element_by_xpath(
            ".//*[@id='service_catalog__row__%s']/td[%s]"
            % (service, column)).text
        if result == value:
            return True
        else:
            return False

    def select_and_click_element(self, element):
        self.driver.find_element_by_xpath(
            ".//*[@value = '%s']" % element).click()

    def choose_and_upload_files(self, name):
        __location = os.path.realpath(os.path.join(os.getcwd(),
                                                   os.path.dirname(__file__)))
        self.driver.find_element_by_xpath(".//*[@id='id_file']").click()
        self.driver.find_element_by_id('id_file').send_keys(
            os.path.join(__location, name))
        self.select_and_click_element('Upload')

    def check_the_status_of_env(self, env_name, status):
        env_id = self.get_element_id(env_name)

        env_status = self.driver.find_element_by_xpath(
            ".//*[@id='murano__row__%s']/td[3]" % env_id)
        k = 0
        while env_status.text != status:
            time.sleep(15)
            k += 1
            self.driver.refresh()
            env_status = self.driver.find_element_by_xpath(
                ".//*[@id='murano__row__%s']/td[3]" % env_id)
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
