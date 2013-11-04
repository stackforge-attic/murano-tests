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

# Please, install python before run this script.
# Also, please, do not forget to install the following packages for tests:
# robotframework, robotframework-selenium2library, BeautifulSoup4

from subprocess import Popen
from argparse import ArgumentParser
from time import sleep
from os import listdir
from os.path import join, split


def wait_for_finished(threads):
    """
    Wait until threads finish.
    """
    for ind, t in enumerate(threads):
        if t.poll() is not None:
            threads.pop(ind)
    sleep(1)


s = "This script allows to run Robot Framework tests concurrently."
parser = ArgumentParser(description=s)

parser.add_argument("-n", dest="processes_count",
                    default=1, type=int,
                    help="The number of parallel threads (1 by default).")

req_group = parser.add_mutually_exclusive_group(required=True)

req_group.add_argument('-s', dest='script_name',
                       default=None, type=str,
                       help='The name of file with tests or name pattern.')

req_group.add_argument('-l', dest='scripts_list',
                       default=None, nargs='*',
                       help='Names of test files separated by spaces.')

req_group.add_argument('-d', dest='tests_dir',
                       default=None, type=str,
                       help='The name of directory with tests to be executed.')

parser.add_argument("-t", dest="tag", type=str)

parser.add_argument('-r', dest='reports_dir',
                    default="reports", type=str,
                    help='The directory name with reports '
                         '("reports" directory by default).')

parser.add_argument('--IP', dest='IP', type=str)

args = parser.parse_args()

i = 1
tags_list = []
parallel_script = args.script_name+'_parallel'
o = open(parallel_script,'a') #open for append
for line in open(args.script_name):
   if args.tag in line:
       new_tag = args.tag + str(i)
       line = line.replace(args.tag, new_tag)
       if not new_tag in tags_list:
           tags_list.append(new_tag)
       i += 1
       if i > args.processes_count:
           i = 1
   o.write(line + 'n')
o.close()


cmd = 'pybot -C off -K off -d %s/%s'

# Start all threads with tests.
if args.script_name:
    cmd += ' -i %s --variable IP:' + args.IP + ' '
    cmd += parallel_script + ' >/dev/null 2>&1'
    # Start all threads with tests and ignore empty threads.
    threads = []
    for i, tag in enumerate(tags_list):
        values = (args.reports_dir, i, tag)
        threads.append(Popen(cmd % values, shell=True))
        sleep(5)
        while len(threads) == args.processes_count:
            wait_for_finished(threads)

# Wait for all threads finish.
while len(threads) > 0:
    wait_for_finished(threads)
    sleep(1)
