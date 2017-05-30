import os
import json

from bottle import route, run, post, request, get
import bottle
from bottle import mako_view as view
from dogdriver.util import MetricsBuilder

HERE = os.path.dirname(__file__)
bottle.TEMPLATE_PATH.append(os.path.join(HERE, 'templates'))


@route('/')
@view('index')
def index():
    return {}



@get('/runs/<project>/<metric>')
def get_runs(project, metric):
    chart = []

    previous = None

    for filename in os.listdir(HERE):
        if not filename.startswith(project + '-'):
            continue
        stamp = filename.split('-')[1].split('.')[0]
        fullpath = os.path.join(HERE, filename)
        with open(fullpath) as f:
            data = json.loads(f.read())

        metric = metric.upper()   # XXX

        run = {'value': data.get(metric, 0), 'label': stamp}
        version = data.get('version', '')
        if version == previous:
            run['release'] = ''
        else:
            run['release'] = previous = version
        chart.append(run)

    return {'data': chart}


@post('/test')
def post_test():
    ok = MetricsBuilder().async_create(**request.json)
    return {'result': ok}


def main():
    # XXX run a queue that will process the metrics
    run(host='localhost', port=8080)
