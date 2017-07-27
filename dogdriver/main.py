import argparse
import socket
from dogdriver.client import run_test


def main():
    parser = argparse.ArgumentParser(description='Dogdriver.')
    parser.add_argument('-s', '--source', default=socket.gethostname(),
                        type=str, help="Name of the source")
    parser.add_argument('-p', '--project', default='kintowe', type=str,
                        help="Name of the project")
    parser.add_argument('-t', '--test', default='dogdriver', type=str,
                        help="Name of the test in the Service Book")
    parser.add_argument('-m', '--molotov-test', default='dogdriver', type=str,
                        help="Name of the test in the Molotov config")
    parser.add_argument('-d', '--deployment', default='stage', type=str,
                        help="Name of the deployment")

    args = parser.parse_args()
    print(run_test(args))
