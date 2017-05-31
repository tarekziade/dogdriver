import os
import time
from contextlib import contextmanager
from io import BytesIO
import json

import boto3

_C = {}


def cached(name, max_age=60):
    def _cached(func):
        def __cached(*args, **kw):
            if name in _C:
                when, val = _C[name]
                if time.time() - when < max_age:
                    return val
            val = func(*args, **kw)
            _C[name] = time.time(), val
            return val
        return __cached
    return _cached


@contextmanager
def s3bucket(name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(name)
    yield bucket


# XXX cache -- need a "has bucket changed?"
@cached('list')
def get_list(filter='', name='dogdriver'):
    keys = []
    with s3bucket(name) as bucket:
        for ob in bucket.objects.filter(Prefix=filter):
            keys.append(ob.key)
    return keys


def upload_json(data, key, name='dogdriver'):
    with s3bucket(name) as bucket:
        data = json.dumps(data).encode('utf8')
        fileobj = BytesIO(data)
        fileobj.seek(0)
        return bucket.upload_fileobj(fileobj, key)


def download_json(key, name='dogdriver'):
    # XXX cheap cache -- need real stuff with LastModified check
    if os.path.exists(key):
        with open(key) as f:
            return json.loads(f.read())

    with s3bucket(name) as bucket:
        fileobj = BytesIO()
        obj = bucket.Object(key)
        obj.download_fileobj(fileobj)
        fileobj.seek(0)
        data = fileobj.read()
        data = data.decode('utf8')
        with open(key, 'w') as f:
            f.write(data)
        return json.loads(data)
