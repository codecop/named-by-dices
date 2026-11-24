# 02 Pac-Man Requirements

Console Pac-Man in plain C (standard C99). See <https://en.wikipedia.org/wiki/Pac-Man>.

## Console UI Sketch

```
+-----------------------+
| PAC-MAN  SCORE: 0010  LIVES: 3 |
| ##################### |
| #.........#.........# |
| #o.##.###.#.###.##.o# |
| #...................# |
| ...                 ... |
| #o.#......C......#.o# |
| #.........#.........# |
| ##################### |
+-----------------------+
  [WASD] move  [Q] quit
```

* One frame per game tick, screen cleared between frames (ANSI escape codes).
* `#` wall, `.` dot, `o` power pellet, `-` ghost-house door, `C` Pac-Man,
  `M` ghost, `w` frightened ghost, blank empty path.
* HUD line shows score and remaining lives; border and help line around the maze.
* Keys: `W`/`A`/`S`/`D` steer Pac-Man, `Q` quits. Ctrl+C also quits (terminal restored).

## Components to build

| # | Component | Description |
| --- | --------- | ----------- |
| 1 | Maze board | Fixed 21x15 ASCII map; cell access; passable checks for Pac-Man (no walls, no door) and ghosts (no walls, door ok); dot/pellet counting; reset to pristine map; Pac-Man and ghost start positions scanned from the map |
| 2 | Actor | Direction enum (up/left/down/right/none), position struct, movement delta, opposite direction, Pac-Man struct (position, direction, wished direction) |
| 3 | Ghost | Ghost struct (position, home, direction, mode chase/frightened, frightened ticks); greedy AI picking the passable, non-reversing direction with minimal Manhattan distance to the target; frightened ghosts pick a random direction via an injected RNG function pointer |
| 4 | Game rules | Game state (board, Pac-Man, ghosts, score, lives, dots left, tick, status running/won/lost); `step` applies one tick: steer and move Pac-Man, eat dot (+10) / pellet (+50, frightens ghosts), move ghosts every 2nd tick, resolve collisions (frightened ghost eaten +200 and respawns at home; otherwise lose a life and reset actors, lives 0 = lost), all dots eaten = won |
| 5 | Renderer | Pure function from game state to an ASCII frame string (border, HUD, maze with entities, help line); frame size query for buffer allocation |
| 6 | Console UI loop | Game loop driven through an injected IO vtable (read key / write frame / sleep ms / clear screen) so it is fully unit-testable with mocks; maps `WASD` keys to directions, `Q` quits |
| 7 | Entry point | `main` wiring the real board, game, terminal (termios raw mode, non-blocking `poll` input, fallback to plain stdin when not a TTY) and a real RNG |

## Rules

* Pac-Man moves one cell per tick; wished direction is applied when passable, otherwise the current direction continues.
* Dot = 10 points, power pellet = 50 points and frightens all ghosts for a fixed number of ticks, eaten ghost = 200 points.
* Ghosts move every 2nd tick, chase Pac-Man greedily, never reverse unless in a dead end; frightened ghosts move randomly.
* Touching a chasing ghost costs one life (start with 3) and resets actor positions; 0 lives = game over; all dots eaten = you win.

## Implementation

* Plain C, standard C99 (`-std=c99 -Wall -Wextra -Werror -pedantic`), built with a `Makefile` (POSIX) or `CMakeLists.txt` (Windows/MinGW); the console layer has a `_WIN32` branch (`conio.h`/`SetConsoleMode`) and a POSIX branch (termios/poll).
* Unit tests with [cmocka](https://cmocka.org) ("c-mokka"), kept with the code in `src/test/`; test method names are descriptive (`<state>_<act>_<expected>`).
* Full code coverage; coverage documents are kept in the task-local `docs` folder.
* MUST FOLLOW `naming` skill convention for all names.
* DO NOT STOP UNTIL COMPLETE.
