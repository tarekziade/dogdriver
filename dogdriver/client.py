import time
import sys
from uuid import uuid4
import socket
import asyncio

import requests
from molotov.slave import main as moloslave

from dogdriver.util import api
from dogdriver.db import upload_json, JOB_PREFIX


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


def get_test_info(project, deployment, test_name):
    book = 'http://servicebook.dev.mozaws.net/api/project'
    projects = requests.get(book).json()['data']
    test_url = deployment_url = None
    project_found = False

    for item in projects:
        if item['name'] == project:
            project_found = True
            project_tests = item['tests']
            names = [test['name'] for test in project_tests]
            print("Tests: %s" % (', '.join(names)))
            for test in project_tests:
                if test['name'] == test_name:
                    test_url = test['url']
            if test_url is None:
                break

            for depl in item['deployments']:
                if depl['name'] == deployment:
                    deployment_url = depl['endpoint']
                    break

    if not project_found:
        raise KeyError("Could not find project %r" % project)
    if test_url is None:
        raise KeyError("No %r test for %r" % (test_name, project))
    if deployment_url is None:
        raise KeyError("No %r deployment for %r" % (deployment, project))

    return test_url, deployment_url


def run_test(args):
    auto = args.auto
    if auto is not None:
        projects = requests.get(auto).json()['projects']
        for project in projects:
            print("******* Running molotov on %r" % project['name'])
            # XXXX
            deployment = 'stage'
            test_name = molotov_test = 'dogdriver'
            if args.source is None:
                source = project['best_source']
            else:
                source = args.source

            try:
                run_single(project['name'], source,
                           deployment, test_name, molotov_test)
                print("******* SUCCESS!")
            except Exception as e:
                print(e)
                print("******* FAILED!")
    else:
        project = args.project
        source = args.source
        if source is None:
            source = socket.gethostname()
        deployment = args.deployment
        test_name = args.test
        molotov_test_name = args.molotov_test
        run_single(project, source, deployment, test_name, molotov_test_name)


def _init_molotov():
    from molotov.api import _SCENARIO, _FIXTURES
    _SCENARIO.clear()
    _FIXTURES.clear()
    asyncio.set_event_loop(asyncio.new_event_loop())


def run_single(project, source, deployment, test_name, molotov_test_name):
    _init_molotov()

    # grab the test url
    test_url, deployment_url = get_test_info(project, deployment, test_name)

    # grab deployed project version
    version_url = deployment_url.rstrip('/') + '/__version__'
    info = requests.get(version_url)
    version = info.json()["version"]
    print('Running %r on %r' % (test_url, deployment))
    start_event = _start(project)
    try:
        # run the molotov test
        args = ['moloslave', test_url, molotov_test_name]
        old = list(sys.argv)
        print("Running %r" % ' '.join(args))
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
    job_name = '%s-%s.json' % (JOB_PREFIX, str(uuid4()))
    upload_json(data, job_name)
