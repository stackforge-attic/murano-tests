import os
import argparse
import git


parser = argparse.ArgumentParser(
    description="Script for checking requirements")
parser.add_argument("-murano_component",  dest='murano_component',  type=str,
                    help="Name of murano component", default='murano-api')
parser.add_argument("-errors_limit",  dest='errors_limit',  type=int,
                    help="Limit of errors",  default=3)
args = parser.parse_args()

murano_component = args.murano_component
errors_limit = args.errors_limit

__location = os.path.realpath(os.path.join(os.getcwd(),
                                           os.path.dirname(__file__)))
component_requirements = os.path.join(__location, 'requirements.txt')
global_requirements = os.path.join(__location, 'global-requirements.txt')
if not os.path.exists(component_requirements):
    git.Git().clone('https://github.com/stackforge/%s.git' % murano_component)
    component_requirements = os.path.join(__location,
                                          '%s/requirements.txt'
                                          % murano_component)

if not os.path.exists(global_requirements):
    git.Git().clone('https://github.com/openstack/requirements.git')
    global_requirements = os.path.join(__location,
                                       'requirements/global-requirements.txt')

with open(component_requirements, 'r') as comp_reqs, open(
        global_requirements, 'r') as glob_reqs:
    errors = 0
    reqs_list = [x for x in glob_reqs]
    for line in comp_reqs:
        if line not in reqs_list:
            errors += 1
        if errors > errors_limit:
            raise Exception('Too many mismatches')
print ('Count of mismatches = %s' % str(errors))
