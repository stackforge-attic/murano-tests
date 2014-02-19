import sys
import os
sys.path.append(os.getcwd())

import testtools
from base import UITestCase
import selenium.webdriver.common.by as by


class UIDeployTests(UITestCase):

    def test_035_deploy_demo_service(self):
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

    def test_036_deploy_telnet_service(self):
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

    def test_037_deploy_apache_service(self):
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

    def test_038_deploy_ad_service(self):
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

    def test_039_deploy_iis_service(self):
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

    def test_040_deploy_asp_service(self):
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
    def test_041_deploy_iis_farm_service(self):
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
    def test_042_deploy_asp_farm_service(self):
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

    def test_043_deploy_mssql_service(self):
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

    def test_044_deploy_sql_cluster_service(self):
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