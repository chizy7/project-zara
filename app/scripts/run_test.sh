#!/bin/bash

#$PWD/python3-virtualenv/bin/python3 -m unittest discover -v tests/

$(dirname "$0")/../../python3-virtualenv/bin/python3 -m unittest discover -v $(dirname "$0")/../../tests/
