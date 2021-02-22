#!/usr/bin/env python3

"""
Same as gido.py but using gitpython instead.

From a git repo, produce a dot file.
"""

import collections
import sys

# https://gitpython.readthedocs.io/en/3.1.0/
import git


import short


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

    dir = "."
    repo = git.Repo(dir)
    nodes = Parents(repo)
    labels = Labels(repo)

    names = NodeNames(nodes)
    short_names = short.short(names)
    shorten = dict()
    for long_name, short_name in short_names:
        M = 5
        if len(short_name) < M:
            short_name = long_name[:M]
        shorten[long_name] = short_name

    print("digraph G {")

    for node in nodes:
        # Output node label.
        label = shorten[node.name]
        print("S"+label, '[ label = "' + label + '" ]')

        # Output an edge for each parent.
        for parent in node.parent:
            print("S"+label, "->", "S"+shorten[parent])

        # Any branch / ref labels
        for xlabel in labels.get(node.name, []):
            print("S"+label, '[ xlabel = "' + xlabel + '" ]')

        while False:
            print(l[0], '[ xlabel = "' + l[i] + '" ]')
            i += 1

    print("}")


Relationship = collections.namedtuple("Relationship", "name parent")


def Parents(repo):
    """
    Return the parents of all findable commits in the git repo.
    `repo` is expected to be a `gitpython` Repo instance,
    typically returned from `git.Repo(dirname)`.
    This function returns a sequence of nodes,
    with each node being represented by
    a ("node-name", ("parent-name, ...)) tuple.
    """

    N=99

    heads = repo.heads

    found_commits = set()
    for head in heads:
        found_commits |= set(repo.iter_commits(head.commit, max_count=N))

    rs = []
    for commit in found_commits:
        rs.append(Relationship(str(commit), [str(p) for p in commit.parents]))

    return rs


def Labels(repo):
    """
    Return a dictionary that maps from commit names (SHAs) to
    ref names (branches and tags).
    """

    labels = collections.defaultdict(list)
    for ref in repo.refs:
        labels[str(ref.commit)].append(str(ref))
    return dict(labels)


def NodeNames(nodes):
    """
    Return a set of all the names used (parents and node names).
    """

    names = set()
    for node in nodes:
        names.add(node.name)
        for parent in node.parent:
            names.add(parent)

    return names


if __name__ == "__main__":
    main()
