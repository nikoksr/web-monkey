""" imports """
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

        # this is going to be the list filled with trees and branches that are #    already known
        self.trees_and_branches = []
        self.verbose = False

    @staticmethod
    def __get_tree_root(tree):
        """ 
        Returns the root of a tree (main-url of a sub-url) 
        e.g.:   tree: https://www.python.org/about/
                root: https://www.python.org/
        """
        # occurrences of slash ('/')
        counter = 0

        # iterate through string and return index of third slash
        for i in range(len(tree)):
            if (tree[i] == '/'):
                counter += 1
                if (counter == 3):
                    return tree[:i + 1]

        # append a slash if less than three slashes were found
        return (tree + '/')

    def __investigate_tree(self, branches, root):
        """ iterate through all branches of the tree """

        for branch in branches:
            # find all href attributes
            branch = branch.get('href')

            if (branch is None):
                continue

            # check if the link found is a new tree(main-url) or a      #   branch(sub-url)
            # in case of sub-url append it to its root url to make a    #   full and wokring url
            if (not branch.startswith('http')):
                while (branch.startswith('/')):
                    branch = branch[1:]
                branch = root + branch

            # check if url ends with '/'
            # important for later on when appending sub-urls
            if (not branch.endswith('/')):
                branch += '/'

            # check if branch or tree is already known and add it to
            #   the list if not
            if (branch in self.trees_and_branches):
                continue

            self.trees_and_branches.append(branch)

            if (self.verbose is True):
                print('\t> ' + branch)

    def __go_through_tree_list(self):
        """ 
        iterate through list of known trees and branches and
        investigate each
        """

        for known_tree in self.trees_and_branches:
            if (self.verbose is True):
                print('> ' + known_tree)

            # giving timeout of 10 seconds
            # prevent infinite requests
            try:
                search_branches = requests.get(known_tree, timeout=10.0)
            except requests.exceptions.Timeout:
                if (self.verbose is True):
                    print("\t> timed out...")
                continue

            # check status-code returned by url
            # filter codes other than 200(ok code)
            if (search_branches.status_code != 200):
                status_code = str(search_branches.status_code)

                if (self.verbose is True):
                    print("\t> returned " + status_code + "(bad code)...")
                continue

            # parse html of requested page
            branches = BeautifulSoup(search_branches.content, 'html.parser')
            # find all a-tags
            branches = branches.find_all('a')

            if (branches is None):
                continue

            # extract root and investigate the tree
            root = self.__get_tree_root(known_tree)
            self.__investigate_tree(branches, root)

    def search(self, verbose, tree=None):
        """ Searches for new trees starting from the root """

        self.verbose = verbose

        # check if user provided an url
        if tree is None:
            print('No url was provided.')
            return

        # check if url ends with '/'
        # important for later on when appending sub-urls
        if (not tree.endswith('/')):
            tree += '/'

        # add starting-tree to list
        self.trees_and_branches.append(tree)

        try:
            self.__go_through_tree_list()
        except KeyboardInterrupt:
            pass
