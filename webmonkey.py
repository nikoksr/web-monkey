""" imports """
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

                search_trees = requests.get(known_tree)

                found_trees = BeautifulSoup(
                    search_trees.content, 'html.parser')

                trees = found_trees.find_all('a')

                if trees is None:
                    continue

                for tree in trees:
                    new_tree = tree.get('href')

                    if (new_tree is None
                            or new_tree[0:4] != 'http'
                            or new_tree in self.known_trees):
                        continue

                    self.known_trees.append(new_tree)
                    print('\t> ' + new_tree)
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    ROOT_URL = 'http://www.python.org'

    DONKEY_KONG = UrlMonkey()
    DONKEY_KONG.find_trees(ROOT_URL)
