import sys
import os

import requests
from molotov.slave import main as moloslave
from dogdriver.util import api


HERE = os.path.dirname(__file__)
title = "Molotov"
text = "We're doing a Molotov test on kintowe"
_tags = ['version:1', 'app:kintowe']


def _start(test_name):
    tags = list(_tags)
    tags.append('step:start')
    tags.append('test:%s' % test_name)
    return api.Event.create(title=title, text=text, tags=tags)


def _stop(test_name):
    tags = list(_tags)
    tags.append('step:stop')
    tags.append('test:%s' % test_name)
    return api.Event.create(title='Molotov-Stop', text=text, tags=tags)


def get_test_url(project_name):
    book = 'http://servicebook.dev.mozaws.net/api/project'
    projects = requests.get(book).json()['data']
    for project in projects:
        if project['name'] == project_name:
            for test in project['tests']:
                if test['name'] == 'dogdriver':
                    return test['url']
    raise KeyError(project_name)


# XXX add argparse and use ServiceBook
def run_test(project="kintowe", metadata={'tag': '1.0'}):
    test_url = get_test_url(project)
    print('Running %s' % test_url)
    # the test
    start_event = _start(project)
    try:
        # run the molotov test against the stack
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

    start = start_event['event']['date_happened']
    end = stop_event['event']['date_happened']
    return start, end



