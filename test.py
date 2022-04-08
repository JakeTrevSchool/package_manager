from enum import Enum

from pyparsing import col


class color(Enum):
    RED = "Red"
    BLACK = "Black"


class Node:
    def __init__(self, content):
        self.content: any = content
        self.parent: Node = None
        self.right: Node = None
        self.left: Node = None
        self.color: color = color.BLACK


class RBTree:
    def __init__(self):
        self.root: Node = None


def left_rotate(T: RBTree, x: Node):
    y = x.right
    x.right = y.left
    if (y.left != None):
        y.left.parent = x
    y.parent = x.parent
    if x.parent == None:  # if x is the root
        T.root = y
    elif x == x.parent.left:
        x.parent.left = y
    else:
        x.parent.right = y
    y.left = x
    x.parent = y


def right_rotate(T: RBTree, x: Node):
    y = x.left
    x.left = y.right
    if (y.right != None):
        y.right.parent = x
    y.parent = x.parent
    if x.parent == None:  # if x is the root
        T.root = y
    elif x == x.parent.right:
        x.parent.right = y
    else:
        x.parent.left = y
    y.right = x
    x.parent = y


def fixup(T: RBTree, z: Node):
    while z.parent.color == color.RED:
        if z.parent == z.parent.parent.left:
            y = z.parent.parent.right
            if y.color == color.RED:
                z.parent.color = color.BLACK
                y.color = color.BLACK
                z.parent.parent.color = color.RED
                z = z.parent.parent
            else:
                if z == z.parent.right:
                    z = z.parent
                z.parent.color = color.BLACK
                z.parent.parent.color = color.RED
                right_rotate(T, z.parent.parent)
        else: # symmetric to code above
            y = z.parent.parent.left
            if y.color == color.RED:
                z.parent.color = color.BLACK
                y.color = color.BLACK
                z.parent.parent = color.RED
                z = z.parent.parent
            else:
                if z == z.parent.left:
                    z = z.parent
                z.parent.color = color.BLACK
                z.parent.parent.color = color.RED
                left_rotate(T, z.parent.parent)
    T.root.color = color.BLACK
