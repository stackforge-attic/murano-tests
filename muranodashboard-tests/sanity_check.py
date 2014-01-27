import sys
import os
sys.path.append(os.getcwd())
from base import UITestCase
import selenium.webdriver.common.by as by


class UISanityTests(UITestCase):

    def test_create_delete_environment(self):
        self.log_in()
        self.create_environment('test_create_del_env')
        self.driver.find_element_by_link_text('test_create_del_env').click()
        self.delete_environment('test_create_del_env')

        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'test_create_del_env'))

    def test_edit_environment(self):
        self.log_in()
        self.navigate_to_environments()
        self.create_environment('test_edit_env')
        self.driver.find_element_by_link_text('test_edit_env')
        self.edit_environment(old_name='test_edit_env', new_name='edited_env')

        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'edited_env'))

    def test_rename_image(self):
        self.log_in()
        self.navigate_to_images()
        self.driver.find_element_by_id(
            'marked_images__action_mark_image').click()

        self.select_from_list('image', 'TestImageForDeletion')
        self.fill_field(by.By.ID, 'id_title', 'New Image')
        self.select_from_list('type', ' Windows Server 2012')

        mark = self.elements.get('button', 'MarkImage')
        self.driver.find_element_by_xpath(mark).click()

    def test_delete_image(self):
        self.log_in()
        self.navigate_to_images()
        self.driver.find_element_by_id(
            'marked_images__action_mark_image').click()

        self.select_from_list('image', 'TestImageForDeletion')
        self.fill_field(by.By.ID, 'id_title', 'Image for deletion')
        self.select_from_list('type', ' Windows Server 2012')

        mark = self.elements.get('button', 'MarkImage')
        self.driver.find_element_by_xpath(mark).click()

        element_id = self.get_element_id('TestImageForDeletion')
        self.driver.find_element_by_id(
            "marked_images__row_%s__action_delete" % element_id).click()
        self.confirm_deletion()
        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'TestImageForDeletion'))

    def test_create_and_delete_demo_service(self):
        self.log_in()
        self.navigate_to_environments()
        self.create_environment('test')
        self.env_to_service('test')
        self.create_demo_service('DemoService')

        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'DemoService'))

        self.delete_service('DemoService')

        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'DemoService'))

    def test_create_and_delete_linux_telnet(self):
        self.log_in()
        self.navigate_to_environments()
        self.create_environment('test')
        self.env_to_service('test')
        self.create_linux_telnet('linuxtelnet')

        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'linuxtelnet'))

        self.delete_service('linuxtelnet')

        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'linuxtelnet'))

    def test_create_and_delete_linux_apache(self):
        self.log_in()
        self.navigate_to_environments()
        self.create_environment('test')
        self.env_to_service('test')
        self.create_linux_apache('linuxapache')

        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'linuxapache'))

        self.delete_service('linuxapache')

        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'linuxapache'))

    def test_create_and_delete_ad_service(self):
        self.log_in()
        self.navigate_to_environments()
        self.create_environment('test')
        self.env_to_service('test')
        self.create_ad_service('muranotest.domain')

        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'muranotest.domain'))

        self.delete_service('muranotest.domain')

        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'muranotest.domain'))

    def test_create_and_delete_iis_service(self):
        self.log_in()
        self.navigate_to_environments()
        self.create_environment('test')
        self.env_to_service('test')
        self.create_iis_service('IISService')

        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'IISService'))

        self.delete_service('IISService')

        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'IISService'))

    def test_create_and_delete_asp_service(self):
        self.log_in()
        self.navigate_to_environments()
        self.create_environment('test')
        self.env_to_service('test')
        self.create_asp_service('ASPService')

        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'ASPService'))

        self.delete_service('ASPService')

        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'ASPService'))

    def test_create_and_delete_iisfarm_service(self):
        self.log_in()
        self.navigate_to_environments()
        self.create_environment('test')
        self.env_to_service('test')
        self.create_iisfarm_service('IISFarmService')

        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'IISFarmService'))

        self.delete_service('IISFarmService')

        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'IISFarmService'))

    def test_create_and_delete_aspfarm_service(self):
        self.log_in()
        self.navigate_to_environments()
        self.create_environment('test')
        self.env_to_service('test')
        self.create_aspfarm_service('ASPFarmService')

        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'ASPFarmService'))

        self.delete_service('ASPFarmService')

        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'ASPFarmService'))

    def test_create_and_delete_mssql_service(self):
        self.log_in()
        self.navigate_to_environments()
        self.create_environment('test')
        self.env_to_service('test')
        self.create_mssql_service('ASPFarmService')

        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'MSSQLService'))

        self.delete_service('MSSQLService')

        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'MSSQLService'))

    def test_create_and_delete_sql_cluster_service(self):
        self.log_in()
        self.navigate_to_environments()
        self.create_environment('test')
        self.env_to_service('test')
        self.create_ad_service('activeDirectory.mssql')

        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'activeDirectory.mssql'))

        self.driver.find_element_by_link_text('Create Service').click()
        self.create_sql_cluster_service('SQLCluster', 'activeDirectory.mssql')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'SQLCluster'))

        self.delete_service('SQLCluster')

        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'SQLCluster'))
