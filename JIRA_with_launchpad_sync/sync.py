# Copyright (c) 2013 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import sys
import httplib2
import os
import ConfigParser
from dateutil import parser
from jira.client import JIRA
from launchpadlib.launchpad import Launchpad
from launchpadlib.launchpad import uris


httplib2.debuglevel = 0

lp_cache_dir = os.path.expanduser(
    os.environ.get('LAUNCHPAD_CACHE_DIR', '~/.launchpadlib/cache'))
lp_creds_filename = os.path.expanduser(
    os.environ.get('LAUNCHPAD_CREDS_FILENAME', '~/.launchpadlib/creds'))


def update_status_of_jira_issue(jira, issue, new_status):
    new_status_id = None
    for status in jira.transitions(issue):
        if get_str(status['name']) == new_status:
            new_status_id = status['id']

    if not new_status_id:
        raise RuntimeError('No jira_status_id exists for status {0}'.format(
            new_status))

    jira.transition_issue(issue, new_status_id,
                          comment="Automatically updated by script.")


def get_str(parameter):
    if not parameter:
        parameter = ''
    return str(parameter.encode('ascii', 'ignore'))


def get_date(parameter):
    date = parser.parse(parameter)
    return date


def get_status(parameter):
    parameter = get_str(parameter)
    if parameter in ['In Testing', 'To Test']:
        return {'jira': parameter, 'launchpad': 'Fix Committed', 'code': 0}
    elif parameter == 'Fix Committed':
        return {'jira': 'To Test', 'launchpad': 'Fix Committed', 'code': 0}
    elif parameter == 'Resolved':
        return {'jira': 'Resolved', 'launchpad': 'Fix Released', 'code': 3}
    elif parameter == 'Fix Released':
        return {'jira': 'Closed', 'launchpad': 'Fix Released', 'code': 3}
    elif parameter in ['Reopened', 'To Do']:
        return {'jira': parameter, 'launchpad': 'New', 'code': 1}
    elif parameter == 'Rejected':
        return {'jira': parameter, 'launchpad': 'Invalid', 'code': 2}
    elif parameter == 'Closed':
        return {'jira': parameter, 'launchpad': 'Fix Released', 'code': 3}
    elif parameter in ['New', 'Incomplete', 'Opinion', 'Confirmed', 'Triaged']:
        return {'jira': 'ToDo', 'launchpad': parameter, 'code': 1}
    elif parameter in ['Invalid', "Won't Fix"]:
        return {'jira': 'Rejected', 'launchpad': parameter, 'code': 2}
    else:
        return {'jira': parameter, 'launchpad': parameter, 'code': 4}


def get_priority(parameter):
    parameter = get_str(parameter)
    if parameter in ['Blocker', 'Critical']:
        return {'jira': parameter, 'launchpad': 'Critical', 'code': 0}
    elif parameter in ['High', 'Medium']:
        return {'jira': 'Major', 'launchpad': parameter, 'code': 1}
    elif parameter == 'Major':
        return {'jira': 'Major', 'launchpad': 'Medium', 'code': 1}
    elif parameter in ['Nice to have', 'Some day']:
        return {'jira': parameter, 'launchpad': 'Low', 'code': 2}
    elif 'Low' in parameter:
        return {'jira': 'Nice to have', 'launchpad': 'Low', 'code': 2}
    else:
        return {'jira': parameter, 'launchpad': parameter, 'code': 3}


def get_jira_bugs(url, user, password, project,
                  issues_count=1000000,
                  issues_fields='key,summary,description,issuetype,priority,'
                                'status,updated,comment,fixVersions',
                  search_string_template='project={0} and issuetype=Bug'):

    jira = JIRA(basic_auth=(user, password), options={'server': url})

    search_string = search_string_template.format(project)
    issues = jira.search_issues(search_string, fields=issues_fields,
                                maxResults=issues_count)
    bugs = []

    for issue in issues:
        bug = {'key': get_str(issue.key),
               'title': get_str(issue.fields.summary),
               'description': get_str(issue.fields.description),
               'priority': get_priority(issue.fields.priority.name),
               'status': get_status(issue.fields.status.name),
               'updated': get_date(issue.fields.updated),
               'comments': issue.fields.comment.comments,
               'fix_version': ''}

        if issue.fields.fixVersions:
            version = get_str(issue.fields.fixVersions[0].name)
            bug.update({'fix_version': version})

        summary = bug['title']
        if 'Launchpad Bug' in summary:
            summary = summary[24:]

        bug.update({'priority_code': bug['priority']['code'],
                    'status_code': bug['status']['code'],
                    'summary': summary})

        bugs.append(bug)

    print 'Found {0} bugs in JIRA'.format(len(bugs))

    return bugs


