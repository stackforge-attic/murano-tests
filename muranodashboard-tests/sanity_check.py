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
        self.delete_environment()

        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'test_create_del_env'))

    def test_edit_environment(self):
        self.log_in()
        self.navigate_to_environments()
        self.create_environment('test_edit_env')
        self.driver.find_element_by_link_text('test_edit_env')
        self.edit_environment(new_name='edited_env')

        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'edited_env'))

    def test_rename_windows_image(self):
        self.log_in()
        self.navigate_to_images()
        self.driver.find_element_by_id(
            'marked_images__action_mark_image').click()
        self.select_from_list('image', 'ws-2012-std')
        self.find_clean_send(by.By.ID, 'id_title',
                             'Windows Server 2012 Standard')
        self.select_from_list('type', ' Windows Server 2012')
        mark = self.elements.get('button', 'ButtonSubmit')
        self.driver.find_element_by_xpath(mark).click()

<<<<<<< HEAD
    def test_create_demo_service(self):
=======
    def test_create_and_delete_demo_service(self):
>>>>>>> f3efa1b... Add 'create demo service' dashboard test
        self.log_in()
        self.navigate_to_environments()
        self.create_environment('test')
        self.create_demo_service('DemoService')

        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
<<<<<<< HEAD
                                                   'DemoService'))
=======
                                                   'DemoService'))

        self.delete_service('DemoService')

        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'DemoService'))
>>>>>>> f3efa1b... Add 'create demo service' dashboard test
