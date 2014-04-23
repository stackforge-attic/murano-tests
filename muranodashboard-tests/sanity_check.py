import os
import sys
sys.path.append(os.getcwd())

import selenium.webdriver.common.by as by
from selenium.webdriver.support.ui import WebDriverWait
import testtools

from base import UITestCase


class UISanityTests(UITestCase):

    def test_001_create_delete_environment(self):
        """
        Test check ability to create and delete environment

        Scenario:
            1. Create environment
            2. Navigate to this environment
            3. Go back to environment list and delete created environment
        """
        self.go_to_submenu('Environments')
        self.create_environment('test_create_del_env')
        self.driver.find_element_by_link_text('test_create_del_env').click()

        self.delete_environment('test_create_del_env')
        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'test_create_del_env'))

    def test_002_edit_environment(self):
        """
        Test check ability to change environment name

        Scenario:
            1. Create environment
            2. Change environment's name
            3. Check that there is renamed environment is in environment list
        """
        self.go_to_submenu('Environments')
        self.create_environment('test_edit_env')
        self.driver.find_element_by_link_text('test_edit_env')

        self.edit_environment(old_name='test_edit_env', new_name='edited_env')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'edited_env'))
        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'test_edit_env'))

    def test_003_rename_image(self):
        """
        Test check ability to mark murano image

        Scenario:
            1. Navigate to Images page
            2. Click on button "Mark Image"
            3. Fill the form and submit it
        """
        self.navigate_to('Manage')
        self.go_to_submenu('Images')
        self.driver.find_element_by_id(
            'marked_images__action_mark_image').click()

        self.select_from_list('image', 'TestImageForDeletion')
        self.fill_field(by.By.ID, 'id_title', 'New Image')
        self.select_from_list('type', ' Windows Server 2012')

        self.select_and_click_element('Mark')

    def test_004_delete_image(self):
        """
        Test check ability to delete image

        Scenario:
            1. Navigate to Images page
            2. Create test image
            3. Select created image and click on "Delete Metadata"
        """
        self.navigate_to('Manage')
        self.go_to_submenu('Images')
        self.driver.find_element_by_id(
            'marked_images__action_mark_image').click()

        self.select_from_list('image', 'TestImageForDeletion')
        self.fill_field(by.By.ID, 'id_title', 'Image for deletion')
        self.select_from_list('type', ' Windows Server 2012')

        self.select_and_click_element('Mark')

        element_id = self.get_element_id('TestImageForDeletion')
        self.driver.find_element_by_id(
            "marked_images__row_%s__action_delete" % element_id).click()
        self.confirm_deletion()
        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'TestImageForDeletion'))

    @testtools.skip("New UI in progress")
    def test_005_create_and_delete_demo_service(self):
        """
        Test check ability to create and delete demo service

        Scenario:
            1. Navigate to Environments page
            2. Create environment
            3. Create demo service in this environment by filling
            the creation form
            4. Delete demo service from environment
        """
        self.go_to_submenu('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_link_text('Add Application').click()
        self.create_demo_service('DemoService')

        self.go_to_submenu('Environments')
        self.env_to_service('test')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'DemoService'))

        self.delete_service('DemoService')
        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'DemoService'))

    @testtools.skip("New UI in progress")
    def test_006_create_and_delete_linux_telnet(self):
        """
        Test check ability to create and delete linux telnet service

        Scenario:
            1. Navigate to Environments page
            2. Create environment
            3. Create linux telnet service in this environment by filling
            the creation form
            4. Delete linux telnet service from environment
        """
        self.go_to_submenu('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_link_text('Add Application').click()
        self.create_linux_telnet('linuxtelnet')

        self.go_to_submenu('Environments')
        self.env_to_service('test')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'linuxtelnet'))

        self.delete_service('linuxtelnet')
        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'linuxtelnet'))

    @testtools.skip("New UI in progress")
    def test_007_create_and_delete_linux_apache(self):
        """
        Test check ability to create and delete linux apache service

        Scenario:
            1. Navigate to Environments page
            2. Create environment
            3. Create linux apache service in this environment by filling
            the creation form
            4. Delete linux apache service from environment
        """
        self.go_to_submenu('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_link_text('Add Application').click()
        self.create_linux_apache('linuxapache')

        self.go_to_submenu('Environments')
        self.env_to_service('test')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'linuxapache'))

        self.delete_service('linuxapache')
        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'linuxapache'))

    @testtools.skip("New UI in progress")
    def test_008_create_and_delete_ad_service(self):
        """
        Test check ability to create and delete active directory service

        Scenario:
            1. Navigate to Environments page
            2. Create environment
            3. Create active directory service in this environment by filling
            the creation form
            4. Delete active directory service from environment
        """
        self.go_to_submenu('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_link_text('Add Application').click()
        self.driver.find_element_by_xpath(
            self.elements.get('apps', 'AD')).click()
        self.create_ad_service('muranotest.domain')

        self.go_to_submenu('Environments')
        self.env_to_service('test')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'muranotest.domain'))

        self.delete_service('muranotest.domain')
        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'muranotest.domain'))

    @testtools.skip("New UI in progress")
    def test_009_create_and_delete_iis_service(self):
        """
        Test check ability to create and delete IIS service

        Scenario:
            1. Navigate to Environments page
            2. Create environment
            3. Create IIS service in this environment by filling
            the creation form
            4. Delete IIS service from environment
        """
        self.go_to_submenu('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_link_text('Add Application').click()
        self.create_iis_service('IISService')

        self.go_to_submenu('Environments')
        self.env_to_service('test')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'IISService'))
        self.delete_service('IISService')
        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'IISService'))

    @testtools.skip("New UI in progress")
    def test_010_create_and_delete_asp_service(self):
        """
        Test check ability to create and delete ASP.Net service

        Scenario:
            1. Navigate to Environments page
            2. Create environment
            3. Create ASP.Net service in this environment by filling
            the creation form
            4. Delete ASP.Net service from environment
        """
        self.go_to_submenu('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_link_text('Add Application').click()
        self.create_asp_service('ASPService')

        self.go_to_submenu('Environments')
        self.env_to_service('test')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'ASPService'))

        self.delete_service('ASPService')
        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'ASPService'))

    @testtools.skip("New UI in progress")
    def test_011_create_and_delete_iisfarm_service(self):
        """
        Test check ability to create and delete IIS Farm service

        Scenario:
            1. Navigate to Environments page
            2. Create environment
            3. Create IIS Farm service in this environment by filling
            the creation form
            4. Delete IIS Farm service from environment
        """
        self.go_to_submenu('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_link_text('Add Application').click()
        self.create_iisfarm_service('IISFarmService')

        self.go_to_submenu('Environments')
        self.env_to_service('test')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'IISFarmService'))

        self.delete_service('IISFarmService')
        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'IISFarmService'))

    @testtools.skip("New UI in progress")
    def test_012_create_and_delete_aspfarm_service(self):
        """
        Test check ability to create and delete ASP.Net Farm service

        Scenario:
            1. Navigate to Environments page
            2. Create environment
            3. Create ASP.Net Farm service in this environment by filling
            the creation form
            4. Delete ASP.Net Farm service from environment
        """
        self.go_to_submenu('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_link_text('Add Application').click()
        self.create_aspfarm_service('ASPFarmService')

        self.go_to_submenu('Environments')
        self.env_to_service('test')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'ASPFarmService'))

        self.delete_service('ASPFarmService')
        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'ASPFarmService'))

    @testtools.skip("New UI in progress")
    def test_013_create_and_delete_mssql_service(self):
        """
        Test check ability to create and delete MSSQL service

        Scenario:
            1. Navigate to Environments page
            2. Create environment
            3. Create MSSQL service in this environment by filling
            the creation form
            4. Delete MSSQL service from environment
        """
        self.go_to_submenu('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_link_text('Add Application').click()
        self.create_mssql_service('MSSQLService')

        self.go_to_submenu('Environments')
        self.env_to_service('test')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'MSSQLService'))

        self.delete_service('MSSQLService')
        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'MSSQLService'))

    @testtools.skip("New UI in progress")
    def test_014_create_and_delete_sql_cluster_service(self):
        """
        Test check ability to create and delete MSSQL cluster service

        Scenario:
            1. Navigate to Environments page
            2. Create environment
            3. Create MSSQL cluster service in this environment by filling
            the creation form
            4. Delete MSSQL cluster service from environment
        """
        self.go_to_submenu('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_link_text('Add Application').click()
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

    @testtools.skip("New UI in progress")
    def test_015_create_and_delete_tomcat_service(self):
        """
        Test check ability to create and delete tomcat service

        Scenario:
            1. Navigate to Environments page
            2. Create environment
            3. Create tomcat service in this environment by filling
            the creation form
            4. Delete tomcat service from environment
        """
        self.go_to_submenu('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_link_text('Add Application').click()
        self.create_postgreSQL_service('posrgreSQL')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'posrgreSQL'))

        self.driver.find_element_by_link_text('Create Service').click()
        self.create_tomcat_service('tomcat-serv', 'posrgreSQL')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'tomcat-serv'))

        self.delete_service('tomcat-serv')
        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'tomcat-serv'))

    @testtools.skip("New UI in progress")
    def test_016_create_and_delete_postgreSQL_service(self):
        """
        Test check ability to create and delete postgreSQL service

        Scenario:
            1. Navigate to Environments page
            2. Create environment
            3. Create postgreSQL service in this environment by filling
            the creation form
            4. Delete postgreSQL service from environment
        """
        self.go_to_submenu('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_link_text('Add Application').click()
        self.create_postgreSQL_service('postgreSQL-serv')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'postgreSQL-serv'))

        self.delete_service('postgreSQL-serv')
        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'postgreSQL-serv'))

    @testtools.skip("New UI in progress")
    def test_017_check_regex_expression_for_ad_name(self):
        """
        Test check that validation of domain name field work and appropriate
        error message is appeared after entering incorrect domain name

        Scenario:
            1. Navigate to Environments page
            2. Create environment and start to create AD service
            3. Set "a" as a domain name and verify error message
            4. Set "aa" as a domain name and check that error message
            didn't appear
            5. Set "@ct!v3" as a domain name and verify error message
            6. Set "active.com" as a domain name and check that error message
            didn't appear
            7. Set "domain" as a domain name and verify error message
            8. Set "domain.com" as a domain name and check that error message
            didn't appear
            9. Set "morethan15symbols.beforedot" as a domain name and
            verify error message
            10. Set "lessthan15.beforedot" as a domain name and check that
            error message didn't appear
            11. Set ".domain.local" as a domain name and
            verify error message
            12. Set "domain.local" as a domain name and check that
            error message didn't appear
        """
        self.go_to_submenu('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_link_text('Add Application').click()
        self.driver.find_element_by_xpath(
            self.elements.get('apps', 'AD')).click()

        self.fill_field(by.By.ID, field='id_0-name', value='a')
        self.assertTrue(self.check_that_error_message_is_correct(
            'Ensure this value has at least 2 characters (it has 1).', 1))

        self.fill_field(by.By.ID, field='id_0-name', value='aa')
        self.assertFalse(self.check_that_error_message_is_correct(
            'Ensure this value has at least 2 characters (it has 1).', 1))

        self.fill_field(by.By.ID, field='id_0-name', value='@ct!v3')
        self.assertTrue(self.check_that_error_message_is_correct(
            'Only letters, numbers and dashes in the middle are allowed.', 1))

        self.fill_field(by.By.ID, field='id_0-name', value='active.com')
        self.assertFalse(self.check_that_error_message_is_correct(
            'Only letters, numbers and dashes in the middle are allowed.', 1))

        self.fill_field(by.By.ID, field='id_0-name', value='domain')
        self.assertTrue(self.check_that_error_message_is_correct(
            'Single-level domain is not appropriate.', 1))

        self.fill_field(by.By.ID, field='id_0-name', value='domain.com')
        self.assertFalse(self.check_that_error_message_is_correct(
            'Single-level domain is not appropriate.', 1))

        self.fill_field(by.By.ID, field='id_0-name',
                        value='morethan15symbols.beforedot')
        self.assertTrue(self.check_that_error_message_is_correct(
            'NetBIOS name cannot be shorter than'
            ' 1 symbol and longer than 15 symbols.', 1))

        self.fill_field(by.By.ID, field='id_0-name',
                        value='lessthan15.beforedot')
        self.assertFalse(self.check_that_error_message_is_correct(
            'NetBIOS name cannot be shorter than'
            ' 1 symbol and longer than 15 symbols.', 1))

        self.fill_field(by.By.ID, field='id_0-name', value='.domain.local')
        self.assertTrue(self.check_that_error_message_is_correct(
            'Period characters are allowed only when '
            'they are used to delimit the components of domain style names', 1))

        self.fill_field(by.By.ID, field='id_0-name', value='domain.local')
        self.assertFalse(self.check_that_error_message_is_correct(
            'Period characters are allowed only when '
            'they are used to delimit the components of domain style names', 1))

    @testtools.skip("New UI in progress")
    def test_018_check_regex_expression_for_iis_name(self):
        """
        Test check that validation of iis name field work and appropriate
        error message is appeared after entering incorrect name

        Scenario:
            1. Navigate to Environments page
            2. Create environment and start to create IIS service
            3. Set "a" as a iis name and verify error message
            4. Set "aa" as a iis name and check that error message
            didn't appear
            5. Set "S3rv!$" as a iis name and verify error message
            6. Set "Service" as a iis name and check that error message
            didn't appear
        """
        self.go_to_submenu('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_link_text('Add Application').click()
        self.driver.find_element_by_xpath(
            self.elements.get('apps', 'IIS')).click()

        self.fill_field(by.By.ID, field='id_0-name', value='a')
        self.assertTrue(self.check_that_error_message_is_correct(
            'Ensure this value has at least 2 characters (it has 1).', 1))

        self.fill_field(by.By.ID, field='id_0-name', value='aa')
        self.assertFalse(self.check_that_error_message_is_correct(
            'Ensure this value has at least 2 characters (it has 1).', 1))

        self.fill_field(by.By.ID, field='id_0-name', value='S3rv!$')
        self.assertTrue(self.check_that_error_message_is_correct(
            'Just letters, numbers, underscores and hyphens are allowed.', 1))

        self.fill_field(by.By.ID, field='id_0-name', value='Service')
        self.assertFalse(self.check_that_error_message_is_correct(
            'Just letters, numbers, underscores and hyphens are allowed.', 1))

    @testtools.skip("New UI in progress")
    def test_019_check_regex_expression_for_git_repo_field(self):
        """
        Test check that validation of git repository field work and appropriate
        error message is appeared after entering incorrect url

        Scenario:
            1. Navigate to Environments page
            2. Create environment and start to create ASP.Net service
            3. Set "a" as a git repository url and verify error message
            4. Set "://@:" as a git repository url and verify error message
        """
        self.go_to_submenu('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_link_text('Add Application').click()
        self.driver.find_element_by_xpath(
            self.elements.get('apps', 'ASP')).click()

        self.fill_field(by.By.ID, field='id_0-repository', value='a')
        self.assertTrue(self.check_that_error_message_is_correct(
            'Enter correct git repository url', 4))

        self.fill_field(by.By.ID, field='id_0-repository', value='://@:')
        self.assertTrue(self.check_that_error_message_is_correct(
            'Enter correct git repository url', 4))

    @testtools.skip("New UI in progress")
    def test_020_check_validation_for_hostname_template_field(self):
        """
        Test check that validation of hostname template field work and
        appropriate error message is appeared after entering incorrect name

        Scenario:
            1. Navigate to Environments page
            2. Create environment and start to create demo service
            3. Set "demo" as a hostname template name a and verify error message
            4. Set "demo" as a hostname template name and change number of
            instances from 2 to 1 and check that there is no error message
        """
        self.go_to_submenu('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_link_text('Add Application').click()
        self.driver.find_element_by_xpath(
            self.elements.get('apps', 'Demo')).click()

        self.fill_field(by.By.ID, 'id_0-name', 'demo')
        self.fill_field(by.By.ID, 'id_0-unitNamingPattern', 'demo')

        xpath = ".//*[@id='create_service_form']/div[1]/div[1]/fieldset/div[1]"

        self.driver.find_element_by_xpath(
            self.elements.get('button', 'ButtonSubmit')).click()
        self.assertTrue(self.check_element_on_page(by.By.XPATH, xpath))

        self.fill_field(by.By.ID, 'id_0-dcInstances', value='1')
        self.driver.find_element_by_xpath(
            self.elements.get('button', 'ButtonSubmit')).click()

        WebDriverWait(self.driver, 10).until(lambda s: s.find_element(
            by.By.ID, '1-osImage').is_displayed())

    @testtools.skip("New UI in progress")
    def test_021_check_bool_field_validation(self):
        """
        Test check that validation of bool field work

        Scenario:
            1. Navigate to Environments page
            2. Create environment and start to create mssql cluster service
            3. Select externalAD and fill fields with incorrect values
            4. Unselect externalAD and click on Next, second step of wizard
            should appears
        """
        self.go_to_submenu('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_id('services__action_CreateService').click()

        self.select_from_list('service_choice-service', 'MS SQL Server Cluster')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        sql_cluster = 'id_msSqlClusterServer-0'

        self.fill_field(by.By.ID, '{0}-name'.format(sql_cluster), 'ms-sql')
        self.fill_field(by.By.ID,
                        '{0}-adminPassword'.format(sql_cluster),
                        'P@ssw0rd')
        self.fill_field(by.By.ID,
                        '{0}-adminPassword-clone'.format(sql_cluster),
                        'P@ssw0rd')
        self.driver.find_element_by_id(
            '{0}-externalAD'.format(sql_cluster)).click()
        self.fill_field(by.By.ID,
                        '{0}-domainAdminUserName'.format(sql_cluster),
                        'user')
        self.fill_field(by.By.ID,
                        '{0}-domainAdminPassword'.format(sql_cluster),
                        'P@ssw0rd')
        self.fill_field(by.By.ID,
                        '{0}-domainAdminPassword-clone'.format(sql_cluster),
                        'anotherP@ssw0rd')
        self.fill_field(by.By.ID,
                        '{0}-saPassword'.format(sql_cluster),
                        'P@ssw0rd')
        self.fill_field(by.By.ID,
                        '{0}-saPassword-clone'.format(sql_cluster),
                        'P@ssw0rd')

        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()
        self.assertTrue(self.check_that_alert_message_is_appeared(
            'Active Directory Passwords don\'t match'))

        self.driver.find_element_by_id(
            '{0}-externalAD'.format(sql_cluster)).click()

        self.assertTrue(self.check_that_error_message_is_correct(
            'This field is required.', 1))

    @testtools.skip("New UI in progress")
    def test_022_positive_scenario_1_for_the_MS_SQL_Cluster_Form(self):
        """
        Test check one possible scenario of creation mssql cluster

        Scenario:
            1. Navigate to Environments page
            2. Create environment and start to create mssql cluster service
            3. External AD and Mixed-Mode Auth checkboxes
            are not selected. User select created earlier domain.
        """
        self.go_to_submenu('Environments')
        self.create_environment('scenario_1')
        self.env_to_service('scenario_1')

        self.create_ad_service('activeDirectory.mssql')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'activeDirectory.mssql'))

        self.driver.find_element_by_link_text('Create Service').click()

        self.select_from_list('service_choice-service', 'MS SQL Server Cluster')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        sql_cluster = 'id_msSqlClusterServer-0'

        self.fill_field(by.By.ID, '{0}-name'.format(sql_cluster), 'ms-sql')
        self.fill_field(by.By.ID,
                        '{0}-adminPassword'.format(sql_cluster),
                        'P@ssw0rd')
        self.fill_field(by.By.ID,
                        '{0}-adminPassword-clone'.format(sql_cluster),
                        'P@ssw0rd')

        self.select_from_list('msSqlClusterServer-0-domain',
                              'activeDirectory.mssql')

        self.driver.find_element_by_id(
            '{0}-mixedModeAuth'.format(sql_cluster)).click()

        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()
        self.assertTrue(self.check_element_on_page(
            by.By.ID, 'id_msSqlClusterServer-1-clusterIp'))

    @testtools.skip("New UI in progress")
    def test_023_positive_scenario_2_for_the_MS_SQL_Cluster_Form(self):
        """
        Test check one possible scenario of creation mssql cluster

        Scenario:
            1. Navigate to Environments page
            2. Create environment and start to create mssql cluster service
            3. External AD field is selected (and user fill
            all required fields here) and Mixed-Mode Auth checkbox
            is not selected.
        """
        self.go_to_submenu('Environments')
        self.create_environment('scenario_2')
        self.env_to_service('scenario_2')

        self.driver.find_element_by_link_text('Create Service').click()

        self.select_from_list('service_choice-service', 'MS SQL Server Cluster')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        sql_cluster = 'id_msSqlClusterServer-0'

        self.fill_field(by.By.ID, '{0}-name'.format(sql_cluster), 'ms-sql')
        self.fill_field(by.By.ID,
                        '{0}-adminPassword'.format(sql_cluster),
                        'P@ssw0rd')
        self.fill_field(by.By.ID,
                        '{0}-adminPassword-clone'.format(sql_cluster),
                        'P@ssw0rd')

        self.driver.find_element_by_id(
            '{0}-externalAD'.format(sql_cluster)).click()
        self.fill_field(by.By.ID,
                        '{0}-domainAdminUserName'.format(sql_cluster),
                        'user')
        self.fill_field(by.By.ID,
                        '{0}-domainAdminPassword'.format(sql_cluster),
                        'P@ssw0rd')
        self.fill_field(by.By.ID,
                        '{0}-domainAdminPassword-clone'.format(sql_cluster),
                        'P@ssw0rd')

        self.driver.find_element_by_id(
            '{0}-mixedModeAuth'.format(sql_cluster)).click()

        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()
        self.assertTrue(self.check_element_on_page(
            by.By.ID, 'id_msSqlClusterServer-1-clusterIp'))

    @testtools.skip("New UI in progress")
    def test_024_positive_scenario_3_for_the_MS_SQL_Cluster_Form(self):
        """
        Test check one possible scenario of creation mssql cluster

        Scenario:
            1. Navigate to Environments page
            2. Create environment and start to create mssql cluster service
            3. External AD and Mixed-Mode Auth checkboxes are selected.
            User have to fill all required fields.
        """
        self.go_to_submenu('Environments')
        self.create_environment('scenario_3')
        self.env_to_service('scenario_3')

        self.driver.find_element_by_link_text('Create Service').click()

        self.select_from_list('service_choice-service', 'MS SQL Server Cluster')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        sql_cluster = 'id_msSqlClusterServer-0'

        self.fill_field(by.By.ID, '{0}-name'.format(sql_cluster), 'ms-sql')
        self.fill_field(by.By.ID,
                        '{0}-adminPassword'.format(sql_cluster),
                        'P@ssw0rd')
        self.fill_field(by.By.ID,
                        '{0}-adminPassword-clone'.format(sql_cluster),
                        'P@ssw0rd')

        self.driver.find_element_by_id('{0}-externalAD').click()
        self.fill_field(by.By.ID,
                        '{0}-domainAdminUserName'.format(sql_cluster),
                        'user')
        self.fill_field(by.By.ID,
                        '{0}-domainAdminPassword'.format(sql_cluster),
                        'P@ssw0rd')
        self.fill_field(by.By.ID,
                        '{0}-domainAdminPassword-clone'.format(sql_cluster),
                        'P@ssw0rd')

        self.fill_field(by.By.ID,
                        '{0}-saPassword'.format(sql_cluster),
                        'P@ssw0rd')
        self.fill_field(by.By.ID,
                        '{0}-saPassword-clone'.format(sql_cluster),
                        'P@ssw0rd')

        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()
        self.assertTrue(self.check_element_on_page(
            by.By.ID, 'id_msSqlClusterServer-1-clusterIp'))

    @testtools.skip("There are no default packages in Murano")
    def test_025_modify_package_name(self):
        """
        Test check ability to change name of the package

        Scenario:
            1. Navigate to 'Package Definitions' page
            2. Select package and click on 'Modify Package'
            3. Rename package
        """
        self.navigate_to('Manage')
        self.go_to_submenu('Package Definitions')
        self.select_action_for_package('NAME',
                                       'modify_package')
        self.fill_field(by.By.ID, 'id_name', 'NAME-modified')
        self.driver.find_element_by_xpath(
            self.elements.get('button', 'InputSubmit')).click()

        self.assertTrue(self.check_element_on_page(
            by.By.XPATH, './/*[@data-display="NAME-modified"]'))

        self.select_action_for_package('NAME-modified',
                                       'modify_package')
        self.fill_field(by.By.ID, 'id_name', 'NAME')
        self.driver.find_element_by_xpath(
            self.elements.get('button', 'InputSubmit')).click()

        self.assertTrue(self.check_element_on_page(
            by.By.XPATH, './/*[@data-display="NAME"]'))

    @testtools.skip("There are no default packages in Murano")
    def test_026_modify_description(self):
        """
        Test check ability to change description of the package

        Scenario:
            1. Navigate to 'Package Definitions' page
            2. Select package and click on 'Modify Package'
            3. Change description
        """
        self.navigate_to('Manage')
        self.go_to_submenu('Package Definitions')
        self.select_action_for_package('NAME',
                                       'modify_package')

        self.fill_field(by.By.ID, 'id_description', 'New Description')
        self.driver.find_element_by_xpath(
            self.elements.get('button', 'InputSubmit')).click()

        self.navigate_to('Application_Catalog')
        self.go_to_submenu('Applications')

        self.check_element_on_page(
            "XPATH_OF_NAME",
            'New Description')

    @testtools.skip("There are no default packages in Murano")
    def test_027_modify_package_add_tag(self):
        """
        Test check ability to add file in composed service

        Scenario:
            1. Navigate to 'Package Definitions' page
            2. Click on "Compose Service"  and create new service
            3. Manage composed service: add file
        """
        self.navigate_to('Manage')
        self.go_to_submenu('Package Definitions')
        self.select_action_for_package('NAME',
                                       'modify_package')

        self.fill_field(by.By.ID, 'id_tags', 'TEST_TAG')
        self.driver.find_element_by_xpath(
            self.elements.get('button', 'InputSubmit')).click()

        app_id = self.get_element_id('NAME')

        self.navigate_to('Application_Catalog')
        self.go_to_submenu('Applications')
        self.select_and_click_action_for_app('details', app_id)
        self.check_element_on_page(
            'XPATH_OF_AREA',
            'TEST_TAG')

    @testtools.skip("There are no default packages in Murano")
    def test_028_download_package(self):
        """
        Test check ability to download service from repository

        Scenario:
            1. Navigate to 'Package Definitions' page
            2. Select Demo service and click on "More>Download"
        """
        self.navigate_to('Manage')
        self.go_to_submenu('Package Definitions')

        self.select_action_for_package('demoService', 'more')
        self.select_action_for_package('demoService', 'download_service')

    @testtools.skip("There are no default packages in Murano")
    def test_029_upload_package_add_to_env(self):
        """
        Test check ability to upload package to repository

        Scenario:
            1. Navigate to 'Package Definitions' page
            2. Click on "Upload Package"
            3. Select zip archive with package and category, submit form
        """
        self.navigate_to('Manage')
        self.go_to_submenu('Package Definitions')

        self.click_on_package_action('upload_package')
        self.choose_and_upload_files('PACKAGE.zip')
        self.select_from_list('categories', 'CATEGORY')
        self.driver.find_element_by_xpath(
            self.elements.get('button', 'InputSubmit')).click()

        self.assertTrue(self.check_element_on_page(
            by.By.XPATH, './/*[@data-display="PACKAGE_NAME"]'))

    @testtools.skip("There are no default packages in Murano")
    def test_030_check_opportunity_to_toggle_service(self):
        """
        Test check ability to make package active or inactive

        Scenario:
            1. Navigate to 'Package Definitions' page
            2. Select some package and make it inactive ("More>Toggle Package")
            3. Check that package became inactive
            4. Select some package and make it active ("More>Toggle Package ")
            5. Check that package became active
        """
        self.navigate_to('Manage')
        self.go_to_submenu('Package Definitions')

        self.select_action_for_package('NAME', 'more')
        self.select_action_for_package('NAME', 'toggle_enabled')

        self.assertTrue(self.check_package_parameter('NAME', '3', 'False'))

        self.select_action_for_package('NAME', 'more')
        self.select_action_for_package('NAME', 'toggle_enabled')

        self.assertTrue(self.check_package_parameter('NAME', '3', 'True'))

    @testtools.skip("There are no default packages in Murano")
    def test_031_check_opportunity_to_delete_package(self):
        """
        Test check ability to delete package from database

        Scenario:
            1. Navigate to 'Package Definitions' page
            2. Select some package
            3. Delete this package
        """
        self.navigate_to('Manage')
        self.go_to_submenu('Package Definitions')

        package = self.get_element_id('NAME')
        self.select_and_click_element(package)

        self.click_on_package_action('delete_package')
        self.confirm_deletion()
        self.assertFalse(self.check_element_on_page(
            by.By.XPATH, './/*[@data-display="NAME"]'))

    def test_032_check_application_catalog_panel(self):
        """
        Test checks that 'Applications' panel is operable

        Scenario:
            1. Create environment
            2. Navigate to 'Application Catalog > Applications' panel
        """
        self.go_to_submenu('Applications')
        self.assertTrue(self.check_element_on_page(
            by.By.XPATH, ".//*[@id='content_body']/div[2]/h3[1]"))

    @testtools.skip("There are no default apps in Murano")
    def test_033_env_creation_form_app_catalog_page(self):
        """
        Test checks that app's option 'Add to environment' is operable
        when there is no previously created env. In this case creation of the
        environment should start after clicking 'Add to environment' button

        Scenario:
            1. Navigate to 'Application Catalog > Applications' panel
            2. Click on 'Add to environment' button for some application
            3. Create new environment
            4. Add application in created environment
        """
        self.go_to_submenu('Applications')
        self.driver.find_element_by_link_text('Add to environment').click()

        self.fill_field(by.By.ID, 'id_name', 'test_033')
        self.driver.find_element_by_xpath(
            self.elements.get('button', 'InputSubmit')).click()

        self.navigate_to('Application_Catalog')
        self.go_to_submenu('Environments')
        self.driver.find_element_by_link_text('test_033').click()
        self.assertTrue(
            self.driver.find_element_by_id('services__action_AddApplication'))

    @testtools.skip("There are no default apps in Murano")
    def test_034_check_info_about_app(self):
        """
        Test checks that information about app is available and truly.

        Scenario:
            1. Navigate to 'Application Catalog > Applications' panel
            2. Choose some application and click on 'More info'
            3. Verify info about application
        """
        self.go_to_submenu('Applications')
        self.select_and_click_action_for_app('details', 'NAME')

        self.assertIn('DESCRIPTION', self.driver.page_source)
        self.driver.find_element_by_link_text('Requirements').click()
        self.driver.find_element_by_link_text('License').click()

    def test_035_check_search_option(self):
        """
        Test checks that 'Search' option is operable.

        Scenario:
            1. Navigate to 'Application Catalog > Applications' panel
            2. Click on 'Search' panel
            3. Type name of service that should be founded
            3. Click on 'Go' and check result
        """
        self.go_to_submenu('Applications')
        self.driver.find_element_by_id('MuranoSearchPanelToggle').click()
        self.fill_field(by.By.XPATH, ".//*[@name='search']", 'PARAM')
        self.driver.find_element_by_xpath(
            ".//*[@id='MuranoSearchPanel']/form/button").click()

    @testtools.skip("There are no default apps in Murano")
    def test_036_filter_by_category(self):
        """
        Test checks ability to filter applications by category
        in Application Catalog page

        Scenario:
            1. Navigate to 'Application Catalog' panel
            2. Click on 'Category' panel
            3. Select category and click on it
            4. Verify result
        """
        self.navigate_to('Manage')
        self.go_to_submenu('Package Definition')

        package_category1 = self.get_element_id('PACKAGE_CATEGORY1')
        package_category2 = self.get_element_id('PACKAGE_CATEGORY2')

        self.navigate_to('Application_Catalog')
        self.go_to_submenu('Applications')
        self.driver.find_element_by_id('MuranoCategoriesPanelToggle').click()
        self.driver.find_element_by_link_text('CATEGORY1').click()

        self.assertTrue(self.check_element_on_page(
            by.By.XPATH, "//*[@href='/murano/catalog/details/{1}']".
            format(package_category1)))

        self.driver.find_element_by_id('MuranoCategoriesPanelToggle').click()
        self.driver.find_element_by_link_text('CATEGORY2').click()

        self.assertTrue(self.check_element_on_page(
            by.By.XPATH, "//*[@href='/murano/catalog/details/{1}']".
            format(package_category2)))

    @testtools.skip("There are no default apps in Murano")
    def test_037_check_option_switch_env(self):
        """
        Test checks ability to switch environment and to add app in other env

        Scenario:
            1. Navigate to 'Application Catalog>Environments' panel
            2. Create environment 'env1'
            3. Create environment 'env2'
            4. Navigate to 'Application Catalog>Application Catalog'
            5. Click on 'Environment' panel
            6. Switch to env2
            7. Add application in env2
            8. Navigate to 'Application Catalog>Environments' and go to the env2
            9. Check that added application is here
        """
        self.go_to_submenu('Environments')
        self.create_environment('env1')
        self.create_environment('env2')
        self.navigate_to('Application_Catalog')
        self.go_to_submenu('Applications')
        self.driver.find_element_by_link_text('Environment').click()
        self.driver.find_element_by_link_text('env2').click()

        self.select_and_click_action_for_app('add', 'NAME')
        self.create_iis_service('IISService')

        self.go_to_submenu('Environments')
        self.env_to_service('env2')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'IISService'))