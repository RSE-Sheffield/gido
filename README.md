# gido — git into dot

Display `git` repo as graph network using `dot`.

## Install

    # from pypi
    python -m pip install gido

    # from a clone:
    python -m pip install .

Instructions for developers, who may need to build wheel files
or create editable installs, can be found in a section at the
end of this file.

## Usage

    gido

`gido` outputs [DOT graph description language](https://en.wikipedia.org/wiki/DOT_%28graph_description_language%29).
It is probably more useful to use `dot` to convert to PNG:

    gido | dot -Tpng > log.png

or, if using `kitty` or a similar terminal program capable of
displaying PNG files:

    gido | dot -Tpng | kitty icat

The result is a graphical image of the network graph of your git
repo:

![A directed graph showing this repo's ancestral structure](asset/example-202012.png "output of gido | dot -Tpng")

## Extra options

Additional options can be given, and at least in this
version they get passed to the `git log` command.

Some uses of this:

Show all branches (instead of just the current one):

    gido --all

Limit the output to the most recent 99 entries (for large repos
which can exceed the largest PNG file allowed by the PNG
format):

    gido -n 99

Most options are likely to disrupt the parsing of the output of
`git log` and are therefore not recommended.

## For `gido` developers

`pip` and `wheel` are recommend to build a wheel file:

    python -m pip wheel .

Which can be uploaded to PyPI using `twine`:

    python -m twine upload *.whl

Because there is a stub `setup.py` an editable install can be
made with:

    python -m pip install -e .

There is CI running on gitlab.
∎
