import os
from datadog import initialize, api
from dogdriver.db import upload_json


_INIT = False


def init_api():
    global _INIT
    if _INIT:
        return
    if 'DOG_APP_KEY' in os.environ:
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


def _max(metric, transform=lambda x: x, index=0):
    if index >= len(metric['series']):
        return 0
    values = metric['series'][index]
    return max([transform(val) for _, val in
               values['pointlist']])


def create_metrics(**data):
    start = data['start']
    end = data['end']
    project = data['project']
    results = {}
    cpu = api.Metric.query(start=start, end=end, query=_CPU)
    results['CPU'] = _max(cpu)
    rps = api.Metric.query(start=start, end=end, query=_REQ)
    results['RPS'] = _max(rps)
    latency = api.Metric.query(start=start, end=end, query=_LATENCY)
    results['ART'] = _max(latency, lambda x: x * 1000)
    results['version'] = data['version']
    filename = '%s-%s.json' % (project, str(start))
    upload_json(results, filename)
    return 's3://dogdriver/' + filename
