import sys
import os
sys.path.append(os.getcwd())

import testtools

from base import UITestCase
import selenium.webdriver.common.by as by
from selenium.webdriver.support.ui import WebDriverWait


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
        self.create_mssql_service('MSSQLService')

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

    def test_check_regex_expression_for_ad_name(self):
        self.log_in()
        self.navigate_to_environments()
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

    def test_check_regex_expression_for_iis_name(self):
        self.log_in()
        self.navigate_to_environments()
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

    def test_check_regex_expression_for_git_repo_field(self):
        self.log_in()
        self.navigate_to_environments()
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

    def test_check_validation_for_hostname_template_field(self):
        self.log_in()
        self.navigate_to_environments()
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_id('services__action_CreateService').click()

        self.select_from_list('service_choice-service', 'Demo Service')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        self.fill_field(by.By.ID, field='id_demoService-0-name', value='demo')
        self.fill_field(by.By.ID, field='id_demoService-0-unitNamingPattern',
                        value='demo')

        xpath = ".//*[@id='create_service_form']/div[1]/div[1]/fieldset/div[1]"

        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()
        self.assertTrue(self.check_element_on_page(by.By.XPATH, xpath))

        self.fill_field(by.By.ID, field='id_demoService-0-dcInstances',
                        value='1')
        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()

        id = 'id_demoService-1-osImage'
        WebDriverWait(self.driver, 10).until(lambda s: s.find_element(
            by.By.ID, id).is_displayed())

    def test_check_bool_field_validation(self):
        self.log_in()
        self.navigate_to_environments()
        self.create_environment('test')
        self.env_to_service('test')

        self.driver.find_element_by_id('services__action_CreateService').click()

        self.select_from_list('service_choice-service', 'MS SQL Server Cluster')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        self.fill_field(by.By.ID, 'id_msSqlClusterServer-0-name', 'ms-sql')
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-0-adminPassword', 'P@ssw0rd')
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-0-adminPassword-clone', 'P@ssw0rd')

        self.driver.find_element_by_id(
            'id_msSqlClusterServer-0-externalAD').click()
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-0-domainAdminUserName', 'user')
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-0-domainAdminPassword', 'P@ssw0rd')
        self.fill_field(by.By.ID,
                        'id_msSqlClusterServer-0-domainAdminPassword-clone',
                        'anotherP@ssw0rd')
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-0-saPassword', 'P@ssw0rd')
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-0-saPassword-clone', 'P@ssw0rd')
        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()
        self.assertTrue(self.check_that_alert_message_is_appeared(
            'Active Directory Passwords don\'t match'))

        self.driver.find_element_by_id(
            'id_msSqlClusterServer-0-externalAD').click()

        self.assertTrue(self.check_that_error_message_is_correct(
            'This field is required.', 1))

    def test_positive_scenario_1_for_the_MS_SQL_Cluster_Form(self):
        """
            Scenario 1: External AD and Mixed-Mode Auth checkboxes
            are not selected. User select created earlier domain.
        """

        self.log_in()
        self.navigate_to_environments()
        self.create_environment('scenario_1')
        self.env_to_service('scenario_1')

        self.create_ad_service('activeDirectory.mssql')
        self.assertTrue(self.check_element_on_page(by.By.LINK_TEXT,
                                                   'activeDirectory.mssql'))

        self.driver.find_element_by_link_text('Create Service').click()

        self.select_from_list('service_choice-service', 'MS SQL Server Cluster')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        self.fill_field(by.By.ID, 'id_msSqlClusterServer-0-name', 'ms-sql')
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-0-adminPassword', 'P@ssw0rd')
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-0-adminPassword-clone', 'P@ssw0rd')

        self.select_from_list('msSqlClusterServer-0-domain',
                              'activeDirectory.mssql')

        self.driver.find_element_by_id(
            'id_msSqlClusterServer-0-mixedModeAuth').click()

        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()
        self.assertTrue(self.check_element_on_page(
            by.By.ID, 'id_msSqlClusterServer-1-clusterIp'))

    def test_positive_scenario_2_for_the_MS_SQL_Cluster_Form(self):
        """
            Scenario 2: External AD field is selected (and user fill
            all required fields here) and Mixed-Mode Auth checkbox
            is not selected.
        """

        self.log_in()
        self.navigate_to_environments()
        self.create_environment('scenario_2')
        self.env_to_service('scenario_2')

        self.driver.find_element_by_link_text('Create Service').click()

        self.select_from_list('service_choice-service', 'MS SQL Server Cluster')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        self.fill_field(by.By.ID, 'id_msSqlClusterServer-0-name', 'ms-sql')
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-0-adminPassword', 'P@ssw0rd')
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-0-adminPassword-clone', 'P@ssw0rd')

        self.driver.find_element_by_id(
            'id_msSqlClusterServer-0-externalAD').click()
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-0-domainAdminUserName', 'user')
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-0-domainAdminPassword', 'P@ssw0rd')
        self.fill_field(by.By.ID,
                        'id_msSqlClusterServer-0-domainAdminPassword-clone',
                        'P@ssw0rd')

        self.driver.find_element_by_id(
            'id_msSqlClusterServer-0-mixedModeAuth').click()

        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()
        self.assertTrue(self.check_element_on_page(
            by.By.ID, 'id_msSqlClusterServer-1-clusterIp'))

    def test_positive_scenario_3_for_the_MS_SQL_Cluster_Form(self):
        """
            Scenario 3: External AD and Mixed-Mode Auth checkboxes are selected.
            User have to fill all required fields.
        """

        self.log_in()
        self.navigate_to_environments()
        self.create_environment('scenario_3')
        self.env_to_service('scenario_3')

        self.driver.find_element_by_link_text('Create Service').click()

        self.select_from_list('service_choice-service', 'MS SQL Server Cluster')
        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        self.fill_field(by.By.ID, 'id_msSqlClusterServer-0-name', 'ms-sql')
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-0-adminPassword', 'P@ssw0rd')
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-0-adminPassword-clone', 'P@ssw0rd')

        self.driver.find_element_by_id(
            'id_msSqlClusterServer-0-externalAD').click()
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-0-domainAdminUserName', 'user')
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-0-domainAdminPassword', 'P@ssw0rd')
        self.fill_field(by.By.ID,
                        'id_msSqlClusterServer-0-domainAdminPassword-clone',
                        'P@ssw0rd')

        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-0-saPassword', 'P@ssw0rd')
        self.fill_field(
            by.By.ID, 'id_msSqlClusterServer-0-saPassword-clone', 'P@ssw0rd')

        next_button = self.elements.get('button', 'Next2')
        self.driver.find_element_by_xpath(next_button).click()
        self.assertTrue(self.check_element_on_page(
            by.By.ID, 'id_msSqlClusterServer-1-clusterIp'))

    def test_check_opportunity_to_compose_a_new_service(self):
        self.log_in()
        self.driver.find_element_by_link_text('Service Definitions').click()
        self.compose_trivial_service('composedService')
        self.assertTrue(self.check_element_on_page(
            by.By.XPATH, './/*[@data-display="composedService"]'))

    def test_modify_service_name(self):
        self.log_in()
        self.driver.find_element_by_link_text('Service Definitions').click()
        self.compose_trivial_service('forModification')
        self.assertTrue(self.check_element_on_page(
            by.By.XPATH, './/*[@data-display="forModification"]'))

        self.select_action_for_service('forModificationService',
                                       'modify_service')
        self.fill_field(by.By.ID, 'id_service_display_name', 'modifiedService')
        submit_button = self.elements.get('button', 'InputSubmit')
        self.driver.find_element_by_xpath(submit_button).click()

        self.assertTrue(self.check_service_parameter(
            'forModificationService', '2', 'modifiedService'))

    def test_modify_description(self):
        self.log_in()
        self.driver.find_element_by_link_text('Service Definitions').click()
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

    def test_check_opportunity_to_toggle_service(self):
        self.log_in()
        self.driver.find_element_by_link_text('Service Definitions').click()
        self.select_action_for_service('demoService', 'more')
        self.select_action_for_service('demoService', 'toggle_enabled')
        self.assertTrue(
            self.check_service_parameter('demoService', '3', 'False'))
        self.select_action_for_service('demoService', 'more')
        self.select_action_for_service('demoService', 'toggle_enabled')
        self.assertTrue(
            self.check_service_parameter('demoService', '3', 'True'))

    def test_check_opportunity_to_select_composed_service(self):
        self.log_in()
        self.driver.find_element_by_link_text('Service Definitions').click()
        self.compose_trivial_service('TEST')
        self.assertTrue(self.check_element_on_page(
            by.By.XPATH, './/*[@data-display="TEST"]'))

        self.navigate_to_environments()
        self.create_environment('env')
        self.env_to_service('env')
        self.driver.find_element_by_link_text('Create Service').click()
        self.select_from_list('service_choice-service', 'TEST')

        next_button = self.elements.get('button', 'Next')
        self.driver.find_element_by_xpath(next_button).click()

        next_ = "/html/body/div[3]/div/form/div[2]/input[2]"
        self.assertTrue(self.check_element_on_page(by.By.XPATH, next_))

    def test_check_opportunity_to_delete_composed_service(self):
        self.log_in()
        self.driver.find_element_by_link_text('Service Definitions').click()
        self.compose_trivial_service('ForDeletion')
        self.assertTrue(self.check_element_on_page(
            by.By.XPATH, './/*[@data-display="ForDeletion"]'))

        self.select_element('ForDeletionService')
        self.refresh_page()
        self.click_on_service_catalog_action('delete_service')
        self.confirm_deletion()
        self.assertFalse(self.check_element_on_page(
            by.By.XPATH, './/*[@data-display="ForDeletion"]'))

    def test_delete_component_from_existing_service(self):
        self.log_in()
        self.driver.find_element_by_link_text('Service Definitions').click()

        self.select_action_for_service('demoService', 'more')
        self.select_action_for_service('demoService', 'manage_service')

        self.select_element('agent##Demo.template')
        self.refresh_page()
        self.driver.find_element_by_id(
            'agent__action_delete_file_from_service').click()
        self.confirm_deletion()

        self.assertFalse(self.check_element_on_page(
            by.By.XPATH, ".//*[@id='agent__row__agent##Demo.tseemplate']"))

    def test_modify_service_add_file(self):
        self.log_in()
        self.driver.find_element_by_link_text('Service Definitions').click()
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

    def test_download_service(self):
        self.log_in()
        self.driver.find_element_by_link_text('Service Definitions').click()

        self.select_action_for_service('demoService', 'more')
        self.select_action_for_service('demoService', 'download_service')

    def test_upload_service_to_repository(self):
        self.log_in()
        self.driver.find_element_by_link_text('Service Definitions').click()

        self.click_on_service_catalog_action('upload_service')
        self.choose_and_upload_files('myService.tar.gz')

        self.assertTrue(self.check_element_on_page(
            by.By.XPATH, './/*[@data-display="My Service"]'))

    def test_manage_service_upload_file(self):
        self.log_in()
        self.driver.find_element_by_link_text('Service Definitions').click()
        self.compose_trivial_service('TEST')

        self.select_action_for_service('TESTService', 'more')
        self.select_action_for_service('TESTService', 'manage_service')

        self.driver.find_element_by_id('scripts__action_upload_file2').click()
        self.choose_and_upload_files('myScript.ps1')

        self.assertTrue(self.check_element_on_page(
            by.By.XPATH, ".//*[@id='scripts__row__scripts##myScript.ps1']"))

    def test_manage_files_upload_delete_file(self):
        self.log_in()
        self.driver.find_element_by_link_text('Service Definitions').click()

        self.click_on_service_catalog_action('manage_files')
        self.driver.find_element_by_id(
            'manage_files__action_upload_file').click()

        self.choose_and_upload_files('myHeatTemplate.template')

        self.select_element('heat')
        self.assertTrue(self.check_element_on_page(
            by.By.XPATH,
            ".//*[@id='manage_files__row__heat##myHeatTemplate.template']"))

        self.select_element('heat##myHeatTemplate.template')
        self.driver.find_element_by_id(
            'manage_files__action_delete_file').click()

        self.confirm_deletion()

        self.assertFalse(self.check_element_on_page(
            by.By.XPATH, ".//*[@id='manage_files__row__heat##"
                         "myHeatTemplate.template']"))