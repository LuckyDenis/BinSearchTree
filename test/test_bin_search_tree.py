# -*- coding: utf8 -*-


import pytest
import math
from random import randint

from bin_search_tree import BinSearchTree


def create_tree():
    """
    Create and return tree
    """
    return BinSearchTree()


def test_this_bin_search_tree():
    """
    Check bin tree is bin search tree

    test 1: check in tree
    """

    tree = create_tree()
    for i in range(100):
        tree.insert(i, i)

    min_key = - math.inf
    max_key = math.inf

    # test 1: check in tree
    def check(node, min_key, max_key):
        if node is None:
            return True
        if min_key < node.key < max_key:
            return check(node.left, min_key, node.key) and check(node.right, node.key, max_key)
        return False

    assert check(tree.root, min_key, max_key)


def test_insert():
    """
    Check insert in tree

    test 1: check for duplicate key insertion
    # test 2: inserting a large number of large elements
    """

    tree = create_tree()

    # test 1: check for duplicate key insertion
    for i in range(1000):
        tree[randint(1, 100)] = i
    assert len(tree) == 100
    tree.clear_tree()

    # test 2: inserting a large number of large elements
    for i in range(100000):
        tree[randint(1, 1000)] = i
    assert len(tree) == 1000
    tree.clear_tree()


def test_del_root():
    """
    Check del root

    test 1: root and right child, del root
    test 2: root and left child, del root
    """

    tree = create_tree()

    # test 1: root and right child, del root
    tree[3] = 3
    tree[4] = 4
    del tree[3]
    assert len(tree) == 1
    assert tree[4] == 4
    assert tree.root.has_any_children() is None
    tree.clear_tree()

    # test 2: root and left child, del root
    tree[3] = 3
    tree[2] = 2
    del tree[3]
    assert len(tree) == 1
    assert tree[2] == 2
    assert tree.root.has_any_children() is None
    tree.clear_tree()


def test_del_element():
    """
    delete element

    test 1: delete all element in tree
    """

    tree = create_tree()

    # test 1: delete all element in tree
    for i in range(100000):
        tree[randint(1, 10000)] = i

    for i in range(1, len(tree) + 1):
        del tree[i]
    assert len(tree) == 0
    tree.clear_tree()
