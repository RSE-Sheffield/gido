#!/usr/bin/env python3

"""
Same as gido.py but using gitpython instead.

From a git repo, produce a dot file.
"""


# https://docs.python.org/3.7/library/collections.html
import collections
# https://docs.python.org/3.7/library/itertools.html
import itertools
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
    return RepoDot(repo)


def RepoDot(repo):
    """
    Print a graphviz dot file that represents the repo (a
    GitPython repo instance).
    """

    nodes = Parents(repo)
    labels = Labels(repo)

    # a dict that maps from long name to short names
    shorten = Shortener(nodes)

    print("digraph G {")

    for node in nodes:
        # Output node label.
        label = shorten[node.name]
        print("S"+label, '[ label = "' + label + '" ]')

        # Output an edge for each parent.
        for parent in node.parent:
            print("S"+label, "->", "S"+shorten[parent])

        # Any branch / ref labels.
        # Fold all git labels into a single xlabel attribute.
        xlabels = labels.get(node.name)
        if xlabels:
            x_repr = r"\n".join(xlabels)
            print("S"+label, '[ xlabel = "' + x_repr + '" ]')

        while False:
            print(l[0], '[ xlabel = "' + l[i] + '" ]')
            i += 1

    print("}")


def Shortener(nodes):
    """
    For a given set of nodes (which are actually Kinship instances),
    return a dict that can be used to map from long name (key) to
    short name (value).
    """

    d = dict()

    names = NodeNames(nodes)
    short_names = short.short(names)
    for long_name, short_name in short_names:
        M = 5
        if len(short_name) < M:
            short_name = long_name[:M]
        d[long_name] = short_name

    return d


Kinship = collections.namedtuple("Kinship", "name parent")


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

    # The heads of this repo...
    refs = repo.heads
    # Plus all the refs (branches, basically) in remotes
    refs += list(itertools.chain(*[rem.refs for rem in repo.remotes]))

    found_commits = set()
    for ref in refs:
        found_commits |= set(repo.iter_commits(ref.commit, max_count=N))

    rs = []
    for commit in found_commits:
        rs.append(Kinship(str(commit), [str(p) for p in commit.parents]))

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
