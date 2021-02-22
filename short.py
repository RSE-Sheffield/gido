#!/usr/bin/env python

# https://docs.python.org/3.7/library/itertools.html
import itertools
import sys


def main():
    for p in short(sys.stdin):
        print(*p)


def short(inp):
    """
    Intended to be used to converted a sequence of
    strings to the shortest unique prefix for each string.
    For each string in the inp sequence,
    the shortest prefix that is different to both of its neighbours
    (before and after in the sorted sequence) is computed.
    A pair (string, prefix) is yielded for each input string.

    Because the input is sorted internally, the output is not
    necessarily in the same order as the input.
    """

    # See pairwise pattern in
    # https://docs.python.org/3.7/library/itertools.html#itertools-recipes
    rows = itertools.chain([""], sorted(inp), [""])
    a, b = itertools.tee(rows)
    next(b)
    b, c = itertools.tee(b)
    next(c)

    triples = zip(a, b, c)
    for t in triples:
        before, curr, after = t
        good = max(preflen(curr, before), preflen(curr, after), key=len)
        yield curr, good


def preflen(subject, pattern):
    """
    What is the shortest prefix of subject that is
    not the same as the (same length) prefix of pattern?
    Return the prefix as a string.
    """

    for i in range(len(subject) + 1):
        if subject[:i] != pattern[:i]:
            return subject[:i]

    raise Exception("subject is a prefix of pattern")


if __name__ == "__main__":
    main()
