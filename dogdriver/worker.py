import os
import json
import time

from dogdriver.util import create_metrics
from dogdriver.db import get_list, download_json, delete_json


_1_MIN = 60
_6_MIN = 60 * 6


class Worker(object):
    def __init__(self, sleep=_1_MIN, delay=_6_MIN):
        self.sleep = sleep
        self.delay = delay

    def run(self):
        while True:
            print('Scanning the S3 bucket')
            for filename in get_list('job-'):
                self._process_file(filename)
            print('ZzzzZ')
            time.sleep(self.sleep)

    def _process_file(self, filename):
        print('Working on %s' % filename)
        data = download_json(filename)
        age = time.time() - data.get('now', time.time() - self.delay - 1)
        if age < self.delay:
            print('Too fresh - %d' % age)
            return
        print('Grabing metrics')
        produced = create_metrics(**data)
        print('Metrics produced at %s' % produced)
        delete_json(filename)


def main():
    worker = Worker()
    worker.run()


if __name__ == '__main__':
    main()
