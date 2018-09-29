""" imports """
import argparse
from bs4 import BeautifulSoup
import requests


class PicMonkey():
    """
    A monkey that either finds all pictures on a website
    or searches for a picture with a specified tag
    """

    @staticmethod
    def __format_pic_url(tree, branch):
        """ Formats a given url to the wanted standard format """

        if branch[0] == '/':
            branch = branch[1:len(branch)]

        if branch[0:4] != 'http' and tree[0:4] == 'http':
            i = tree.find('/', 8, len(tree))

            if i != -1:
                tree = tree[0:(i + 1)]

            if '.' in tree[(len(tree) - 4):len(tree)]:
                tree = tree + '/'

            return tree + branch

        return branch

    @staticmethod
    def __find_leafs(tree):
        """
        Finds leafs in a given tree
        Leafs represent pictures which are found at the different branches of a tree
        """

        search_branches = requests.get(tree)
        branches = BeautifulSoup(search_branches.content, 'html.parser')
        leafs = branches.find_all('img')

        return leafs

    def look_for_specific_pics(self, tree=None, tag=None):
        """ Searches for pictures which include the given tag """

        if tree is None or tag is None:
            print('Invalid link or tag')
            return

        tag = tag.lower()

        try:
            leafs = self.__find_leafs(tree)

            if leafs is None:
                return

            for leaf in leafs:
                src = leaf.get('src')
                alt = leaf.get('alt')

                if not src or not alt:
                    continue

                if tag in src or tag in alt:
                    print(self.__format_pic_url(tree, src))

        except KeyboardInterrupt:
            pass

    def look_for_all_pics(self, tree=None):
        """ Searches for all pictures on a given website """

        if tree is None:
            print('Invalid URL')
            return

        try:
            leafs = self.__find_leafs(tree)

            if leafs is None:
                return

            for leaf in leafs:
                src = leaf.get('src')

                if src is None or not src:
                    continue

                print(self.__format_pic_url(tree, src))

        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument(
        "url",
        help="Enter a valid url to "
        "start the search for "
        "all pictures on this "
        "website")
    PARSER.add_argument("--tag", help="Enter a tag to specify your search")
    ARGS = PARSER.parse_args()
    DONKEY_KONG = PicMonkey()

    if ARGS.tag:
        DONKEY_KONG.look_for_specific_pics(ARGS.url, ARGS.tag)
    else:
        DONKEY_KONG.look_for_all_pics(ARGS.url)
