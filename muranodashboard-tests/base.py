import traceback
import unittest2

import selenium.common.exceptions as selenim_except
from selenium import webdriver
import selenium.webdriver.common.by as by

import config.config as cfg

class UITestCase():

    @classmethod
    def setUpClass(cls):
        try:
            cls.ifFail = False
            cls.driver = webdriver.Firefox()
            cls.driver.get(cfg.common.base_url + "/")
            cls.find_clean_send(by.By.ID, "id_username", cfg.common.user)
            cls.find_clean_send(by.By.ID, "id_password", cfg.common.password)
            cls.driver.find_element_by_xpath(
                "//button[@type='submit']").click()
        except Exception:
            traceback.print_exc()
            cls.ifFail = True
            pass

    def setUp(self):
        if self.ifFail:
            self.fail("setUpClass method is fail")

    def find_clean_send(cls, by_find, find_element, send):
        cls.driver.find_element(by=by_find, value=find_element).clear()
        cls.driver.find_element(by=by_find, value=find_element).send_keys(send)

    def create_environment(cls, env_name):
        cls.driver.find_element_by_id("murano__action_CreateEnvironment").click()
        cls.find_clean_send(by.By.ID, "id_name", env_name)
        cls.driver.find_element_by_xpath(".//*[@id='modal_wrapper']/div/form/div[3]/input").click()
