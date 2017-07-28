from functools import wraps
import os
import time
from contextlib import contextmanager
from io import BytesIO
import json
import hashlib

import boto3

_C = {}
JOB_PREFIX = 'job-'


def cached(name, max_age=60):
    def _cached(func):
        @wraps(func)
        def __cached(*args, **kw):
            hash = hashlib.md5(name.encode('utf8'))
            for arg in args:
                hash.update(str(arg).encode('utf8'))
            keywords = list(kw.items())
            keywords.sort()
            for k, v in keywords:
                hash.update(str(v).encode('utf8'))
            key = hash.hexdigest()

            if key in _C:
                when, val = _C[key]
                if time.time() - when < max_age:
                    return val
            val = func(*args, **kw)
            _C[key] = time.time(), val
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


def delete_json(key, name='dogdriver'):
    with s3bucket(name) as bucket:
        bucket.Object(key).delete()


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
