# gido — git into dot

Install:
    # from pypi
    python -m pip install gido

    # from a clone:
    python -m pip install .


Usage:
    ./gido.py

`gido` outputs [DOT graph description language](https://en.wikipedia.org/wiki/DOT_%28graph_description_language%29),
so it is probably more useful to use `dot` to convert to PNG:

    ./gido.py | dot -Tpng > log.png

or, if using `kitty` or a similar terminal program capable of
displaying PNG files:

    ./gido.py | dot -Tpng | kitty icat

