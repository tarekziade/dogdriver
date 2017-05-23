import os
import json
import time
from dogdriver.util import MetricsBuilder


_1_MIN = 60
_6_MIN = 60 * 6
HERE = os.path.dirname(__file__)


class Worker(object):
    def __init__(self, root=HERE, sleep=_1_MIN, delay=_6_MIN):
        self.root = root
        self.builder = MetricsBuilder(root)
        self.sleep = sleep
        self.delay = delay

    def run(self):
        while True:
            print('Scanning %s' % self.root)
            for filename in os.listdir(self.root):
                if not filename.startswith('job-'):
                    continue
                self._process_file(filename)
            print('ZzzzZ')
            time.sleep(self.sleep)

    def _process_file(self, filename):
        print('Working on %s' % filename)
        fullpath = os.path.join(self.root, filename)
        with open(fullpath) as f:
            data = json.loads(f.read())

        age = time.time() - data['now']
        if age < self.delay:
            print('Too fresh')
            return
        print('Grabing metrics')
        produced = self.builder.create(**data)
        print('Metrics produced at %s' % produced)
        os.remove(fullpath)

def main():
    worker = Worker()
    worker.run()


if __name__ == '__main__':
    main()
