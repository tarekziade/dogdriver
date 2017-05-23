import sys
import os
from datadog import initialize
from molotov.slave import main as moloslave


HERE = os.path.dirname(__file__)
APP_KEY = os.environ['DOG_APP_KEY']
API_KEY = os.environ['DOG_API_KEY']

initialize(app_key=APP_KEY, api_key=API_KEY)

# Use Datadog REST API client
from datadog import api

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


def run_test(name="My Test"):
    # the test
    start_event = _start(name)
    try:
        # run the molotov test against the stack
        args = ['moloslave', 'https://github.com/tarekziade/kinto-loadtests',
                'dogdriver']

        old = list(sys.argv)
        sys.argv = args
        try:
            moloslave()
        except SystemExit:
            pass
        finally:
            sys.argv = old
    finally:
        stop_event = _stop(name)

    start = start_event['event']['date_happened']
    end = stop_event['event']['date_happened']
    return start, end
