import sys
import os
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


# XXX add argparse and use ServiceBook
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
