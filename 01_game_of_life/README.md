# 01 Game of Life

Conway's Game of Life with an ASCII console UI. See [requirement.md](requirement.md).

## Build and test

```
mvn test
mvn package
```

## Run

```
java -jar target/IServiceProcessor-1.0-SNAPSHOT.jar [--cols N] [--rows N] [--delay MS] [--wrap] [--random]
```

Defaults: 40x20 grid, tick 200 ms, glider + blinker seed, edges clipped.

Keys: `[space]` pause/resume, `[s]` single step, `[+/-]` faster/slower, `[t]` toggle toroidal wrap, `[q]` or Ctrl+C quit.

## Demo

Screenshots and an animated GIF of a real run: [docs/demo.gif](docs/demo.gif), [docs/frame-generation-0.png](docs/frame-generation-0.png). Created with the `capture-demo` skill.

## Naming

All code names (package, classes, methods, fields, variables) are random dice names from `../bin/dices`, following the `naming` skill. Only test method names are descriptive (`<state>_<act>_<expected>`).
