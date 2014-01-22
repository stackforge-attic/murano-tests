import base
import config.config as cfg

class UISanityTests(base.UITestCase):

    def test_create_environment(self):
        self.driver.find_element_by_link_text("Murano").click()
        self.driver.find_element_by_link_text("Environment").click()
        self.create_environment(name="test")


