#!/bin/sh
# Build script for 03_roguelike (exempt from the naming skill): one line for the tests, one line for the game.
cd "$(dirname "$0")" && python3 -m unittest discover -s test -t . -p '*_test.py'
cd "$(dirname "$0")" && python3 -m src.main "$@"
