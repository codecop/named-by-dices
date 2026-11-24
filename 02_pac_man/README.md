# 02 Pac-Man

Console Pac-Man in plain C (C99). See [requirements.md](requirements.md).

## Build and test

```
make                # builds build/pacman
make test           # builds and runs the cmocka unit tests (needs cmocka, e.g. sudo apt-get install libcmocka-dev)
make CMOCKA_PREFIX=/path/to/cmocka test   # use a cmocka installed in a custom prefix
make smoke          # headless smoke runs: piped input and a pseudo-terminal run
make coverage       # runs tests + smoke runs under gcov/lcov and writes docs/coverage-report + docs/coverage.md data
```

## Run

```
./build/pacman
```

Keys: `[W]` up, `[A]` left, `[S]` down, `[D]` right, `[Q]` quit. Ctrl+C also quits.

## Demo

Animated GIF of a real headless run (Pac-Man eats dots, grabs a power pellet, ghosts turn frightened): [docs/demo.gif](docs/demo.gif). Frames: [docs/frame-move-0.png](docs/frame-move-0.png), [docs/frame-move-9.png](docs/frame-move-9.png), [docs/frame-move-18.png](docs/frame-move-18.png). Created with the `capture-demo` skill.

## Layout

```
src/        game code (maze, actor, ghost, game rules, renderer, console UI loop, entry point)
src/test/   cmocka unit tests and the pty smoke script (tests live with the code)
docs/       coverage documents only (coverage.md, coverage-report/)
```

## Naming

All code names (files, types, functions, fields, variables, macros) are random dice names from `../bin/dices`, following the `naming` skill. Only test method names are descriptive (`<state>_<act>_<expected>`).
