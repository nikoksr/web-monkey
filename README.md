<h1 align="center">:monkey: Web Monkey</h1>

<p align="center">Small web-crawler created with the imagination of monkeys jumping from tree to tree.</p>

## :bulb: Idea

  * Url Monkey

    A monkey jumps on a tree which represents an url. On his way climbing up the tree
    the monkey discovers many branches which visualize sub-urls of the main-url.

    Example

    * main-url (tree):  https://www.python.org/
    * sub-url (branch): https://www.python.org/about/

    All of them are being noted on a list of known trees, but only if they aren't already
    known and noted at this point in time. On his way to the treetop the monkey eventually
    discovers branches which don't belong to the tree he's climbing, so he notes these aswell 
    and he keeps on climbing towards the top. Reaching the top the monkey has discovered every
    single branch surrounding his tree. He decides to take a look on his list of noted trees, 
    chooses the first tree on the list following his current tree and jumps over to it.

    He repeats this process over and over again.
    
  * Plot Monkey
    
    A monkey that takes a database, created by an UrlMonkey, and creates plots based on the data.
    He tries to visualize the connections and distribution of urls found under a given url.

  * Pic Monkey

    A monkey jumps on a tree and starts discovering its branches where he finds leafs. Leafs
    represent sub-objects of urls; pictures in this case. The monkey notes every leaf on his list 
    and after discovering every leaf the tree has to offer, the monkey returns the list to the user.
    The user now has a list of all pictures found under the given url.
    The user can give the monkey a search-tag to specify his search for leafs. The monkey is only 
    going to return leafs which match the wanted search-tag.

## :snake: Python

Python 3.7
