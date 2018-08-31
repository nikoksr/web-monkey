""" imports """
import argparse
from bs4 import BeautifulSoup
import requests


class UrlMonkey():
    """
    Web crawler class called (url-)monkey
        * They swing from tree to tree and discover
            branches and new trees
        * Every tree represents a main-url
            (e.g.   - main: https://www.python.org/
                    - main: https://www.google.com/)
        * Every branch represents a sub-url
            (e.g.   - main: https://www.python.org/
                    - sub:  https://www.python.org/about/)
        * Every unique tree or branch gets reported
            to the user
    """

    def __init__(self):
        """ Inits urlmonkey class with an empty tree list """
        self.known_trees = []

    def find_trees(self, root=None):
        """ Searches for new trees starting from the root """
        if root is None:
            print('Invalid URL')
            return

        try:
            self.known_trees.append(root)

            for known_tree in self.known_trees:
                print('> ' + known_tree)

                search_branches = requests.get(known_tree)
                branches = BeautifulSoup(search_branches.content,
                                         'html.parser')

                branches = branches.find_all('a')

                if branches is None:
                    continue

                for branch in branches:
                    branch = branch.get('href')

                    if (branch is None or branch[0:4] != 'http'
                            or branch in self.known_trees):
                        continue

                    self.known_trees.append(branch)
                    print('\t> ' + branch)
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument(
        "url",
        help="Enter a valid url to "
        "start the infinite search "
        "for all branches and trees "
        "surrounding it")

    ARGS = PARSER.parse_args()
    DONKEY_KONG = UrlMonkey()
    DONKEY_KONG.find_trees(ARGS.url)
