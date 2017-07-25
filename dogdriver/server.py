import os
from bottle import route, run, get, request
import bottle
from bottle import mako_view as view

from dogdriver.db import get_list, download_json
from dogdriver.util import trend


def get_sources(project):
    sources = []
    for filename in get_list(project + '-'):
        data = download_json(filename)
        source = data.get('source')
        if source and source not in sources:
            sources.append(source)
    return sources



PROJECTS = [{'name': 'kintowe', 'sources': get_sources('kintowe')},
            {'name': 'absearch', 'sources': get_sources('absearch')},
            {'name': 'sync', 'sources': get_sources('sync')}]

HERE = os.path.dirname(__file__)
bottle.TEMPLATE_PATH.append(os.path.join(HERE, 'templates'))


@route('/')
@route('/dogdriver')
@view('index')
def index():
    source = request.query.get('source', 'tarek')
    return {'source': source, 'project': 'kintowe', 'projects': PROJECTS}


@route('/<project>')
@route('/dogdriver/<project>')
@view('project')
def project_index(project):
    source = request.query.get('source', 'tarek')
    return {'source': source, 'project': project, 'projects': PROJECTS}



@get('/trend/<project>')
@get('/dogdriver/trend/<project>')
def get_trend(project):
    # trend is only on RPS for now
    metric = 'RPS'
    previous = None
    bysource = request.query.get('source')
    values = []

    for filename in get_list(project + '-'):
        data = download_json(filename)
        if bysource is not None and data.get('source') != bysource:
            continue
        metric = metric.upper()   # XXX
        value = data.get(metric, 0)
        values.append(value)

    _trend = trend(values)
    up = 'trendGood'
    down = 'trendBad'

    if _trend == 1:
        _trend = '<span class="%s">⇧</span>' % up
    elif _trend == 0:
        _trend = '<span class="trendEq">≈</span>'
    else:
        _trend = '<span class="%s">⬇</span>' % down

    return {'trend': _trend}


@get('/runs/<project>/<metric>')
@get('/dogdriver/runs/<project>/<metric>')
def get_runs(project, metric):
    chart = []
    previous = None
    bysource = request.query.get('source')
    values = []

    for filename in get_list(project + '-'):
        data = download_json(filename)
        if bysource is not None and data.get('source') != bysource:
            continue

        stamp = filename.split('-')[1].split('.')[0]
        metric = metric.upper()   # XXX
        value = data.get(metric, 0)
        run = {'value': value, 'label': stamp}
        version = data.get('version', '')
        if version == previous:
            run['release'] = ''
        else:
            run['release'] = previous = version
        values.append(value)
        chart.append(run)

    _trend = trend(values)

    if metric in ('CPU', 'ART'):
        up = 'trendBad'
        down = 'trendGood'
    else:
        up = 'trendGood'
        down = 'trendBad'

    if _trend == 1:
        _trend = '<span class="%s">⇧</span>' % up
    elif _trend == 0:
        _trend = '<span class="trendEq">≈</span>'
    else:
        _trend = '<span class="%s">⬇</span>' % down

    return {'data': chart, 'trend': _trend}


application = bottle.default_app()


def main():
    # XXX run a queue that will process the metrics
    run(host='localhost', port=8080)
