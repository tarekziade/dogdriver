import json
import sys
import os
import time
from datadog import initialize
from molotov.slave import main as moloslave


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


_200 = 'aws.elb.httpcode_backend_2xx{app:kintowe,env:stage}'
_REQ = 'sum:aws.elb.request_count{app:kintowe,env:stage}.as_count()'
_CPU = """\
max:system.cpu.user{app:kintowe,env:stage,type:web} by {host} +
max:system.cpu.system{app:kintowe,env:stage,type:web} by {host} +
max:system.cpu.stolen{app:kintowe,env:stage,type:web} by {host}"""


def create_metrics(start, end):
    # now we want to grab metrics on that time window
    results = {}
    results['CPU'] = api.Metric.query(start=start, end=end, query=_CPU)
    results['RPS'] = api.Metric.query(start=start, end=end, query=_REQ)
    results['200'] = api.Metric.query(start=start, end=end, query=_200)
    here = os.path.dirname(__file__)
    filename = 'dogdrive-%s.json' % str(start)
    filename = os.path.join(here, filename)

    with open(filename, 'w') as f:
        f.write(json.dumps(results))

    return filename


def main():
    start, end = run_test()
    # lets wait 6 minutes
    print('zZZzZzz')
    time.sleep(60*6)
    import pdb; pdb.set_trace()
    filename = create_metrics(start, end)
    print('%s created.' % filename)


if __name__ == '__main__':
    main()
