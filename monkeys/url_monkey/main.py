from url_monkey import UrlMonkey
from db_monkey import DatabaseMonkey
from argparse import ArgumentParser


def create_args():
    """ arparse wrapper to clean up main function """

    parser = ArgumentParser()
    parser.add_argument(
        '-v',
        '--verbose',
        action="store_true",
        help='Enter this argument to enable verbosity')
    parser.add_argument(
        '-s',
        '--save',
        help=
        'Save all urls in a sqlite-database. For this purpose append a database'
        ' name to this argument (e.g. ... -s url_monkey ...)')
    parser.add_argument(
        'url',
        help='Enter a valid url to start the infinite search for all branches '
        'and trees surrounding it (as example: https://www.python.org/)')

    return parser.parse_args()


def write_urls_to_db(args, url_monkey):
    """ database monkey wrapper to clean up main function """

    # database name defined by user
    db_name = args.save + '.db'

    # create database monkey
    chimp = DatabaseMonkey(db_name)
    chimp.attach_to_urlmonkey(url_monkey)

    # the number of urls found by the url-monkey
    number_of_urls = str(len(url_monkey.trees_and_branches))

    # information for the user and save data to database
    print("Writing {} urls to database {}...".format(number_of_urls, db_name))
    chimp.parse_urllist()
    print("Done...")


def main():
    """ just a wrapper function """

    # read user arguments
    args = create_args()
    # create url-monkey
    donkey_kong = UrlMonkey(args.verbose)

    # start search for trees/urls
    print("Your monkey starts his tree search...")
    donkey_kong.search(args.url)
    print("\nYour monkey finished his tree search...")

    # if wanted, write trees/urls to database
    if args.save:
        write_urls_to_db(args, donkey_kong)


if __name__ == '__main__':
    main()
