import sys
import os
sys.path.append(os.getcwd())

import testtools
from base import UITestCase
import selenium.webdriver.common.by as by


class UIDeployTests(UITestCase):

    def test_001_deploy_demo_service(self):
        self.log_in()
        self.navigate_to('Environments')
        self.create_environment('deploy_demo')
        self.env_to_service('deploy_demo')

        self.create_demo_service('DemoService')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'DemoService'))
        self.driver.find_element_by_id('services__action_deploy_env').click()
        self.navigate_to('Environments')
        self.check_the_status_of_env('deploy_demo', 'Ready')
        self.check_that_deploy_finished('deploy_demo')

    def test_002_deploy_telnet_service(self):
        self.log_in()
        self.navigate_to('Environments')
        self.create_environment('deploy_telnet')
        self.env_to_service('deploy_telnet')

        self.create_linux_telnet('linuxtelnet')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'linuxtelnet'))

        self.driver.find_element_by_id('services__action_deploy_env').click()
        self.navigate_to('Environments')
        self.check_the_status_of_env('deploy_telnet', 'Ready')
        self.check_that_deploy_finished('deploy_telnet')

    def test_003_deploy_apache_service(self):
        self.log_in()
        self.navigate_to('Environments')
        self.create_environment('deploy_apache')
        self.env_to_service('deploy_apache')

        self.create_linux_apache('linuxapache')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'linuxapache'))

        self.driver.find_element_by_id('services__action_deploy_env').click()
        self.navigate_to('Environments')
        self.check_the_status_of_env('deploy_apache', 'Ready')
        self.check_that_deploy_finished('deploy_apache')

    def test_004_deploy_ad_service(self):
        self.log_in()
        self.navigate_to('Environments')
        self.create_environment('deploy_ad')
        self.env_to_service('deploy_ad')

        self.create_ad_service('muranotest.domain')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'muranotest.domain'))

        self.driver.find_element_by_id('services__action_deploy_env').click()
        self.navigate_to('Environments')
        self.check_the_status_of_env('deploy_ad', 'Ready')
        self.check_that_deploy_finished('deploy_ad')

    def test_005_deploy_iis_service(self):
        self.log_in()
        self.navigate_to('Environments')
        self.create_environment('deploy_iis')
        self.env_to_service('deploy_iis')

        self.create_iis_service('IISService')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'IISService'))

        self.driver.find_element_by_id('services__action_deploy_env').click()
        self.navigate_to('Environments')
        self.check_the_status_of_env('deploy_iis', 'Ready')
        self.check_that_deploy_finished('deploy_iis')

    def test_006_deploy_asp_service(self):
        self.log_in()
        self.navigate_to('Environments')
        self.create_environment('deploy_asp')
        self.env_to_service('deploy_asp')

        self.create_asp_service('ASPService')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'ASPService'))

        self.driver.find_element_by_id('services__action_deploy_env').click()
        self.navigate_to('Environments')
        self.check_the_status_of_env('deploy_asp', 'Ready')
        self.check_that_deploy_finished('deploy_asp')

    @testtools.skip("There is no Neutron LB on lab")
    def test_007_deploy_iis_farm_service(self):
        self.log_in()
        self.navigate_to('Environments')
        self.create_environment('deploy_iisfarm')
        self.env_to_service('deploy_iisfarm')

        self.create_iisfarm_service('IISFarmService')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'IISFarmService'))

        self.driver.find_element_by_id('services__action_deploy_env').click()
        self.navigate_to('Environments')
        self.check_the_status_of_env('deploy_iisfarm', 'Ready')
        self.check_that_deploy_finished('deploy_iisfarm')

    @testtools.skip("There is no Neutron LB on lab")
    def test_008_deploy_asp_farm_service(self):
        self.log_in()
        self.navigate_to('Environments')
        self.create_environment('deploy_aspfarm')
        self.env_to_service('deploy_aspfarm')

        self.create_aspfarm_service('ASPFarmService')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'ASPFarmService'))

        self.driver.find_element_by_id('services__action_deploy_env').click()
        self.navigate_to('Environments')
        self.check_the_status_of_env('deploy_aspfarm', 'Ready')
        self.check_that_deploy_finished('deploy_aspfarm')

    def test_009_deploy_mssql_service(self):
        self.log_in()
        self.navigate_to('Environments')
        self.create_environment('deploy_mssql')
        self.env_to_service('deploy_mssql')

        self.create_mssql_service('MSSQLService')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'MSSQLService'))

        self.driver.find_element_by_id('services__action_deploy_env').click()
        self.navigate_to('Environments')
        self.check_the_status_of_env('deploy_mssql', 'Ready')
        self.check_that_deploy_finished('deploy_mssql')

    @testtools.skip("https://bugs.launchpad.net/murano/+bug/1282097")
    def test_010_deploy_sql_cluster_service(self):
        self.log_in()
        self.navigate_to('Environments')
        self.create_environment('deploy_mssql_cluster')
        self.env_to_service('deploy_mssql_cluster')

        self.create_ad_service('activeDirectory.mssql')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'activeDirectory.mssql'))

        self.driver.find_element_by_link_text('Create Service').click()
        self.create_sql_cluster_service('SQLCluster', 'activeDirectory.mssql')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'SQLCluster'))

        self.driver.find_element_by_id('services__action_deploy_env').click()
        self.navigate_to('Environments')
        self.check_the_status_of_env('deploy_mssql_cluster', 'Ready')
        self.check_that_deploy_finished('deploy_mssql_cluster')

    def test_011_deploy_postgreSQL_service(self):
        self.log_in()
        self.navigate_to('Environments')
        self.create_environment('deploy_postgreSQL')
        self.env_to_service('deploy_postgreSQL')

        self.create_postgreSQL_service('postgreSQL-serv')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'postgreSQL-serv'))

        self.driver.find_element_by_id('services__action_deploy_env').click()
        self.navigate_to('Environments')
        self.check_the_status_of_env('deploy_postgreSQL', 'Ready')
        self.check_that_deploy_finished('deploy_postgreSQL')

    def test_012_deploy_tomcat_service(self):
        self.log_in()
        self.navigate_to('Environments')
        self.create_environment('deploy_tomcat')
        self.env_to_service('deploy_tomcat')

        self.create_postgreSQL_service('postgreSQL')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'postgreSQL'))

        self.driver.find_element_by_link_text('Create Service').click()
        self.create_tomcat_service('tomcat', 'postgreSQL')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'tomcat'))

        self.driver.find_element_by_id('services__action_deploy_env').click()
        self.navigate_to('Environments')
        self.check_the_status_of_env('deploy_tomcat', 'Ready')
        self.check_that_deploy_finished('deploy_tomcat')

    def test_013_add_service_in_deployed_env(self):
        self.log_in()
        self.navigate_to('Environments')
        self.create_environment('add_service_in_deployed_env')
        self.env_to_service('add_service_in_deployed_env')

        self.create_linux_telnet('telnet')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'telnet'))

        self.driver.find_element_by_id('services__action_deploy_env').click()
        self.navigate_to('Environments')
        self.check_the_status_of_env('add_service_in_deployed_env', 'Ready')
        self.check_that_deploy_finished('add_service_in_deployed_env')

        self.navigate_to('Environments')
        self.env_to_service('add_service_in_deployed_env')
        self.create_iis_service('iis')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT, 'iis'))

    def test_014_deploy_linux_windows_services(self):
        self.log_in()
        self.navigate_to('Environments')
        self.create_environment('linux_windows_services')
        self.env_to_service('linux_windows_services')

        self.create_linux_telnet('telnet')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'telnet'))

        self.create_iis_service('iis')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT, 'iis'))

        self.driver.find_element_by_id('services__action_deploy_env').click()
        self.navigate_to('Environments')
        self.check_the_status_of_env('linux_windows_services', 'Ready')
        self.check_that_deploy_finished('linux_windows_services')

    def test_015_checking_type_and_last_operation(self):
        self.log_in()
        self.navigate_to('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.create_linux_telnet('telnet')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'telnet'))
        self.driver.find_element_by_id('services__action_deploy_env').click()

        self.assertTrue(self.check_service_parameter(
            'services', 'telnet', '3', 'Linux Telnet'))
        self.assertTrue(self.check_service_parameter(
            'services', 'telnet', '4', 'Deploy in progress'))
        self.assertFalse(self.check_service_parameter(
            'services', 'telnet', '5', 'Service draft created'))
        self.navigate_to('Environments')
        self.check_the_status_of_env('test', 'Ready')
        self.check_that_deploy_finished('test')
