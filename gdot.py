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

    print("digraph G {")

    for node in nodes:
        # Output node label.
        print("S"+node.name, '[ label = "' + node.name + '" ]')

        # Output an edge for each parent.
        for parent in node.parent:
            print("S"+node.name, "->", "S"+parent)
        while False:
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

    dir = "."

    N=99

    repo = git.Repo(dir)
    heads = repo.heads

    found_commits = set()
    for head in heads:
        found_commits |= set(repo.iter_commits(head.commit, max_count=N))

    rs = []
    for commit in found_commits:
        rs.append(Relationship(str(commit), [str(p) for p in commit.parents]))

    return rs


if __name__ == "__main__":
    main()
