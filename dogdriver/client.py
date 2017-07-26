import time
import sys
from uuid import uuid4

import requests
from molotov.slave import main as moloslave

from dogdriver.util import api
from dogdriver.db import upload_json


def _start(project):
    text = "Dogdriver starts against %s" % project
    tags = []
    tags.append('step:start')
    tags.append('project:%s' % project)
    return api.Event.create(title="Dogdriver", text=text, tags=tags)


def _stop(project):
    text = "Dogdriver ended against %s" % project
    tags = []
    tags.append('step:stop')
    tags.append('project:%s' % project)
    return api.Event.create(title='Dogdriver', text=text, tags=tags)


def get_test_info(project, deployment):
    book = 'http://servicebook.dev.mozaws.net/api/project'
    projects = requests.get(book).json()['data']
    test_url = deployment_url = None

    for item in projects:
        if item['name'] == project:
            for test in item['tests']:
                if test['name'] == 'dogdriver':
                    test_url = test['url']
            if test_url is None:
                break

            for depl in item['deployments']:
                if depl['name'] == deployment:
                    deployment_url = depl['endpoint']
                    break

    if test_url is None:
        raise KeyError("No datadog test for %r" % project)
    if deployment_url is None:
        raise KeyError("No %r deployment for %r" % (deployment, project))

    return test_url, deployment_url


def run_test(args):
    project = args.project
    source = args.source
    deployment = args.deployment

    # grab the test url
    test_url, deployment_url = get_test_info(project, deployment)

    # grab deployed project version
    version_url = deployment_url.rstrip('/') + '/__version__'
    info = requests.get(version_url)
    version = info.json()["version"]
    print('Running %r on %r' % (test_url, deployment))
    start_event = _start(project)
    try:
        # run the molotov test
        args = ['moloslave', test_url, 'dogdriver']
        old = list(sys.argv)
        sys.argv = args
        try:
            moloslave()
        except SystemExit:
            pass
        finally:
            sys.argv = old
    finally:
        stop_event = _stop(project)

    data = {}
    data['start'] = start_event['event']['date_happened']
    data['end'] = stop_event['event']['date_happened']
    data['project'] = project
    data['version'] = version
    data['now'] = time.time()
    data['source'] = source

    # send the data in the S3 bucket
    job_name = 'job-%s.json' % str(uuid4())
    upload_json(data, job_name)
