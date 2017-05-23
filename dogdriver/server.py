from uuid import uuid4
from bottle import route, run, template, post, request
import os
import json
import time
from dogdriver.util import MetricsBuilder


@route('/')
def index():
    return '<b>Hello</b>!'


@post('/test')
def post_test():
    ok = MetricsBuilder().async_create(**request.json)
    return {'result': ok}


def main():
    # XXX run a queue that will process the metrics
    run(host='localhost', port=8080)
