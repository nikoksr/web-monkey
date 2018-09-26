""" imports """
from url_monkey import UrlMonkey
from db_monkey import DatabaseMonkey
from argparse import ArgumentParser


def create_args():
    """ arparse wrapper to clean up main function """

    PARSER = ArgumentParser()
    PARSER.add_argument(
        '-v',
        '--verbose',
        action="store_true",
        help='Enter this argument to enable verbosity')
    PARSER.add_argument(
        '-s',
        '--save',
        help=
        'Save all urls in a sqlite-database. For this purpose append a database'
        ' name to this argument (e.g. ... -s url_monkey ...)')
    PARSER.add_argument(
        'url',
        help='Enter a valid url to start the infinite search for all branches '
        'and trees surrounding it (as example: https://www.python.org/)')

    return PARSER.parse_args()


def write_urls_to_db(args, url_monkey):
    """ database monkey wrapper to clean up main function """

    # database name defined by user
    db = args.save + '.db'

    # create database monkey
    CHIMP = DatabaseMonkey(db)
    CHIMP.attach_to_urlmonkey(url_monkey)

    # the number of urls found by the url-monkey
    number_of_urls = str(len(url_monkey.trees_and_branches))

    # information for the user and save data to database
    print("Writing {} urls to database {}...".format(number_of_urls, db))
    CHIMP.parse_urllist()
    print("Done...")


def main():
    """ just a wrapper function """

    # read user arguments
    ARGS = create_args()
    # create url-monkey
    DONKEY_KONG = UrlMonkey()

    # start search for trees/urls
    print("Your monkey starts his tree search...")
    DONKEY_KONG.search(ARGS.verbose, ARGS.url)
    print("\nYour monkey finished his tree search...")

    # if wanted, write trees/urls to database
    if (ARGS.save):
        write_urls_to_db(ARGS, DONKEY_KONG)


if __name__ == '__main__':
    main()