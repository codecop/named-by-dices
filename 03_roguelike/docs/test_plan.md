# Test plan: 03_roguelike (player perspective)

Manual play-test plan for the roguelike, written from the player's point of view. Every
scenario is played through the real game binary, not the unit tests: the game is started via
`./run.sh` (or `python3 -m src.main`) and driven through the stdin UI seam (`--ui stdin`, one
command per line), except T41 which uses the real terminal UI (`--ui tty`) under a pty. Fixed
seeds make the runs reproducible. Some scenarios were played live by watching the rendered
frames (marked "live"), the rest were driven by scripted runs against the same UI.

The scenario list is based on web research about what players typically and untypically do in
roguelikes: bump-attacking by walking into monsters, kicking walls for secret passages, exploring
every room (fog of war), picking up everything, hoarding and then trial-and-error using potions
and scrolls near the stairs, wielding the shiniest weapon, descending immediately, stair
dancing / level scumming, save-scumming (save often, reload on death), quitting without saving,
restarting right after permadeath, pressing random keys, and dying to the boss underlevelled
(sources: Reddit r/roguelikes "noob mistakes" and "what am I doing wrong" threads, RogueBasin
pages on cheating/save-scumming/level scumming/stair dancing, the original Rogue manual, the
Wikipedia roguelike article).

Legend: `[x]` executed and passed. Each scenario has a result note.

How to reproduce a scenario by hand, e.g. T01:

```
printf 'quit\n' | ./run.sh --ui stdin --seed 5
```

## 1. Starting the game and the command line

- [x] **T01** New game renders and quits cleanly. Steps: start `--ui stdin --seed 5`, read the first frame, send `quit`. Result: passed (live) — frame shows `@`, status line (`HP ... Depth 1/5 ...`) and the welcome message; exit code 0.
- [x] **T02** Seeds are reproducible. Steps: start `--seed 7` twice and `--seed 8` once, compare the first frames. Result: passed — seed 7 runs identical, seed 8 differs.
- [x] **T03** Custom game data via `--data`. Steps: start with a config whose `max_depth` is 1. Result: passed — status line shows `Depth 1/1`.
- [x] **T04** Missing game data file. Steps: start with `--data /tmp/does-not-exist.txt`. Result: passed — exit 1 with `FileNotFoundError` traceback (rough edge, see notes below).
- [x] **T05** UI auto-detection. Steps: pipe commands into `./run.sh` without `--ui`. Result: passed — stdin UI used automatically, frame rendered, `quit` exits 0.

## 2. Movement and keyboard quirks

- [x] **T06** All eight movement keys work (`h j k l y u b n`). Steps: on open floor send each key and compare `@` positions. Result: passed — all 8 directions verified cell-by-cell.
- [x] **T07** Bumping into a wall. Steps: walk towards a visible `#` and bump. Result: passed (live) — message `A wall.`, position unchanged.
- [x] **T08** Unknown key. Steps: send `x`. Result: passed — `Unknown key 'x'`, game continues, exit 0.
- [x] **T09** Empty input line. Steps: send an empty line. Result: passed — the game quits (same as EOF), exit 0. Quirk, documented.
- [x] **T10** EOF on stdin. Steps: close stdin without any command. Result: passed — game exits 0.
- [x] **T11** Uppercase and word commands. Steps: send `H` (moves), then the word `QUIT`. Result: passed — `H` moves like `h`; `QUIT` quits like `Q`.
- [x] **T12** Long and non-ASCII input. Steps: send `hhhh` and `ä`. Result: passed — `hhhh` counts as one `h` move; `ä` gives `Unknown key 'ä'`; no crash.
- [x] **T13** Word commands from the stdin UI. Steps: send `help`, `rest`, `down` (while not on stairs). Result: passed — `help` shows the key help, `rest` passes a turn, `down` off stairs gives `No stairs down here.`

## 3. Combat and monsters

- [x] **T14** Bump-attack a monster until it dies. Steps: find a visible monster, walk adjacent, bump repeatedly. Result: passed (live) — kobold, goblin and rat killed; `You kill the ...! +N xp.`; `XP` in the status line rose. Note: `You hit ...` messages are overwritten by monster retaliation within the same turn (see notes).
- [x] **T15** The monster hits back. Steps: same fight. Result: passed (live) — `The goblin hits you for 5.`, HP dropped 24 to 18.
- [x] **T16** Monsters chase when visible. Steps: see a monster, then rest (`.`) several turns. Result: passed (live) — the goblin closed the distance while the player rested.
- [x] **T17** Levelling up. Steps: kill monsters until level up. Result: passed (live) — `Level up: 2!`, status `Lvl 2`, max HP 24 to 27, `Atk` 3 to 5.

## 4. Items

