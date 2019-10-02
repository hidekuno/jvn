#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#   This is python sample
#   hidekuno@gmail.com

import sys
import argparse
DELIMITER_CHAR = '.'

class Tree(object):
    def __init__(self, cname, parent = None):
        self.cname = cname
        self.parent = parent
        self.children = []

    def add(self, child):
        self.children.append(child)

    def accept(self, visitor):
        visitor.visit(self)

    def short_name(self):
        return self.cname[self.cname.rfind(DELIMITER_CHAR) + 1:]

class Visitor(object) :
    def __init__(self):
        pass

    def visit(self,tree, indent = 0):
        print((indent * "  ") + tree.short_name())

        for c in tree.children:
            self.visit(c, indent + 1)

class RuledLine(object):
    def __init__(self,p1,p2,m1,m2):
        self.p1 = p1
        self.p2 = p2
        self.m1 = m1
        self.m2 = m2

    def visit(self, tree):
        
        if (tree.parent):
            p = tree.parent
            horizon = []
            while p.parent:
                horizon.append(self.p1 if p.parent.children[-1] == p else self.p2)
                p = p.parent

            horizon.reverse()
            horizon.append(self.m1 if tree.parent.children[-1] == tree else self.m2)
            sys.stdout.write("".join(horizon))

        print(tree.short_name())
        for c in tree.children:
            self.visit(c)

def create_tree(istream):
    cache = {}

    for line in istream:
        rec = line.rstrip()

        items = ""
        for c in rec.split(DELIMITER_CHAR):
            if items:
                items  = items + DELIMITER_CHAR + c
            else:
                items  = c

            if items in cache:
                continue

            parent_name = items[:items.rfind(DELIMITER_CHAR)]

            if parent_name in cache:
                cache[items] = Tree(items, cache[parent_name])
                cache[parent_name].add(cache[items])
            else:
                cache[items] = Tree(items)
                fj = cache[items]
    return fj

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-l','--line',  action='store_true')
    parser.add_argument('-m','--mline', action='store_true')
    parser.add_argument('-f', '--filename',  type=str, dest='filename')
    args = parser.parse_args(sys.argv[1:])

    visitor = Visitor()
    istream = sys.stdin

    if args.line:
        visitor = RuledLine("   ","|  ", "`--" ,"|--" )
    if args.mline:
        visitor = RuledLine("　" ,"┃", "┗" ,"┣" )
    if args.filename:
        istream = open(args.filename, "r")
try:
    fj = create_tree(istream)
    fj.accept(visitor)

except Exception as e:
    traceback.print_exc()
