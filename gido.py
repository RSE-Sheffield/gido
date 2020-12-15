#!/usr/bin/env python3

# https://docs.python.org/3.7/library/subprocess.html
import subprocess

import sys

# Minimum supported Python version
assert sys.version_info >= (3, 7)


def main(argv=None):

    import argparse

    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser()
    parser.parse_args()

    inspect(parser)


def inspect(args):
    """
    Inspect the git repo and convert to dot format.
    """

    child = git("log", "--no-patch", "--pretty=%h %p -- %D")

    print( 'digraph G {')

    for row in child.stdout.split("\n"):
        # ignoring blank lines, in particular, the final one
        if not row: continue
        if '--' not in row:
            raise Exception("expected `--` in input")

        # Rename nodes so that they start with S,
        # making them valid lex tokens for dot.
        l = row.split()
        label = l[0]
        for i, n in enumerate(l):
            if n == '--':
                break
            l[i] = 'S' + l[i]

        # Output node label.
        print(l[0], '[ label = "' + label + '" ]')

        # Output an edge for each parent.
        i = 1
        while l[i] != '--':
            print(l[0], "->", l[i])
            i+=1

    print ("}")



def git(*args):
    """
    Run a git command.
    Returns a subprocess.CompletedProcess instance.
    """

    l = "git", *args
    return subprocess.run(l, capture_output=True, encoding="UTF-8")


if __name__ == "__main__":
    main()

# gido

"""
printf 'digraph G {\n'
git log --no-patch '--pretty=%h %p -- %D' "$@" |
  awk '{
    label = $1
    # Rename nodes so that they start with S, making them lexique.
    for(i=1; $i != "--"; i+=1){ $i = "S"$i }
    # Node label
    print $1, "[ label = \042" label "\042 ]"
    # An edge for each parent
    for(i=2; $i!="--"; i+=1) {
      print $1, "->", $i
    }
    i += 1
    # An exterior label for each branch/tag
    while(i<=NF) {
      print $1, "[ xlabel = \042" $i "\042 ]"
      i += 1
    }
  }'
printf '}\n'
"""
