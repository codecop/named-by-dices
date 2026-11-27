#!/bin/sh
# Build script for 03_roguelike (exempt from the naming skill): run the game.
cd "$(dirname "$0")" && python3 -m src.main "$@"
