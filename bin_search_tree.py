# -*- coding: utf8 -*-


class NodeTree:
    __slots__ = ['key', 'value', 'parent', 'left', 'right']

    def __init__(self, key, value, parent=None, left=None, right=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right

    # node has left child
    def has_left_child(self):
        return self.left

    # node has right child
    def has_right_child(self):
        return self.right

    # node.parent.left == node
    def is_left_knot(self):
        return self.parent and self.parent.left == self

    # node.parent.right == node
    def is_right_knot(self):
        return self.parent and self.parent.right == self

    def is_root(self):
        return not self.parent

    # node has not children
    def has_leaf(self):
        return not(self.left or self.right)

    # node has left or right child
    def has_any_children(self):
        return self.left or self.right

    # node has left and right child
    def has_both_children(self):
        return self.left and self.right

    # node is root, swap left or right child
    def replace_node_date(self, key, value, left, right):
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        if self.has_left_child():
            self.left.parent = self
        if self.has_right_child():
            self.right.parent = self

    def find_min(self):
        curr = self
        while curr.has_left_child():
            curr = curr.left
        return curr

    def find_successor(self):
        succ = None
        if self.has_right_child():
            succ = self.right.find_min()
        else:
            if self.parent:
                if self.is_left_knot():
                    succ = self.parent
                else:
                    self.parent.right = None
                    succ = self.parent.find_successor()
                    self.parent.right = self
        return succ

    # cut successor node
    def splice_out(self):
        if self.has_leaf():
            if self.is_left_knot():
                self.parent.left = None
            else:
                self.parent.right = None
        elif self.has_any_children():
            if self.has_left_child():
                if self.is_left_knot():
                    self.parent.left = self.left
                else:
                    self.parent.right = self.left
                self.left.parent = self.parent
            else:
                if self.is_left_knot():
                    self.parent.left = self.right
                else:
                    self.parent.right = self.right
                self.right.parent = self.right

    def __iter__(self):
        if self:
            if self.has_left_child():
                for element in self.left:
                    yield element
            yield self.key
            if self.has_right_child():
                for element in self.right:
                    yield element


class BinSearchTree:

    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def _insert(self, key, value, curr_node):
        # key in tree, if you want to insert a duplicate key, the condition is removed
        if key == curr_node.key:
            curr_node.value = value
        # find parent's node, way left
        elif key < curr_node.key:
            # node has left child, find next
            if curr_node.has_left_child():
                self._insert(key, value, curr_node.left)
            # node has not child, insert
            else:
                curr_node.left = NodeTree(key, value, parent=curr_node)
                self.size += 1
        else:
            # node has right child, find next
            if curr_node.has_right_child():
                self._insert(key, value, curr_node.right)
            # node has not child, insert
            else:
                curr_node.right = NodeTree(key, value, parent=curr_node)
                self.size += 1

    def insert(self, key, value):
        if self.root:
            self._insert(key, value, self.root)
        else:
            self.root = NodeTree(key, value)
            self.size += 1

    def __setitem__(self, key, value):
        self.insert(key, value)

    def _get(self, key, curr_node):
        # node is None, stop recursion
        if not curr_node:
            return None
        # return node
        elif key == curr_node.key:
            return curr_node
        # way left
        elif key < curr_node.key:
            return self._get(key, curr_node.left)
        # way right
        else:
            return self._get(key, curr_node.right)

    def get(self, key):
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res.value
            else:
                return None
        else:
            return None

    def __getitem__(self, key):
        return self.get(key)

    def __contains__(self, key):
        if self._get(key, self.root):
            return True
        else:
            return False

    def delete(self, key):
        # element in tree > 1
        if self.size > 1:
            # find remove node in tree
            node_to_remove = self._get(key, self.root)
            # if remove is not None
            if node_to_remove:
                self.remove(node_to_remove)
                self.size -= 1
            else:
                raise KeyError('key not in tree.')
        # root is one element in tree
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size -= 1
        else:
            raise KeyError('key not in tree.')

    def remove(self, curr_node):
        # node has not children
        if curr_node.has_leaf():
            # node.parent.left == node
            if curr_node.is_left_knot():
                curr_node.parent.left = None
            # node.parent.right == node
            else:
                curr_node.parent.right = None
        # node has two children
        elif curr_node.has_both_children():
            succ = curr_node.find_successor()
            succ.splice_out()
            curr_node.key = succ.key
            curr_node.value = succ.value
        # node has left or right child
        else:
            # node has left child
            if curr_node.has_left_child():
                # node.parent.left == node
                if curr_node.is_left_knot():
                    curr_node.left.parent = curr_node.parent
                    curr_node.parent.left = curr_node.left
                # node.parent.right == node
                elif curr_node.is_right_knot():
                    curr_node.left.parent = curr_node.parent
                    curr_node.parent.right = curr_node.left
                # node is root, swap left child
                else:
                    curr_node.replace_node_date(curr_node.left.key,
                                               curr_node.left.value,
                                               curr_node.left.left,
                                               curr_node.left.right)
            # node has right child
            else:
                # node.parent.left == node
                if curr_node.is_left_knot():
                    curr_node.right.parent = curr_node.parent
                    curr_node.parent.left = curr_node.right
                # node.parent.right == node
                elif curr_node.is_right_knot():
                    curr_node.right.parent = curr_node.parent
                    curr_node.parent.right = curr_node.right
                # node is root, swap right child
                else:
                    curr_node.replace_node_date(curr_node.right.key,
                                               curr_node.right.value,
                                               curr_node.right.left,
                                               curr_node.right.right)

    def __delitem__(self, key):
        self.delete(key)

    def __iter__(self):
        return self.root.__iter__()

    def clear_tree(self):
        self.root = None
        self.size = 0
