import time
import sys
from uuid import uuid4

import requests
from molotov.slave import main as moloslave

from dogdriver.util import api
from dogdriver.db import upload_json


def _start(project):
    text = "Dogdriver starts against %s" % project
    tags = []
    tags.append('step:start')
    tags.append('project:%s' % project)
    return api.Event.create(title="Dogdriver", text=text, tags=tags)


def _stop(project):
    text = "Dogdriver ended against %s" % project
    tags = []
    tags.append('step:stop')
    tags.append('project:%s' % project)
    return api.Event.create(title='Dogdriver', text=text, tags=tags)


def get_test_url(project_name):
    book = 'http://servicebook.dev.mozaws.net/api/project'
    projects = requests.get(book).json()['data']
    for project in projects:
        if project['name'] == project_name:
            for test in project['tests']:
                if test['name'] == 'dogdriver':
                    return test['url']
    raise KeyError(project_name)


def run_test(args):
    project = args.project
    source = args.source

    # grab the test url
    test_url = get_test_url(project)

    # grab deployed project version
    # XXX should be in servicbook
    info = requests.get('https://webextensions-settings.stage.mozaws.net/v1/')
    version = info.json()["project_version"]

    print('Running %s' % test_url)
    start_event = _start(project)
    try:
        # run the molotov test
        args = ['moloslave', test_url, 'dogdriver']
        old = list(sys.argv)
        sys.argv = args
        try:
            moloslave()
        except SystemExit:
            pass
        finally:
            sys.argv = old
    finally:
        stop_event = _stop(project)

    data = {}
    data['start'] = start_event['event']['date_happened']
    data['end'] = stop_event['event']['date_happened']
    data['project'] = project
    data['version'] = version
    data['now'] = time.time()
    data['source'] = source

    # send the data in the S3 bucket
    job_name = 'job-%s.json' % str(uuid4())
    upload_json(data, job_name)
