''' imports '''
import re
import time

import requests
from bs4 import BeautifulSoup


class UrlMonkey():
    '''
    Web crawler class called (url-)monkey
        * They swing from tree to tree and discover branches and new trees
        * Every tree represents a main-url
            (e.g.   - main: https://www.python.org/
                    - main: https://www.google.com/)
        * Every branch represents a sub-url
            (e.g.   - main: https://www.python.org/
                    - sub:  https://www.python.org/about/)
        * Every unique tree or branch gets reported to the user
    '''

    def __init__(self, verbose):
        ''' Init urlmonkey class with an empty tree list. '''

        # The list to be filled with trees and branches that are already known.
        # It's going to be multi-dimensional. The first value
        #  will be the tree/url and the second value will be the url under
        #  which the current url was found.
        self.trees_and_branches = []

        # User choice for verbosity
        self.verbose = verbose

    @staticmethod
    def extract_root(tree):
        '''
        Returns the root of a tree (main-url of a sub-url)
          e.g.:   tree: https://www.python.org/about/
                  root: https://www.python.org/
        '''

        tree_re = re.compile(
            r'''
                (https?://|ftp://)  # protocol
                ([A-Za-z.-]{4,}/?)   # domain and countrycode
                (.*)                # rest of url
            ''', re.VERBOSE)
        mo = tree_re.search(tree)
        tree = mo[1] + mo[2]
        if not tree.endswith('/'):
            tree += '/'
        return tree

    @staticmethod
    def format_branch(branch, root):
        '''
        Checks the origin of a branch.
        Does the branch come from a different tree or is it a
        branch of the current tree?
        If the branch-url starts with http or ftp it comes from a different
        tree - does not need to be formatted.
        Else format the url so that it can be appended to its root url.
        Formats the branch-url depending on its origin.
        '''

        if not branch.endswith('.html') and not branch.endswith('/'):
            branch += '/'

        if branch.startswith('http') or branch.startswith('ftp'):
            return branch

        branch_re = re.compile(r'(/*)?(.+)')
        return root + branch_re.search(branch)[2]

    def is_tree_known(self, tree):
        ''' Tests if a given tree is already in the list '''

        for known_tree in self.trees_and_branches:
            if tree == known_tree[0]:
                return 1
        return 0

    def investigate_tree(self, branches, current_tree):
        ''' Iterate through all branches of a tree. '''

        # Find the root of the current tree
        # e.g.: current tree    = https://www.python.org/downloads
        #       root            = https://www.python.org/
        root = self.extract_root(current_tree)

        for branch in branches:
            # Find all href attributes
            branch = branch.get('href')

            if branch is None:
                continue

            # Check if the link is a new tree(main-url) or a
            # branch(sub-url). In case of a sub-url append it to its root-url
            # to create a working url.
            branch = branch.strip()
            branch = self.format_branch(branch, root)

            # Check if branch or tree is already known and add it to
            # the list if not.
            if self.is_tree_known(branch):
                continue

            # Found new branch
            self.trees_and_branches.append([branch, current_tree])

            if self.verbose is True:
                print('\t> ' + branch)

    def go_through_tree_list(self):
        '''
        Iterate through list of known trees and branches and
        investigate each.
        '''

        for known_tree in self.trees_and_branches:
            tree = known_tree[0]

            if self.verbose is True:
                print('> ' + tree)

            # Prevent instability due to too rapid requests
            time.sleep(0.01)
            try:
                # Giving timeout of 10 seconds to prevent infinite request-time
                search_branches = requests.get(tree, timeout=10.0)
            except requests.exceptions.Timeout:
                if self.verbose is True:
                    print('\t> timed out...')
                continue

            # Check status-code returned by url
            # Filter codes other than 200(ok code)
            if search_branches.status_code != 200:
                status_code = str(search_branches.status_code)

                if self.verbose is True:
                    print('\t> returned ' + status_code + '(bad code)...')
                continue

            # Parse html of requested page
            branches = BeautifulSoup(search_branches.content, 'html.parser')
            # Find all a-tags
            branches = branches.find_all('a')

            if branches is None:
                continue

            # Investigate the tree
            self.investigate_tree(branches, tree)

    def search(self, tree):
        ''' Searches for new trees starting from the root. '''

        # Check if user provided an url
        if tree is None:
            print('No url was provided.')
            return

        # Check if url ends with '/' - important for later on when
        # appending sub-urls.
        if not tree.endswith('/'):
            tree += '/'
        tree = tree.strip()

        # Add starting-tree to list
        self.trees_and_branches.append([tree, 'None'])

        try:
            self.go_through_tree_list()
        except KeyboardInterrupt:
            pass
