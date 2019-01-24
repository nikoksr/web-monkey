#!/usr/bin/python3
''' imports '''
import sys
from argparse import ArgumentParser

from plot_monkey import PlotMonkey


def create_args():
    ''' Arparse wrapper to define possible user args and
    clean up the main function. '''

    PARSER = ArgumentParser()
    PARSER.add_argument(
        '--pie',
        action='store_true',
        help='Create a pie plot based on a given database.')
    PARSER.add_argument(
        'db', help='Enter a valid path to a sqlite db created by an UrlMonkey')

    return PARSER.parse_args()


def evaluate_args(args):
    ''' Evaluate the arguments. Make sure the right amount
    of args was given. '''

    ARGS_NEEDED = 1
    ARGS_PROVIDED = len(sys.argv) - 2

    # Check if enough args have been provided.
    # It needs at least a database path and a plot.
    if ARGS_PROVIDED < ARGS_NEEDED:
        return 1, ('Not enough args were provided. '
                   f'{ARGS_PROVIDED} provided and {ARGS_NEEDED} needed.')

    # Check if too many args have been provided.
    # Only one plot can be chosen.
    if ARGS_PROVIDED > ARGS_NEEDED:
        return 2, ('Too many args were provided. '
                   f'{ARGS_PROVIDED} provided and {ARGS_NEEDED} needed.')

    return 0, ''


def main():
    ''' Main function '''

    # Read user arguments
    ARGS = create_args()

    # Evaluate the args
    res = evaluate_args(ARGS)

    if res[0] != 0:
        print(res[1])
        sys.exit(1)

    # Create PlotMonkey and run corresponding plot function
    charlie = PlotMonkey(ARGS.db)

    if not charlie:
        print('Could\'t create the PlotMonkey.\'')
        sys.exit(2)

    if ARGS.pie:
        charlie.display_pie()


if __name__ == '__main__':
    main()
