import time
from dogdriver.server import MetricsBuilder
from dogdriver.client import run_test


def main():
    start, end = run_test()
    # lets wait 6 minutes
    print('zZZzZzz')
    time.sleep(60*6)
    filename = MetricsBuilder().create(start, end)
    print('%s created.' % filename)


if __name__ == '__main__':
    main()
