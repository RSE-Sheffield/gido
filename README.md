# gido — git into dot

Usage:
    ./gido.py

it outputs [DOT graph description language](https://en.wikipedia.org/wiki/DOT_%28graph_description_language%29),
so it is probably more useful to use `dot` to convert to PNG:

    ./gido.py | dot -Tpng > log.png

or, if using `kitty` or a similar terminal program capable of
displaying PNG files:

    ./gido.py | dot -Tpng | kitty icat

