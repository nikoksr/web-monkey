Web Monkey
==========
Small webcrawler created with the imagination of monkeys jumping from tree to tree

Idea
====
A monkey jumps on a tree which represents an URL. On his way climbing up the tree
the monkey discovers many branches which visualize sub-urls of the main-url.

Example
* main-url(tree):  https://www.python.org/
* sub-url(branch): https://www.python.org/about/

All of them are being noted on a list of known trees, but only if they aren't already
known and noted at this point in time. On his way to the treetop the monkey eventually 
discovers branches which don't belong to the tree he's climbing, so he notes these aswell,
aslong as they are not already known and he keeps on climbing towards the top. Reaching the
top the monkey has discovered every single branch surrounding his tree. He decides to take
a look on his list of noted trees, chooses the first tree on the list following his current
tree and jumps over to it.

He repeats this process over and over again.

Python
======
Python 3.7 and pylint 2.1.1
