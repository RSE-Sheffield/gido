#!/usr/bin/env python3

"""
Same as gido.py but using gitpython instead.

From a git repo, produce a dot file.
"""

import collections
import sys

# https://gitpython.readthedocs.io/en/3.1.0/
import git


# Minimum supported Python version
assert sys.version_info >= (3, 7)


def main(argv=None):

    import argparse

    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser()
    ns, remainder = parser.parse_known_args()

    inspect(ns, remainder)


def inspect(ns, remainder):
    """
    Inspect the git repo and convert to dot format.
    """

    nodes = Parents()

    for node in nodes:
        print(node)

    return

    print("digraph G {")

    for row in child.stdout.split("\n"):
        # ignoring blank lines, in particular, the final one
        if not row:
            continue
        if "--" not in row:
            raise Exception("expected `--` in input")

        # Rename nodes so that they start with S,
        # making them valid lex tokens for dot.
        l = row.split()
        label = l[0]
        for i, n in enumerate(l):
            if n == "--":
                break
            l[i] = "S" + l[i]

        # Output node label.
        print(l[0], '[ label = "' + label + '" ]')

        # Output an edge for each parent.
        i = 1
        while l[i] != "--":
            print(l[0], "->", l[i])
            i += 1
        i += 1
        while i < len(l):
            print(l[0], '[ xlabel = "' + l[i] + '" ]')
            i += 1

    print("}")


Relationship = collections.namedtuple("Relationship", "name parent")


def Parents():
    """
    Return the parents of all findable commits in this git repo.
    A sequence of nodes is returned, with each node
    being represented by ("node-name", ("parent-name, ...))
    tuple.
    """

    return []


if __name__ == "__main__":
    main()
