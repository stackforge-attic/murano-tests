import os
import argparse
import git


parser = argparse.ArgumentParser(
    description="Script for checking requirements")
parser.add_argument("-component",  dest='component',  type=str,
                    help="Name of component", default='murano-api')
parser.add_argument("-errors_limit",  dest='errors_limit',  type=int,
                    help="Limit of errors",  default=3)
parser.add_argument("-requirements_file_name",  dest='requirements_file_name',
                    type=str, help="Name of file with requirements",
                    default='requirements.txt')
args = parser.parse_args()

component = args.component
errors_limit = args.errors_limit
requirements_file_name = args.requirements_file_name

__location = os.path.realpath(os.path.join(os.getcwd(),
                                           os.path.dirname(__file__)))

component_requirements = os.path.join(__location, requirements_file_name)
global_requirements = os.path.join(__location, 'global-requirements.txt')

if not os.path.exists(component_requirements):
    git.Git().clone('https://github.com/stackforge/%s.git' % component)
    component_requirements = os.path.join(__location,
                                          '%s/%s'
                                          % (component,
                                             requirements_file_name))

if not os.path.exists(global_requirements):
    git.Git().clone('https://github.com/openstack/requirements.git')
    global_requirements = os.path.join(__location,
                                       'requirements/global-requirements.txt')

with open(component_requirements, 'r') as comp_reqs, open(
        global_requirements, 'r') as glob_reqs:

    errors = 0
    reqs_list = [x for x in glob_reqs]

    for line in comp_reqs:

        if line[0] == '#':
            continue

        if line not in reqs_list:
            errors += 1
            print line

        if errors > errors_limit:
            raise Exception('Too many mismatches')

print ('Count of mismatches = %s' % str(errors))
