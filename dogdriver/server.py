from bottle import route, run, template, post
import os
import json
from dogdriver.util import api


HERE = os.path.dirname(__file__)
APP_KEY = os.environ['DOG_APP_KEY']
API_KEY = os.environ['DOG_API_KEY']
_200 = 'aws.elb.httpcode_backend_2xx{app:kintowe,env:stage}'
_REQ = 'sum:aws.elb.request_count{app:kintowe,env:stage}.as_count()'
_CPU = """\
max:system.cpu.user{app:kintowe,env:stage,type:web} by {host} +
max:system.cpu.system{app:kintowe,env:stage,type:web} by {host} +
max:system.cpu.stolen{app:kintowe,env:stage,type:web} by {host}"""


class MetricsBuilder(object):
    def __init__(self, root=HERE):
        self.root = root

    def create(self, start, end):
        # now we want to grab metrics on that time window
        results = {}
        results['CPU'] = api.Metric.query(start=start, end=end, query=_CPU)
        results['RPS'] = api.Metric.query(start=start, end=end, query=_REQ)
        results['200'] = api.Metric.query(start=start, end=end, query=_200)
        filename = 'dogdrive-%s.json' % str(start)
        filename = os.path.join(self.root, filename)
        with open(filename, 'w') as f:
            f.write(json.dumps(results))
        return filename


@route('/')
def index():
    return '<b>Hello</b>!'


@post('/test')
def post_test():
    import pdb; pdb.set_trace()
    # XXX store the test name, start end end dates.
    return {}



def main():
    # XXX run a queue that will process the metrics
    run(host='localhost', port=8080)
