import argparse
import sys
from main import run


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-D', '--db', default='sqlite:///twitter.db',
                        help='DB connection string ex: sqlite:///test.db')
    parser.add_argument('-N', '--name', default='tweet',
                        help='Name of sqlite table or mongo collection')
    parser.add_argument('-T', '--topics', nargs='+', required=True,
                        help='List of topics to follow')
    parser.add_argument('--verbose', dest='verbose', action='store_true')
    
    return parser.parse_args(args)


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    run(**vars(args))