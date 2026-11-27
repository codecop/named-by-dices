#!/bin/sh
# Build script for 03_roguelike (exempt from the naming skill): run the tests.
cd "$(dirname "$0")" && python3 -m unittest discover -s test -t . -p '*_test.py'
