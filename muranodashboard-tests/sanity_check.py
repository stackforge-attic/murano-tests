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
        self.find_clean_send(by.By.ID, 'id_title', 'New Image')
        self.select_from_list('type', ' Windows Server 2012')

        mark = self.elements.get('button', 'MarkImage')
        self.driver.find_element_by_xpath(mark).click()

    def test_delete_image(self):
        self.log_in()
        self.navigate_to_images()
        self.driver.find_element_by_id(
            'marked_images__action_mark_image').click()

        self.select_from_list('image', 'TestImageForDeletion')
        self.find_clean_send(by.By.ID, 'id_title', 'Image for deletion')
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
        self.create_demo_service('test', 'DemoService')

        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'DemoService'))

        self.delete_service('DemoService')

        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'DemoService'))

    def test_create_and_delete_linux_telnet(self):
        self.log_in()
        self.navigate_to_environments()
        self.create_environment('test')
        self.create_linux_telnet('test', 'linuxtelnet')

        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'linuxtelnet'))

        self.delete_service('linuxtelnet')

        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'linuxtelnet'))

    def test_create_and_delete_linux_apache(self):
        self.log_in()
        self.navigate_to_environments()
        self.create_environment('test')
        self.create_linux_apache('test', 'linuxapache')

        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'linuxapache'))

        self.delete_service('linuxapache')

        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'linuxapache'))