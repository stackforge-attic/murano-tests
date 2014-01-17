#    Copyright (c) 2013 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from ConfigParser import ConfigParser
from os import getcwd
from os.path import join

from robot.libraries.BuiltIn import BuiltIn


_settingsFileName = 'settings.ini'


class _SettingsReader(object):
    """ 'settings.ini' driver. """

    @staticmethod
    def read():
        """
            Loads default variables from the 'resources/settings.ini' file.

            Arguments:
            - None.

            Return:
            - None.
        """
        try:
            p = BuiltIn().get_variable_value('${resources_path}')
            if p is not None:
                _settingsFullFileName = join(p, _settingsFileName)
            else:
                _settingsFullFileName = join(getcwd(), 'resources',
                                             _settingsFileName)

            conf = ConfigParser()
            conf.read(_settingsFullFileName)

            for setting in conf.options('default'):
                BuiltIn().set_global_variable('${%s}' % setting,
                                              conf.get('default', setting))
        except:
            pass