def get_launchpad_bugs(project):
    project = project.lower()
    launchpad = Launchpad.login_with(project.lower(),
                                     uris.LPNET_SERVICE_ROOT,
                                     lp_cache_dir,
                                     credentials_file=lp_creds_filename)
    project = launchpad.projects[project]
    launchpad_bugs = project.searchTasks(status=["New", "Fix Committed",
                                                 "Invalid", "Won't Fix",
                                                 "Confirmed", "Triaged",
                                                 "In Progress", "Incomplete",
                                                 "Fix Released"])

    bugs = []
    for launchpad_bug in launchpad_bugs:
        bug_link = get_str(launchpad_bug.self_link)
        key = re.search(r"[0-9]+$", bug_link).group()
        parameters = launchpad_bug.bug

        bug = {'key': get_str(key),
               'title': get_str(parameters.title),
               'summary': get_str(parameters.title),
               'description': get_str(parameters.description),
               'priority': get_priority(launchpad_bug.importance),
               'status': get_status(launchpad_bug.status),
               'updated': parameters.date_last_updated,
               #'comments': parameters.messages.entries[1:],
               #'attachments': parameters.attachments.entries,
               'fix_version': ''}

        #if parameters.linked_branches.entries:
        #    version = get_str(parameters.linked_branches.entries[0])
        #    bug.update({'fix_version': version})

        bug.update({'priority_code': bug['priority']['code'],
                    'status_code': bug['status']['code']})

        bugs.append(bug)

        # It works very slow, print the dot per bug, for fun
        print ".",
        sys.stdout.flush()

    print '\nFound {0} bugs on launchpad'.format(len(bugs))

    return bugs


def update_jira_bug(jira, issue, title, description, priority, status):
    print "Updating JIRA bug ", title
    print "Description & Title & Priority updating..."
    try:
        issue.update(summary=title, description=description,
                     priority={'name': priority})
        print "... updated: OK"
    except Exception as ex:
        print "... updated: FAIL (not possible)"
        print type(ex), ex

    print "Status updating..."
    try:
        update_status_of_jira_issue(jira, get_str(issue.key), status)
        print "... updated: OK"
    except Exception as ex:
        print "... updated: FAIL (not possible)"
        print type(ex), ex


def update_lp_bug(bug, title, description, priority, status):
    print "Updating launchpad bug ", title
    # attachments
    #print launchpad.bugs[Lbug['key']].lp_operations

    print "Description & Title updating..."
    try:
        bug.title = title
        bug.description = description
        bug.lp_save()
        print "... updated: OK"
    except Exception as ex:
        print "... updated: FAIL (not possible)"
        print type(ex), ex

    print "Status & Priority updating..."
    try:
        bug_task = bug.bug_tasks[0]
        bug_task.status = status
        bug_task.importance = priority
        bug_task.lp_save()
        print "... updated: OK"
    except Exception as ex:
        print "... updated: FAIL (not possible)"
        print type(ex), ex


def create_jira_bug(jira, project_key, title, description):
    new_issue = None
    fields = {'project': {'key': project_key}, 'summary': title,
              'description': description, 'issuetype': {'name': 'Bug'}}

    print "Creating the new bug desciption in JIRA... ", title
    try:
        new_issue = jira.create_issue(fields=fields)
        print "The new bug description was successfully created in JIRA"
    except Exception as ex:
        print "Can not create new bug in JIRA"
        print type(ex), ex

    return new_issue


def create_lp_bug(launchpad, project, title, description):
    new_bug = None
    print "Creating the bug desciption on launchpad... ", title
    try:
        new_bug = launchpad.bugs.createBug(target=project.self_link,
                                           title=title,
                                           description=description)
        print "The bug description was successfully created on launchpad"
    except Exception as ex:
        print "Can not create new bug on launchpad"
        print type(ex), ex

    return new_bug


