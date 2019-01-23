''' imports '''
from argparse import ArgumentParser

from db_monkey import DatabaseMonkey
from url_monkey import UrlMonkey


def create_args():
    ''' arparse wrapper to clean up main function '''

    PARSER = ArgumentParser()
    PARSER.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Enter this argument to enable verbosity')
    PARSER.add_argument(
        '-s',
        '--save',
        help='''Save all urls in a sqlite-database. For this purpose append a
        database name to this argument (e.g. ... -s url_monkey ...)''')
    PARSER.add_argument(
        'url',
        help='Enter a valid url to start the infinite search for all branches '
        'and trees surrounding it (as example: https://www.python.org/)')

    return PARSER.parse_args()


def write_urls_to_db(args, url_monkey):
    ''' database monkey wrapper '''

    # Database name defined by user
    db_name = args.save
    if not db_name.endswith('.db'):
        db_name += '.db'

    # Create database monkey
    CHIMP = DatabaseMonkey(db_name)
    CHIMP.attach_to_urlmonkey(url_monkey)

    # The number of urls found by the url-monkey
    number_of_urls = str(len(url_monkey.trees_and_branches))

    # Information for the user and save data to database
    print(f'Writing {number_of_urls} urls to database {db_name}...')
    CHIMP.parse_urllist()
    print('Done...')


def main():
    ''' main wrapper function '''

    # Read user arguments
    ARGS = create_args()
    # Create url-monkey
    DONKEY_KONG = UrlMonkey(ARGS.verbose)

    # Start search for trees/urls
    print('Your monkey is starting his tree search...')
    DONKEY_KONG.search(ARGS.url)

    # Finish run
    NUM_TREES = len(DONKEY_KONG.trees_and_branches)
    print('\nYour monkey finished his tree search...')
    print(f'He found {NUM_TREES} urls...')

    # If wanted, write trees/urls to database
    if (ARGS.save):
        write_urls_to_db(ARGS, DONKEY_KONG)


if __name__ == '__main__':
    main()