- [x] **T18** Picking up. Steps: walk onto a visible item letter and send `,`. Result: passed — `You pick up N gold.` and `Gold` in the status line increased.
- [x] **T19** Picking up on an empty floor. Steps: send `,` on empty floor. Result: passed — `Nothing here.`
- [x] **T20** Inventory. Steps: `i` on a fresh game, then after picking something up. Result: passed — `Inventory is empty.`, later `Inventory: dagger` (live: `Inventory: the Golden Die`).
- [x] **T21** Wield a weapon. Steps: pick up `)`, then `wield` + `a`. Result: passed — inventory shows `wielding dagger`. Note: wielding a weaker weapon than fists can lower `Atk` (by design).
- [x] **T22** Wear armour. Steps: pick up `[`, then `wear` + `a`. Result: passed — inventory shows `wearing ...`. Note: in the stdin UI a single `W` is lowercased to `w` (wield); use the word `wear` (added during this plan).
- [x] **T23** Quaff a potion. Steps: pick up `!`, then `quaff` + `a`. Result: passed — `You quaff ... +N hp.`
- [x] **T24** Read a scroll. Steps: pick up `?`, then `read` + `a`. Result: passed — `The dungeon map reveals itself!`
- [x] **T25** Zap a wand. Steps: pick up `/`, then `zap` + `a` + direction. Result: passed — `Zap which way?`, then bolt hits or fizzles.
- [x] **T26** Using an item with an empty inventory. Steps: fresh game, send `q`. Result: passed — `No potion in your inventory.`

## 5. Traps

- [x] **T27** Stepping on a trap. Steps: explore until a hidden trap triggers. Result: passed (live + scripted) — `A dart trap hits you for 4.` with HP drop; a teleport trap was hit live (`A teleport trap whisks you away!`). Found traps render as `^` and do not re-trigger.

## 6. Stairs and dungeon depth

- [x] **T28** Descending. Steps: find `>`, stand on it, send `>`. Result: passed — status shows `Depth 2/2` (2-deep test config), new map.
- [x] **T29** Descending without stairs. Steps: send `>` on plain floor. Result: passed — `No stairs down here.`
- [x] **T30** Ascending above the surface. Steps: on depth 1 send `<`. Result: passed — `No stairs up here.`
- [x] **T31** Ascending back (stair dancing). Steps: descend to depth 2, find `<`, send `<`. Result: passed — `You climb up to depth 1.`, status `Depth 1/2`.

## 7. Winning and dying

- [x] **T32** Winning the game. Steps (1-deep config): find `&`, send `,`, find `<`, send `<`. Result: passed — artefact in inventory (`the Golden Die`), final frame shows `You emerge from the caverns with the Golden Die. You win!` and `*** YOU WIN ***`; exit 0. Note: the final win frame was not rendered before — fixed during this plan.
- [x] **T33** Dying (permadeath). Steps: 3-HP config with dragons, bump the `D` until it hits. Result: passed — final frame shows `You die in the dark... Game over.`, exit 0. Note: the final death frame was not rendered before — fixed during this plan.

## 8. Save and load

- [x] **T34** Save and reload. Steps: play a turn, send `s`, quit; restart with the same `--save`, answer `y`. Result: passed — `Game saved.`, file exists, `Game loaded.`, same `@` position (70,3) and depth.
- [x] **T35** Declining the load. Steps: same, but answer `n`. Result: passed — `New game.`
- [x] **T36** Quitting without saving. Steps: fresh `--save` path, send `quit` immediately. Result: passed — no save file created.
- [x] **T37** Saving twice. Steps: `s`, move, `s` again. Result: passed — `Game saved.` twice, a single file holding the later state.
- [x] **T38** Corrupted save file. Steps: write garbage into the save file, start, answer `y`. Result: recorded — exit 1 with a `JSONDecodeError` traceback; does not hang. Rough edge (see notes).

## 9. Configuration file

- [x] **T39** Extending the game with a new monster. Steps: config with `monster X testbeast 4 2 0 3 1`, explore until visible. Result: passed — `X` appeared on the map.
- [x] **T40** Malformed config line. Steps: start with a config containing an incomplete `monster` line. Result: passed — exit 1 with a clear `line N: monster needs letter, name, hp, attack, defence, xp, min depth` error.

## 10. Terminal UI (tty)

- [x] **T41** Real terminal UI under a pty. Steps: `--ui tty`, send an arrow key (`\x1b[C`) and `Q`. Result: passed — ANSI frame with hidden/restored cursor (`\x1b[?25l` / `\x1b[?25h`), arrow key moved `@` (71,3) to (72,3), exit code 0.
- [x] **T42** Bumping into the friendly NPC. Steps: find `H`, walk into it. Result: passed — first bump gives the hint (`The hermit: 'The Golden Die lies below the dragon.'`), second bump heals (`The hermit heals you completely!`); the NPC never attacks.

## Findings

Fixed while executing this plan (each with unit tests, 100% coverage kept):

1. The Golden Die spawned as a random item on shallow levels — now only on the deepest level.
2. Startup crashed for configs without monsters, without items or without an artefact line —
   now guarded.
3. The win/death screen was never rendered (the game loop exited before the final frame) —
   the final frame is now rendered; the stdin UI also gained word commands (`wield`, `wear`,
   `quaff`, `read`, `zap`) because single uppercase letters are lowercased there.

Recorded observations (behaviour, not bugs):

- The message line shows only the last event of a turn; a player's `You hit ...` is overwritten
  by a monster's retaliation in the same frame. Kill/XP results are still visible via the status
  line and the kill message when no monster acts afterwards.
- In the stdin UI a single `Q` is lowercased to `q` (quaff); quit with the word `quit`, an empty
  line or EOF. In the tty UI `Q` quits directly.
- T04 (missing data file) and T38 (corrupted save) exit 1 with a Python traceback instead of a
  friendly one-line error.
