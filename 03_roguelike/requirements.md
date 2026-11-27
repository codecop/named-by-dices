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

```
+----------------------------------------------------------------------------+
| HP 22/23  Lvl 1  XP 0  Str 9 Dex 12 Con 11  Fight 1 Dodge 0 Magic 2  Gold 0  |
| Depth 1/5  Atk 4 Def 4                                                     |
| ########################################################################## |
| #........#..............................#.......#.....................# |
| #........+..............................+.......+.....................# |
| #.@......#......r.......................#.......#.......$.............# |
| #........#..............................#.......#.....................# |
| ########################################################################## |
| The hermit heals you completely!                                           |
+----------------------------------------------------------------------------+
  [hjkl] move  [.] rest  [>] [<] stairs  [,] pick up  [i] inventory  [q] quaff
  [r] read  [z] zap  [w] wield  [W] wear  [s] save  [Q] quit  [?] help
```

* One frame per key press, screen cleared between frames (ANSI escape codes, cursor hidden).
* `#` wall, `.` floor, `+` door, `>`/`<` stairs, `^` found trap, `@` player, letters monsters/NPCs, item letters per kind (`)` weapon, `[` armour, `!` potion, `?` scroll, `/` wand, `$` gold, `&` artefact).
* Status line shows hp, level, xp, attributes, skills, gold, depth and attack/defence bonuses; bottom line shows the last message. Explored but not visible cells are dimmed (fog of war, radius from config).

## Components to build

| # | Component | Description |
| --- | --------- | ----------- |
| 1 | Game data | Plain text file `game.txt` (see Configuration): settings, monsters, npc, items, traps; parsed with line-numbered errors |
| 2 | Dungeon | Seeded level generator: 10+ non-overlapping rooms, L-shaped corridors, doors, up/down stairs, hidden traps; different each game depending on the seed; entity layer (monsters, items, traps, explored cells) |
| 3 | Actor | Position helpers, actor base (letter, name, pos, hp), player with attributes, skills, inventory and xp/levels, monsters from config, friendly helper NPC |
| 4 | Items | Weapons, armour, potions, scrolls (magic mapping, teleportation, fireball), wands of magic missile with charges, gold, the artefact |
| 5 | Game rules | Turn-based game loop through an injected IO bundle (read key / write frame / save) so it is fully unit-testable: move, bump-to-attack combat with hit chance and damage, monster AI (chase when visible, wander otherwise), traps (dart, teleport, alarm), pick up, wield/wear/quaff/read/zap, descend/ascend, save/load, win (artefact + exit) and death |
| 6 | Renderer | Pure function from game state to an ANSI frame (status line, coloured map with fog of war, message line) |
| 7 | Console input | `getch` on Windows via `msvcrt`, on POSIX via `termios`/`tty`, arrow-key escape sequences, piped-stdin fallback when not a TTY |
| 8 | Entry point | `main` wiring config, save file menu (new/load), real terminal and the game loop |

## Configuration

* All game data lives in a plain text file, `game.txt` by default (`--data FILE` overrides it); one entry per line, `#` starts a comment:
  * `setting <key> <value>` for `width`, `height`, `max_depth`, `fov_radius`, `min_rooms`, `max_rooms`, `start_hp`
  * `monster <letter> <name> <hp> <attack> <defence> <xp> <min depth>`
  * `npc <letter> <name> <hp>` friendly helper, heals once per visit
  * `item <kind> <letter> <name> <power>` kinds: `weapon`, `armour`, `potion`, `scroll`, `wand`, `gold`, `artefact`
  * `trap <kind>`
* Add one line to extend the game with a new enemy, item or trap; the single `artefact` item is the win condition.

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
* thin IO seam between UI and logic: the game is driven through an injected port (read command / write frame / save game); besides the ANSI terminal UI there is a line-based stdin test UI (`--ui stdin`, one command per line: `h`, `down`, `get`, `save`, `quit`)
* github ci action

MUST FOLLOW `naming` skill convention for all names.

DO NOT STOP UNTIL COMPLETE.
