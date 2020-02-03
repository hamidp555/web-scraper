#!/bin/sh

for i in `find . -type f -name "*.py"`
do
    pep8 $i
    pyflakes $i
    pylint $i
done

tail -f /dev/null