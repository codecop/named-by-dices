# 03 Roguelike

Console roguelike in plain Python (3.13) with an ANSI terminal UI. See [requirements.md](requirements.md).

## Build and test

No third-party runtime dependencies; lint and coverage use pip packages only (`pip install pylint flake8 coverage`).

[run.sh](run.sh) has one line for the tests and one line for the game:

```
./run.sh
```

or directly:

```
python3 -m unittest discover -s test -t . -p '*_test.py'
python3 -m src.main [--seed N] [--data game.txt] [--save savegame.json] [--ui tty|stdin]
```

Lint (strict): `flake8 src test` and `PYTHONPATH=. pylint src test` (10.00/10).
Coverage (100%, branch coverage): `coverage run -m unittest discover -s test -t . -p '*_test.py'` then `coverage report -m` and `coverage html -d docs/coverage-report`; documents in [docs/coverage.md](docs/coverage.md) and [docs/coverage-report](docs/coverage-report).

## Run

```
python3 -m src.main [--seed N]
```

Keys: `[H][J][K][L]` or arrow keys (plus `y/u/b/n` diagonals) move and attack, `[.]` rest, `[>]` descend, `[<]` ascend, `[,]` pick up, `[I]` inventory, `[W]` wield weapon, `[Shift-W]` wear armour, `[Q]` quaff potion, `[R]` read scroll, `[Z]` zap wand, `[S]` save game, `[Shift-Q]` quit, `[?]` help.

Story arc: the dragon has stolen the Golden Die. Descend to the deepest level, take the artefact from the dragon's hall and escape via the up stairs on depth 1. If a saved game exists, the start menu offers to load it.

## UI seam

The game logic talks to a thin IO port (`ArollaBusinessFactory`: read command / write frame / save game); rendering is a pure function (`business_helper.utils_default`). Two UIs sit on the port: `--ui tty` (default on a terminal: `getch` via `msvcrt`/`termios`, arrow keys, ANSI) and `--ui stdin` (line-based test UI: one command per line on stdin, e.g. `h`, `down`, `get`, `save`, `quit`; EOF quits; default when stdin is piped). Example: `printf 'h\nl\ns\nquit\n' | python3 -m src.main --ui stdin --seed 1`.

## Game data

Everything about the world is configurable in [game.txt](game.txt): map size, depth, room count, field of view, start HP, monsters (letter, name, hp, attack, defence, xp, minimum depth), the friendly helper NPC, items (kind, letter, name, power) and traps. Add one line to extend the game. Override with `--data FILE`.

## Layout

```
src/        game code (config, dungeon generation, items, player, monsters, combat, fov, renderer, input, save/load, game engine, entry point)
test/       plain unittest suite, next to src
docs/       coverage documents only (coverage.md, coverage-report/)
game.txt    configurable game data
run.sh      one line for the tests, one line for the game
```

## Naming

All code names (files, classes, methods, fields, variables, parameters) are random dice names from `../bin/dices`, following the `naming` skill. Only test method names are descriptive (`test_<state>_<act>_<expected>`).
