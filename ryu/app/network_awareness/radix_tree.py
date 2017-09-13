#!/usr/bin/env python
#coding: utf-8
from collections import deque
from shortest_forwarding import *  ####

class Node(object):

    def __init__(self, prefix=None, action=None, name=None,
                 parent=None, left_child=None, right_child=None,
                 aggregated=False,in_port=None,eth_type=None,ipv4_src=None,ipv4_dst=None):
        self._prefix = prefix
        self._action = action
        self._name = name
        self._parent = parent
        self._left_child = left_child
        self._right_child = right_child
        self._aggregated = aggregated
        self._in_port = in_port
        self._eth_type = eth_type
        self._ipv4_src = ipv4_src
        self._ipv4_dst = ipv4_dst


    def has_left_child(self):
        return self._left_child is not None

    def has_right_child(self):
        return self._right_child is not None

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        self._prefix = value

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        self._action = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def left_child(self):
        return self._left_child

    @left_child.setter
    def left_child(self, value):
        self._left_child = value

    @property
    def right_child(self):
        return self._right_child

    @right_child.setter
    def right_child(self, value):
        self._right_child = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def aggregated(self):
        return self._aggregated

    @aggregated.setter
    def aggregated(self, value):
        self._aggregated = value

    @property
    def in_port(self):
        return self._in_port

    @in_port.setter
    def in_port(self, value):
        self._in_port = value

    @property
    def eth_type(self):
        return self._eth_type

    @eth_type.setter
    def eth_type(self, value):
        self._eth_type = value

    @property
    def ipv4_src(self):
        return self._ipv4_src

    @ipv4_src.setter
    def ipv4_src(self, value):
        self._ipv4_src = value

    @property
    def ipv4_dst(self):
        return self._ipv4_dst

    @ipv4_dst.setter
    def ipv4_dst(self, value):
        self._ipv4_dst = value

class RadixTree(object):

    def __init__(self, root):
        if root is not None:
            self.root = root
        else:
            self.root = Node()

    def __contains__(self, item):
        node_list = self.level_traverse()
        for node in node_list:
            if node.prefix == item.prefix:
                return True
        return False

    def add(self, node, parent=None):
        if parent == None:
            parent = self.root
        self._add(node, parent, 0)

    def _add(self, node, parent, level):
        if node.prefix[level] == '0':
            if level == len(node.prefix) - 1:
                parent.left_child = node
                node.parent = parent # set the node's parent
                return
            else:
                if not parent.has_left_child():
                    parent.left_child = Node(parent=parent,
                                             prefix=node.prefix[0:level+1])
                self._add(node, parent.left_child, level+1)
        if node.prefix[level] == '1':
            if level == len(node.prefix) - 1:
                parent.right_child = node
                node.parent = parent
                return
            else:
                if not parent.has_right_child():
                    parent.right_child = Node(parent=parent,
                                              prefix=node.prefix[0:level+1])
                self._add(node, parent.right_child, level+1)

    def level_traverse(self):
        result = list()
        q = deque()
        q.append(self.root)
        while q:
            node = q.popleft()
            result.append(node)
            if node.left_child is not None:
                q.append(node.left_child)
            if node.right_child is not None:
                q.append(node.right_child)
        return result

    def show(self):
        if self.root is not None:
            self._show(self.root)

    def _show(self, node):
        if node is not None:
            self._show(node.left_child)
            print 'name:' + str(node.name) + ' prefix:' + str(node.prefix) + ' action:' + str(node.action)
            self._show(node.right_child)


class Aggregator(object):

    def __init__(self, radix_tree):
        self.radix_tree = radix_tree

    def parent_child_aggr(self, node, node_list):
        if node.aggregated is True:
            return
        if node.parent in node_list \
            and node.prefix[0:-1] == node.parent.prefix \
            and node.action == node.parent.action:
                node.aggregated = True

    def sibling_aggr(self, node, node_list):
        if node.aggregated is True:
            return
        if node.prefix is None:
            return
        if node.prefix[-1] == '0':
            if node.parent.right_child is not None \
                and node.parent.right_child.aggregated is False:
                # node is the left child
                sibling_node = node.parent.right_child
            else:
                return
        if node.prefix[-1] == '1':
            if node.parent.left_child is not None \
                and node.parent.left_child.aggregated is False:
                # node is the right child
                sibling_node = node.parent.left_child
            else:
                return
        if sibling_node is not None \
            and node.parent in node_list \
            and node.parent.action is None \
            and node.action == sibling_node.action:
                node.parent.prefix = node.prefix[0:-1]
                node.parent.action = node.action
                node.aggregated = True
                sibling_node.aggregated = True


if __name__ == '__main__':
    root = Node(name='root')
    radix_tree = RadixTree(root=root)
    a = Node(prefix='00', action='A', name='a')
    b = Node(prefix='000', action='A', name='b')
    c = Node(prefix='001', action='A', name='c')
    d = Node(prefix='01', action='B', name='d')
    e = Node(prefix='010', action='B', name='e')
    f = Node(prefix='011', action='B', name='f')
    g = Node(prefix='110', action='C', name='g')
    radix_tree.add(a)
    radix_tree.add(b)
    radix_tree.add(c)
    radix_tree.add(d)
    radix_tree.add(e)
    radix_tree.add(f)
    radix_tree.add(g)
    radix_tree.show()
    print '-----------------------------'
    node_list = radix_tree.level_traverse()
    node_list.reverse()
    for node in node_list:
        print 'name:' + str(node.name)
        if node.parent is not None:
            print 'parent:' + str(node.parent.name)