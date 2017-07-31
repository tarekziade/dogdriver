import argparse
from dogdriver.client import run_test


def main():
    parser = argparse.ArgumentParser(description='Dogdriver.')
    parser.add_argument('-a', '--auto', default=None, type=str,
                        help="Uses the server project list and runs all tests")
    parser.add_argument('-s', '--source', default=None,
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
