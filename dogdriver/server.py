import os
from bottle import route, run, get, request
import bottle
from bottle import mako_view as view

from dogdriver.db import get_list, download_json

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
    bysource = request.query.get('source')

    for filename in get_list(project + '-'):
        data = download_json(filename)
        if bysource is not None and data.get('source') != bysource:
            continue

        stamp = filename.split('-')[1].split('.')[0]
        metric = metric.upper()   # XXX

        run = {'value': data.get(metric, 0), 'label': stamp}
        version = data.get('version', '')
        if version == previous:
            run['release'] = ''
        else:
            run['release'] = previous = version
        chart.append(run)

    return {'data': chart}


application = bottle.default_app()


def main():
    # XXX run a queue that will process the metrics
    run(host='localhost', port=8080)
