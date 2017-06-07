import argparse
import socket
from dogdriver.client import run_test


def main():
    parser = argparse.ArgumentParser(description='Dogdriver.')
    parser.add_argument('-s', '--source', default=socket.gethostname(),
                        type=str, help="Name of the source")
    parser.add_argument('-p', '--project', default='kintowe', type=str,
                        help="Name of the project")


    args = parser.parse_args()
    print(run_test(args))
