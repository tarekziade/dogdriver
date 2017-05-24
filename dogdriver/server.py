from uuid import uuid4
from bottle import route, run, post, request, get
import bottle
from bottle import mako_view as view

import os
import json
import time
from dogdriver.util import MetricsBuilder

HERE = os.path.dirname(__file__)
bottle.TEMPLATE_PATH.append(os.path.join(HERE, 'templates'))


@route('/')
@view('index')
def index():
    return {}


@get('/runs/<project>/<metric>')
def get_runs(project, metric):
    return {'data': [
        {'label': '1.0', 'value': 2},
        {'label': '1.1', 'value': 3},
        {'label': '1.2', 'value': 6},
        {'label': '1.3', 'value': 5},
    ]}


@post('/test')
def post_test():
    ok = MetricsBuilder().async_create(**request.json)
    return {'result': ok}


def main():
    # XXX run a queue that will process the metrics
    run(host='localhost', port=8080)
