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
        self.navigate_to('Environments')
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
        self.navigate_to('Environments')
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
        self.navigate_to('Images')
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
        self.navigate_to('Images')
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
        self.navigate_to('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.create_demo_service('DemoService')
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
        self.navigate_to('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.create_linux_telnet('linuxtelnet')
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
        self.navigate_to('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.create_linux_apache('linuxapache')
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
        self.navigate_to('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_link_text('Add Application').click()
        self.driver.find_element_by_xpath(
            self.elements.get('apps', 'AD')).click()

        self.create_ad_service('muranotest.domain')
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
        self.navigate_to('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_link_text('Add Application').click()
        self.driver.find_element_by_xpath(
            self.elements.get('apps', 'IIS')).click()

        self.create_iis_service('IISService')
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
        self.log_in()
        self.navigate_to('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.create_asp_service('ASPService')
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
        self.navigate_to('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.create_iisfarm_service('IISFarmService')
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
        self.navigate_to('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.create_aspfarm_service('ASPFarmService')
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
        self.navigate_to('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.create_mssql_service('MSSQLService')
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
        self.navigate_to('Environments')
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
        self.navigate_to('Environments')
        self.create_environment('test')
        self.env_to_service('test')

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
        self.navigate_to('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_link_text('Create Service').click()
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
        self.navigate_to('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_id('services__action_CreateService').click()

        self.select_from_list('service_choice-service', 'Active Directory')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        service_name = 'id_activeDirectory-0-name'

        self.fill_field(by.By.ID, field=service_name, value='a')
        self.assertTrue(self.check_that_error_message_is_correct(
            'Ensure this value has at least 2 characters (it has 1).', 1))

        self.fill_field(by.By.ID, field=service_name, value='aa')
        self.assertFalse(self.check_that_error_message_is_correct(
            'Ensure this value has at least 2 characters (it has 1).', 1))

        self.fill_field(by.By.ID, field=service_name, value='@ct!v3')
        self.assertTrue(self.check_that_error_message_is_correct(
            'Only letters, numbers and dashes in the middle are allowed.', 1))

        self.fill_field(by.By.ID, field=service_name, value='active.com')
        self.assertFalse(self.check_that_error_message_is_correct(
            'Only letters, numbers and dashes in the middle are allowed.', 1))

        self.fill_field(by.By.ID, field=service_name, value='domain')
        self.assertTrue(self.check_that_error_message_is_correct(
            'Single-level domain is not appropriate.', 1))

        self.fill_field(by.By.ID, field=service_name, value='domain.com')
        self.assertFalse(self.check_that_error_message_is_correct(
            'Single-level domain is not appropriate.', 1))

        self.fill_field(by.By.ID, field=service_name,
                        value='morethan15symbols.beforedot')
        self.assertTrue(self.check_that_error_message_is_correct(
            'NetBIOS name cannot be shorter than'
            ' 1 symbol and longer than 15 symbols.', 1))

        self.fill_field(by.By.ID, field=service_name,
                        value='lessthan15.beforedot')
        self.assertFalse(self.check_that_error_message_is_correct(
            'NetBIOS name cannot be shorter than'
            ' 1 symbol and longer than 15 symbols.', 1))

        self.fill_field(by.By.ID, field=service_name, value='.domain.local')
        self.assertTrue(self.check_that_error_message_is_correct(
            'Period characters are allowed only when '
            'they are used to delimit the components of domain style names', 1))

        self.fill_field(by.By.ID, field=service_name, value='domain.local')
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
        self.navigate_to('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_id('services__action_CreateService').click()

        self.select_from_list('service_choice-service',
                              'Internet Information Services')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        service_name = 'id_webServer-0-name'

        self.fill_field(by.By.ID, field=service_name, value='a')
        self.assertTrue(self.check_that_error_message_is_correct(
            'Ensure this value has at least 2 characters (it has 1).', 1))

        self.fill_field(by.By.ID, field=service_name, value='aa')
        self.assertFalse(self.check_that_error_message_is_correct(
            'Ensure this value has at least 2 characters (it has 1).', 1))

        self.fill_field(by.By.ID, field=service_name, value='S3rv!$')
        self.assertTrue(self.check_that_error_message_is_correct(
            'Just letters, numbers, underscores and hyphens are allowed.', 1))

        self.fill_field(by.By.ID, field=service_name, value='Service')
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
        self.navigate_to('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_id('services__action_CreateService').click()

        self.select_from_list('service_choice-service', 'ASP.NET Application')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        git_repository = 'id_aspNetApp-0-repository'

        self.fill_field(by.By.ID, field=git_repository, value='a')
        self.assertTrue(self.check_that_error_message_is_correct(
            'Enter correct git repository url', 4))

        self.fill_field(by.By.ID, field=git_repository, value='://@:')
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
        self.navigate_to('Environments')
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_id('services__action_CreateService').click()

        self.select_from_list('service_choice-service', 'Demo Service')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        service = 'id_demoService-0'

        self.fill_field(by.By.ID, '{0}-name'.format(service), 'demo')
        self.fill_field(by.By.ID,
                        '{0}-unitNamingPattern'.format(service),
                        'demo')

        xpath = ".//*[@id='create_service_form']/div[1]/div[1]/fieldset/div[1]"

        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()
        self.assertTrue(self.check_element_on_page(by.By.XPATH, xpath))

        self.fill_field(by.By.ID, '{0}-dcInstances'.format(service), value='1')
        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()

        WebDriverWait(self.driver, 10).until(lambda s: s.find_element(
            by.By.ID, 'demoService-1-osImage').is_displayed())

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
        self.navigate_to('Environments')
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
        self.navigate_to('Environments')
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
        self.navigate_to('Environments')
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
        self.navigate_to('Environments')
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

    @testtools.skip("New UI in progress")
    def test_025_check_opportunity_to_compose_a_new_service(self):
        """
        Test check ability to compose new service via Murano Repository

        Scenario:
            1. Navigate to Package Definitions page
            2. Click on "Compose Service"  and create new service
        """
        self.navigate_to('Package Definitions')
        self.compose_trivial_service('composedService')
        self.assertTrue(self.check_element_on_page(
            by.By.XPATH, './/*[@data-display="composedService"]'))

    @testtools.skip("New UI in progress")
    def test_026_modify_service_name(self):
        """
        Test check ability to change name of the composed service

        Scenario:
            1. Navigate to Package Definitions page
            2. Click on "Compose Service"  and create new service
            3. Rename composed service
        """
        self.navigate_to('Package Definitions')
        self.compose_trivial_service('forModification')
        self.assertTrue(self.check_element_on_page(
            by.By.XPATH, './/*[@data-display="forModification"]'))

        self.select_action_for_service('forModificationService',
                                       'modify_service')
        self.fill_field(by.By.ID, 'id_service_display_name', 'modifiedService')
        submit_button = self.elements.get('button', 'InputSubmit')
        self.driver.find_element_by_xpath(submit_button).click()

        self.assertTrue(self.check_element_on_page(
            by.By.XPATH, './/*[@data-display="modifiedService"]'))

    @testtools.skip("New UI in progress")
    def test_027_modify_description(self):
        """
        Test check ability to change description of the composed service

        Scenario:
            1. Navigate to Package Definitions page
            2. Click on "Compose Service"  and create new service
            3. Change description of composed service
        """
        self.navigate_to('Package Definitions')
        self.compose_trivial_service('forModification')
        self.assertTrue(self.check_element_on_page(
            by.By.XPATH, './/*[@data-display="forModification"]'))

        self.select_action_for_service('forModificationService',
                                       'modify_service')

        self.fill_field(by.By.ID, 'id_description', 'New Description')
        submit_button = self.elements.get('button', 'InputSubmit')
        self.driver.find_element_by_xpath(submit_button).click()
        self.select_action_for_service('forModificationService', 'more')
        self.select_action_for_service('forModificationService',
                                       'manage_service')
        self.check_element_on_page(
            ".//*[@id='main_content']/div[3]/dl/dd[4]",
            'New Description')

    @testtools.skip("New UI in progress")
    def test_028_check_opportunity_to_select_composed_service(self):
        """
        Test check ability to add composed service in the environment

        Scenario:
            1. Navigate to Package Definitions page
            2. Click on "Compose Service"  and create new service
            3. Navigate to Environments page
            4. Create environment and add in this env created service
        """
        self.navigate_to('Package Definitions')
        self.compose_trivial_service('TEST')
        self.assertTrue(self.check_element_on_page(
            by.By.XPATH, './/*[@data-display="TEST"]'))

        self.navigate_to('Environments')
        self.create_environment('env')
        self.env_to_service('env')
        self.driver.find_element_by_link_text('Create Service').click()
        self.select_from_list('service_choice-service', 'TEST')

        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        next_ = "/html/body/div[3]/div/form/div[2]/input[2]"
        self.assertTrue(self.check_element_on_page(by.By.XPATH, next_))

    @testtools.skip("New UI in progress")
    def test_029_modify_service_add_file(self):
        """
        Test check ability to add file in composed service

        Scenario:
            1. Navigate to 'Package Definitions' page
            2. Click on "Compose Service"  and create new service
            3. Manage composed service: add file
        """
        self.navigate_to('Package Definitions')
        self.compose_trivial_service('TEST')

        self.select_action_for_service('TESTService', 'modify_service')

        self.driver.find_element_by_link_text('Scripts').click()
        self.driver.find_element_by_xpath(
            ".//*[@name = 'scripts@@scripts##"
            "Get-DnsListeningIpAddress.ps1@@selected']").click()

        submit_button = self.elements.get('button', 'InputSubmit')
        self.driver.find_element_by_xpath(submit_button).click()

        self.select_action_for_service('TESTService', 'more')
        self.select_action_for_service('TESTService', 'manage_service')
        self.assertTrue(self.check_element_on_page(
            by.By.XPATH, ".//*[@id='scripts__row__scripts##"
                         "Get-DnsListeningIpAddress.ps1']"))

    @testtools.skip("New UI in progress")
    def test_030_download_service(self):
        """
        Test check ability to download service from repository

        Scenario:
            1. Navigate to 'Package Definitions' page
            2. Select Demo service and click on "More>Download"
        """
        self.navigate_to('Package Definitions')

        self.select_action_for_service('demoService', 'more')
        self.select_action_for_service('demoService', 'download_service')

    @testtools.skip("New UI in progress")
    def test_031_upload_service_to_repository(self):
        """
        Test check ability to upload service from repository

        Scenario:
            1. Navigate to 'Package Definitions' page
            2. Click on "Upload Service"
            3. Select tar.gz archive with service and submit form
        """
        self.driver.find_element_by_link_text('Package Definitions').click()

        self.click_on_service_catalog_action('upload_service')
        self.choose_and_upload_files('myService.tar.gz')
        self.select_and_click_element('Upload')

        self.assertTrue(self.check_element_on_page(
            by.By.XPATH, './/*[@data-display="My Service"]'))

    @testtools.skip("New UI in progress")
    def test_032_manage_service_upload_file(self):
        """
        Test check ability to upload service from repository

        Scenario:
            1. Navigate to 'Package Definitions' page
            2. Compose new service
            3. Manage composed service: upload new file to this service
        """
        self.navigate_to('Package Definitions')
        self.compose_trivial_service('TEST')

        self.select_action_for_service('TESTService', 'more')
        self.select_action_for_service('TESTService', 'manage_service')

        self.driver.find_element_by_id('scripts__action_upload_file2').click()
        self.choose_and_upload_files('myScript.ps1')
        self.select_and_click_element('Upload')

        self.assertTrue(self.check_element_on_page(
            by.By.XPATH, ".//*[@id='scripts__row__scripts##myScript.ps1']"))

    @testtools.skip("New UI in progress")
    def test_033_manage_files_upload_delete_heat_template(self):
        """
        Test check ability to upload heat template to repository and delete
        this file

        Scenario:
            1. Navigate to Package Definitions page
            2. Click on "Manage Files"
            3. Select file and type of the file "Heat Template"
            4. Upload file to repository
            5. Find uploaded file in appropriate category and delete it
            from repository
        """
        self.navigate_to('Package Definitions')

        self.click_on_service_catalog_action('manage_files')
        self.driver.find_element_by_id(
            'manage_files__action_upload_file').click()

        self.choose_and_upload_files('myHeatTemplate.template')
        self.select_and_click_element('Upload')

        self.select_and_click_element('heat')
        self.assertTrue(self.check_element_on_page(
            by.By.XPATH,
            ".//*[@id='manage_files__row__heat##myHeatTemplate.template']"))

        self.select_and_click_element('heat##myHeatTemplate.template')
        self.driver.find_element_by_id(
            'manage_files__action_delete_file').click()

        self.confirm_deletion()

        self.assertFalse(self.check_element_on_page(
            by.By.XPATH, ".//*[@id='manage_files__row__heat##"
                         "myHeatTemplate.template']"))

    @testtools.skip("New UI in progress")
    def test_034_manage_files_upload_delete_agent_template(self):
        """
        Test check ability to upload agent template to repository and delete
        this file

        Scenario:
            1. Navigate to 'Package Definitions' page
            2. Click on "Manage Files"
            3. Select file and type of the file "Agent Template"
            4. Upload file to repository
            5. Find uploaded file in appropriate category and delete it
            from repository
        """
        self.navigate_to('Package Definitions')

        self.click_on_service_catalog_action('manage_files')
        self.driver.find_element_by_id(
            'manage_files__action_upload_file').click()

        self.choose_and_upload_files('myAgentTemplate.template')
        self.select_from_list('data_type', 'Murano Agent template')
        self.select_and_click_element('Upload')

        self.select_and_click_element('agent')
        self.assertTrue(self.check_element_on_page(
            by.By.XPATH,
            ".//*[@id='manage_files__row__agent##myAgentTemplate.template']"))

        self.select_and_click_element('agent##myAgentTemplate.template')
        self.driver.find_element_by_id(
            'manage_files__action_delete_file').click()

        self.confirm_deletion()

        self.assertFalse(self.check_element_on_page(
            by.By.XPATH, ".//*[@id='manage_files__row__agent##"
                         "myAgentTemplate.template']"))

    @testtools.skip("New UI in progress")
    def test_035_manage_files_upload_delete_ui_file(self):
        """
        Test check ability to upload ui_file to repository and delete
        this file

        Scenario:
            1. Navigate to 'Package Definitions' page
            2. Click on "Manage Files"
            3. Select file and type of the file "UI Definition (*.yaml)"
            4. Upload file to repository
            5. Find uploaded file in appropriate category and delete it
            from repository
        """
        self.navigate_to('Package Definitions')

        self.click_on_service_catalog_action('manage_files')
        self.driver.find_element_by_id(
            'manage_files__action_upload_file').click()

        self.choose_and_upload_files('myYaml.yaml')
        self.select_from_list('data_type', 'UI Definition (*.yaml)')
        self.select_and_click_element('Upload')

        self.select_and_click_element('ui')
        self.assertTrue(self.check_element_on_page(
            by.By.XPATH,
            ".//*[@id='manage_files__row__ui##myYaml.yaml']"))

        self.select_and_click_element('ui##myYaml.yaml')
        self.driver.find_element_by_id(
            'manage_files__action_delete_file').click()

        self.confirm_deletion()

        self.assertFalse(self.check_element_on_page(
            by.By.XPATH, ".//*[@id='manage_files__row__ui##"
                         "myYaml.yaml']"))

    def test_036_check_cannot_add_second_ui_in_service(self):
        """
        Test check that adding of second ui file in service is prohibited

        Scenario:
            1. Navigate to 'Package Definitions' page
            2. Compose new service "TEST"
            2. Navigate to 'Manage Service: TEST Service' page
            ("More>Manage Service" for test service)
            3. Check that "+ UI Files" button is absent
        """
        self.navigate_to('Package Definitions')
        self.compose_trivial_service('TEST')

        self.select_action_for_service('TESTService', 'more')
        self.select_action_for_service('TESTService', 'manage_service')

        self.assertFalse(self.check_element_on_page(by.By.LINK_TEXT,
                                                    'UI Files'))

    @testtools.skip("New UI in progress")
    def test_037_check_opportunity_to_toggle_service(self):
        """
        Test check ability to make service active or inactive

        Scenario:
            1. Navigate to 'Package Definitions' page
            2. Select Demo service and make it inactive ("More>Toggle Service")
            3. Check that service became inactive
            4. Select Demo service and make it active ("More>Toggle Service")
            5. Check that service became active
        """
        self.navigate_to('Package Definitions')

        self.select_action_for_service('demoService', 'more')
        self.select_action_for_service('demoService', 'toggle_enabled')

        self.assertTrue(self.check_service_parameter(
            'service_catalog', 'demoService', '3', 'False'))

        self.select_action_for_service('demoService', 'more')
        self.select_action_for_service('demoService', 'toggle_enabled')

        self.assertTrue(self.check_service_parameter(
            'service_catalog', 'demoService', '3', 'True'))

    @testtools.skip("New UI in progress")
    def test_038_delete_component_from_existing_service(self):
        """
        Test check ability to delete component from existing service

        Scenario:
            1. Navigate to 'Package Definitions' page
            2. Select Demo service and navigate to service info page
            ("More>Manage Service")
            3. Select one of service's file
            4. Delete this file
        """
        self.navigate_to('Package Definitions')

        self.select_action_for_service('demoService', 'more')
        self.select_action_for_service('demoService', 'manage_service')

        self.select_and_click_element('agent##Demo.template')

        self.assertTrue(self.check_element_on_page(
            by.By.XPATH, ".//*[@id='agent__row__agent##Demo.template']"))

        self.driver.find_element_by_id(
            'agent__action_delete_file_from_service').click()
        self.confirm_deletion()

        self.assertFalse(self.check_element_on_page(
            by.By.XPATH, ".//*[@id='agent__row__agent##Demo.template']"))

    @testtools.skip("New UI in progress")
    def test_039_check_opportunity_to_delete_composed_service(self):
        """
        Test check ability to delete composed service

        Scenario:
            1. Navigate to 'Package Definitions' page
            2. Compose new service
            3. Select composed service
            4. Delete this service
        """
        self.navigate_to('Package Definitions')
        self.compose_trivial_service('ForDeletion')
        self.assertTrue(self.check_element_on_page(
            by.By.XPATH, './/*[@data-display="ForDeletion"]'))

        self.driver.refresh()
        self.select_and_click_element('ForDeletionService')

        self.click_on_service_catalog_action('delete_service')
        self.confirm_deletion()
        self.assertFalse(self.check_element_on_page(
            by.By.XPATH, './/*[@data-display="ForDeletion"]'))

    def test_040_check_application_catalog_panel(self):
        """
        Test check that 'Application Catalog' panel is operable

        Scenario:
            1. Create environment
            2. Navigate to 'Application Catalog' panel
        """
        self.navigate_to('Application Catalog')
        self.assertTrue(self.check_element_on_page(
            by.By.XPATH, ".//*[@id='main_content']/div[3]/h3[1]"))

    def test_041_check_package_definition_panel(self):
        """
        Test check that 'Package Definitions' panel is operable

        Scenario:
            1. Create environment
            2. Navigate to 'Package Catalog' panel
        """
        self.navigate_to('Package Definitions')
        self.assertTrue(self.check_element_on_page(
            by.By.XPATH, ".//*[@id='main_content']/div[1]/div[2]/h2"))