""" imports """
from url_monkey import UrlMonkey
from argparse import ArgumentParser


def main():
    """ just a wrapper function """

    PARSER = ArgumentParser()
    PARSER.add_argument(
        '-v',
        '--verbose',
        action="store_true",
        help='Enter this argument to enable verbosity')
    PARSER.add_argument(
        'url',
        help='Enter a valid url to start the infinite search for all branches '
        'and trees surrounding it (as example: https://www.python.org/)')

    ARGS = PARSER.parse_args()
    DONKEY_KONG = UrlMonkey()
    DONKEY_KONG.search(ARGS.verbose, ARGS.url)


if __name__ == '__main__':
    main()