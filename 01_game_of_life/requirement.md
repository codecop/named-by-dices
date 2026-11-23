# Game of Life Requirements

See <https://en.wikipedia.org/wiki/Conway's_Game_of_Life>

## Rules (B3/S23)

1. Any live cell with fewer than two live neighbours dies (underpopulation).
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies (overpopulation).
4. Any dead cell with exactly three live neighbours becomes a live cell (reproduction).

## Implementation Tasks (ASCII console UI)

| # | Task | Description |
| --- | ------ | ------------- |
| 1 | Grid model | 2D array of fixed size, each cell alive/dead |
| 2 | Neighbour counting | Count live cells in the 8-cell Moore neighbourhood (handle edges) |
| 3 | Next-generation step | Pure function applying the 4 rules simultaneously to every cell |
| 4 | ASCII renderer | Print grid to console: block char for alive, dot/space for dead, with border and generation counter |
| 5 | Console UI loop | Clear screen between frames, fixed tick delay, run generations, Ctrl+C to quit |
| 6 | Seed / initial pattern | Hardcoded pattern (e.g. glider, blinker) or randomized initial grid |
| 7 | Optional controls | Pause / single-step / quit keys, adjustable speed, toroidal wrapping |

## Console UI Sketch

```
+-- Conway's Game of Life -- Generation: 42 --+
|                                              |
|   . . . . . . . . . . . . . . . . . . . .    |
|   . . . # # . . . . . . . . . . . . . . .    |
|   . . # . # . . . . . . . . . . . . . . .    |
|   . . . # # . . . . . . . . . . . . . . .    |
|   . . . . . . . . . . . . . . . . . . . .    |
|                                              |
+----------------------------------------------+
  [space]=pause  [s]=step  [q]=quit
```

## Implementation

* Java 21
* Maven
* JUnit 5
* e.g. framework for console UI

MUST FOLLOW `naming` skill convention for all names.

DO NOT STOP UNTIL COMPLETE.
