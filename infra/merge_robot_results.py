# Copyright (c) 2013 Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License'); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

msg = """
      ### Please use this script for the
      ### XML RobotFramework reports merging:
      ###   python merge_robot_results.py output1.xml output2.xml
      """

### To install requirements:
###    sudo pip install BeautifulSoup4 python-dateutil
import sys
from dateutil import parser
from bs4 import BeautifulSoup


files = []
for i in range(len(sys.argv) - 1):
    try:
        f = open(sys.argv[i + 1], 'r').read()
        res = BeautifulSoup(f)
        files.append(res)
    except:
        print "Incorrect XML file:", sys.argv[i + 1]

if files:
    for test in files[0].robot.suite.find_all('test'):
        for f in files[1:]:
            for retest in f.robot.suite.find_all('test'):
                if test['name'] == retest['name']:
                    test.replace_with(retest)

    files[0].robot.statistics.replace_with('')

    result = open('result.xml', 'w')
    result.write(files[0].prettify())
    result.close()
else:
    print msg
