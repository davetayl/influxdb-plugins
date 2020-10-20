import argparse

parser = argparse.ArgumentParser(description='Format: parsetest.py -t <host address>')
parser.add_argument('host', metavar='host',
                   help='The host address that will be tested')
parser.add_argument('--type', '-t',
                   help='The type of trace')
args = parser.parse_args()

print(vars(args)['host'])