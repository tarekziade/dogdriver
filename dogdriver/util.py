import json
import os
from datadog import initialize, api

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

_200 = 'aws.elb.httpcode_backend_2xx{app:kintowe,env:stage}'
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
        results['CPU'] = api.Metric.query(start=start, end=end, query=_CPU)
        results['RPS'] = api.Metric.query(start=start, end=end, query=_REQ)
        results['200'] = api.Metric.query(start=start, end=end, query=_200)
        filename = '%s-%s.json' % (project, str(start))
        filename = os.path.join(self.root, filename)
        with open(filename, 'w') as f:
            f.write(json.dumps(results))
        return filename