def sync_jira_with_launchpad(url, user, password, project, project_key):
    template = 'Launchpad Bug #{0}: '

    jira_bugs = get_jira_bugs(url, user, password, project_key)
    launchpad_bugs = get_launchpad_bugs(project)

    jira = JIRA(basic_auth=(user, password), options={'server': url})
    launchpad = Launchpad.login_with(project.lower(),
                                     uris.LPNET_SERVICE_ROOT,
                                     lp_cache_dir,
                                     credentials_file=lp_creds_filename)

    # Sync already created tasks
    for Jbug in jira_bugs:
        for Lbug in launchpad_bugs:
            if (Lbug['title'] in Jbug['title'] or
                    Lbug['key'] in Jbug['title']):
                for parameter in ['description', 'summary', 'status_code',
                                  'priority_code']:
                    if Jbug[parameter] != Lbug[parameter]:
                        if Jbug['updated'] < Lbug['updated']:

                            new_title = ''
                            if not Lbug['key'] in Jbug['title']:
                                new_title = template.format(Lbug['key'])
                            new_title += Lbug['title']

                            update_jira_bug(jira, jira.issue(Jbug['key']),
                                            new_title, Lbug['description'],
                                            Lbug['priority']['jira'],
                                            Lbug['status']['jira'])
                        else:
                            new_title = Jbug['title']
                            if 'Launchpad Bug' in new_title:
                                new_title = str(new_title[24:])

                            update_lp_bug(launchpad.bugs[Lbug['key']],
                                          new_title, Jbug['description'],
                                          Jbug['priority']['launchpad'],
                                          Jbug['status']['launchpad'])
                        break
                break

    # Move new bugs from launchpad to JIRA
    for Lbug in launchpad_bugs:
        if Lbug['status_code'] == 3:
            continue

        sync = False
        duplicated = False

        for Lbug2 in launchpad_bugs:
            if Lbug2['title'] == Lbug['title'] and Lbug2['key'] != Lbug['key']:
                duplicated = True

        for Jbug in jira_bugs:
            if (Lbug['title'] in Jbug['title'] or
                    Lbug['key'] in Jbug['title'] or
                    'Launchpad Bug' in Jbug['title']):
                sync = True

            if not sync and not duplicated:
                new_title = ''
                if not Lbug['key'] in Jbug['title']:
                    new_title = template.format(Lbug['key'])
                new_title += Lbug['title']

                new_issue = create_jira_bug(jira, project_key, new_title,
                                            Lbug['description'])
                if new_issue:
                    update_jira_bug(jira, jira.issue(new_issue.key),
                                    new_title, Lbug['description'],
                                    Lbug['priority']['jira'],
                                    Lbug['status']['jira'])

    # Move new bugs from JIRA to launchpad
    for Jbug in jira_bugs:
        if Jbug['status_code'] == 3:
            continue

        sync = False
        duplicated = False

        for Jbug2 in jira_bugs:
            if Jbug2['title'] == Jbug['title'] and Jbug2['key'] != Jbug['key']:
                duplicated = True

        for Lbug in launchpad_bugs:
            if (Lbug['title'] in Jbug['title'] or
                    Lbug['key'] in Jbug['title'] or
                    'Launchpad Bug' in Jbug['title']):
                sync = True

            if not sync and not duplicated:
                lp_project = launchpad.projects[project]
                new_bug = create_lp_bug(launchpad, lp_project, Jbug['title'],
                                        Jbug['description'])

                if new_bug:
                    update_lp_bug(new_bug,
                                  Jbug['title'], Jbug['description'],
                                  Jbug['priority']['launchpad'],
                                  Jbug['status']['launchpad'])

    for Jbug in jira_bugs:
        if Jbug['status_code'] == 3:
            continue

        for Lbug in launchpad_bugs:
            if Lbug['title'] in Jbug['title']:
                if Lbug['key'] in Jbug['title'] and \
                        'Launchpad Bug' in Jbug['title']:
                    continue

                new_title = template.format(Lbug['key']) + Lbug['title']
                update_jira_bug(jira, jira.issue(Jbug['key']),
                                new_title, Jbug['description'],
                                Jbug['priority']['jira'],
                                Jbug['status']['jira'])


config = ConfigParser.RawConfigParser()
config.read('sync.cfg')

sync_jira_with_launchpad(url=config.get('JIRA', 'URL'),
                         user=config.get('JIRA', 'user'),
                         password=config.get('JIRA', 'password'),
                         project=config.get('project', 'name'),
                         project_key=config.get('JIRA', 'project_key'))
