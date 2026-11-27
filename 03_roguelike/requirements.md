# 03 Roguelike Requirements

Console Roguelike in Python. See <https://en.wikipedia.org/wiki/Roguelike> and <https://en.wikipedia.org/wiki/Hack_(video_game)>.

With

* classic look and feel
* story arc
* character development, e.g. attributes, skills, and more
* at least ten rooms, generated (different each game depending on seed), and more
* weapons, armour, potions, magic, enemies, helpers, npcs, treasure, traps, and more
* option to save game

## Console UI Sketch

TODO

## Components to build

TODO

## Implementation

* full Python setup, gitignore and more etc.
* Python 3.13
* plain unit test
* pip (if needed)
* no framework for console UI, use ANSI. For getChar use on Windows

  ```python
  class _GetchWindows(object):
      # see https://stackoverflow.com/a/510364/

      def __call__(self):
          import msvcrt
          return msvcrt.getch()


  getch = _GetchWindows()
  ```

* full code coverage with unit tests kept in task local `docs` folder.
* pylint & flake8 with struct rule set
* github ci action

MUST FOLLOW `naming` skill convention for all names.

DO NOT STOP UNTIL COMPLETE.
