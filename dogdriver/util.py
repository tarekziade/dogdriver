import time
import json
import os
from datadog import initialize, api
from uuid import uuid4


HERE = os.path.dirname(__file__)
_INIT = False

def init_api():
    global _INIT
    if _INIT:
        return
    APP_KEY = os.environ['DOG_APP_KEY']
    API_KEY = os.environ['DOG_API_KEY']
    initialize(app_key=APP_KEY, api_key=API_KEY)
    _INIT = True


init_api()

_LATENCY = 'avg:aws.elb.latency{app:kintowe,env:stage}'
_REQ = 'sum:aws.elb.request_count{app:kintowe,env:stage}.as_count()'
_CPU = """\
max:system.cpu.user{app:kintowe,env:stage,type:web} by {host} +
max:system.cpu.system{app:kintowe,env:stage,type:web} by {host} +
max:system.cpu.stolen{app:kintowe,env:stage,type:web} by {host}"""


class MetricsBuilder(object):
    def __init__(self, root=HERE):
        self.root = root

    def async_create(self, **data):
        data['now'] = int(time.time())
        project = data['project']
        filename = 'job-%s.json' % (str(uuid4()))
        filename = os.path.join(self.root, filename)
        with open(filename, 'w') as f:
            f.write(json.dumps(data))
        return filename

    def create(self, **data):
        start = data['start']
        end = data['end']
        project = data['project']
        results = {}
        cpu = api.Metric.query(start=start, end=end, query=_CPU)
        max_cpu = max([val for _, val in cpu['series'][0]['pointlist']])
        results['CPU'] = max_cpu
        rps = api.Metric.query(start=start, end=end, query=_REQ)
        max_rps = max([val for _, val in rps['series'][0]['pointlist']])
        results['RPS'] = max_rps
        latency = api.Metric.query(start=start, end=end, query=_LATENCY)
        results['ART'] = max([(val*1000) for _, val in latency['series'][0]['pointlist']])
        results['version'] = data['version']
        filename = '%s-%s.json' % (project, str(start))
        filename = os.path.join(self.root, filename)
        with open(filename, 'w') as f:
            f.write(json.dumps(results))
        return filename
