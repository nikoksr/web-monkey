""" imports """
import argparse

import requests
from bs4 import BeautifulSoup


class UrlMonkey():
    """
    Web crawler class called (url-)monkey
        * They swing from tree to tree and discover branches and new trees
        * Every tree represents a main-url
            (e.g.   - main: https://www.python.org/
                    - main: https://www.google.com/)
        * Every branch represents a sub-url
            (e.g.   - main: https://www.python.org/
                    - sub:  https://www.python.org/about/)
        * Every unique tree or branch gets reported to the user
    """

    def __init__(self):
        """ Inits urlmonkey class with an empty tree list """
        self.known_trees = []

    def get_tree_root(self, tree=None):
        """ 
        Returns the root of a tree (main-url of a sub-url) 
        e.g.:   tree: https://www.python.org/about/
                root: https://www.python.org/
        """

        third_slash = 0
        counter = 0

        for i in range(len(tree)):
            if (tree[i] == '/'):
                counter += 1
                if (counter == 3):
                    third_slash = i

        root = tree[:third_slash + 1]

        return root

    def find_trees(self, tree=None):
        """ Searches for new trees starting from the root """
        if tree is None:
            print('Invalid URL')
            return

        if (not tree.endswith('/')):
            tree += '/'

        self.known_trees.append(tree)

        try:
            for known_tree in self.known_trees:
                print('> ' + known_tree)

                root = self.get_tree_root(known_tree)

                search_branches = requests.get(known_tree)
                branches = BeautifulSoup(search_branches.content,
                                         'html.parser')
                branches = branches.find_all('a')

                if (branches is None):
                    continue

                for branch in branches:
                    branch = branch.get('href')

                    if (branch is None):
                        continue

                    if (branch[0:4] != 'http'):
                        while (branch.startswith('/')):
                            branch = branch[1:]

                        branch = root + branch

                    if (branch in self.known_trees):
                        continue

                    self.known_trees.append(branch)
                    print('\t> ' + branch)
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument(
        "url",
        help="Enter a valid url to start the infinite search for all branches "
        "and trees surrounding it")

    ARGS = PARSER.parse_args()
    DONKEY_KONG = UrlMonkey()
    DONKEY_KONG.find_trees(ARGS.url)
