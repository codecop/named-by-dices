# Test plan: 03_roguelike (player perspective)

Manual play-test plan for the roguelike, written from the player's point of view. Every
scenario is played through the real game binary, not the unit tests: the game is started via
`./run.sh` (or `python3 -m src.main`) and driven through the stdin UI seam (`--ui stdin`, one
command per line), except T41 which uses the real terminal UI (`--ui tty`) under a pty. Fixed
seeds make the runs reproducible.

The scenario list is based on web research about what players typically and untypically do in
roguelikes: bump-attacking by walking into monsters, kicking walls for secret passages, exploring
every room (fog of war), picking up everything, hoarding and then trial-and-error using potions
and scrolls near the stairs, wielding the shiniest weapon, descending immediately, stair
dancing / level scumming, save-scumming (save often, reload on death), quitting without saving,
restarting right after permadeath, pressing random keys, and dying to the boss underlevelled
(sources: Reddit r/roguelikes "noob mistakes" and "what am I doing wrong" threads, RogueBasin
pages on cheating/save-scumming/level scumming/stair dancing, the original Rogue manual, the
Wikipedia roguelike article).

Legend: `[x]` executed and passed, `[ ]` open. Each executed scenario has a result note.

How to reproduce a scenario by hand, e.g. T01:

```
printf 'Q\n' | ./run.sh --ui stdin --seed 5
```

## 1. Starting the game and the command line

- [ ] **T01** New game renders and quits cleanly. Steps: start `--ui stdin --seed 5`, read the first frame, send `Q`. Expected: frame shows `@`, the status line (`HP ... Depth 1/5 ...`) and a welcome/story message; exit code 0.
- [ ] **T02** Seeds are reproducible. Steps: start `--seed 7` twice and `--seed 8` once, compare the first map frame. Expected: seed 7 runs are identical, seed 8 differs (procedural generation).
- [ ] **T03** Custom game data via `--data`. Steps: start with a config whose `max_depth` is 1. Expected: status line shows `Depth 1/1`.
- [ ] **T04** Missing game data file. Steps: start with `--data /tmp/does-not-exist.txt`. Expected: the game reports the error and exits non-zero (no silent start).
- [ ] **T05** UI auto-detection. Steps: pipe commands into `./run.sh` without `--ui`. Expected: the stdin UI is used automatically (frame rendered, `quit` exits 0).

## 2. Movement and keyboard quirks

- [ ] **T06** All eight movement keys work (`h j k l y u b n`). Steps: on open floor send each key and compare `@` positions. Expected: each key moves `@` one cell in its direction.
- [ ] **T07** Bumping into a wall. Steps: walk towards a visible `#` and bump. Expected: message `A wall.`, position unchanged.
- [ ] **T08** Unknown key. Steps: send `x`. Expected: message `Unknown key 'x'`, game continues.
- [ ] **T09** Empty input line. Steps: send an empty line. Expected: the game quits (same as EOF) with exit code 0. Quirk, documented.
- [ ] **T10** EOF on stdin. Steps: close stdin without any command. Expected: game exits 0.
- [ ] **T11** Uppercase and word commands. Steps: send `H` (moves left), then the word `QUIT`. Expected: `H` moves like `h`; `QUIT` quits like `Q`.
- [ ] **T12** Long and non-ASCII input. Steps: send `hhhh` and `ä`. Expected: `hhhh` counts as one `h` move; `ä` gives `Unknown key 'ä'`; no crash.
- [ ] **T13** Word commands from the stdin UI. Steps: send `help`, `rest`, `down` (while not on stairs). Expected: `help` shows the key help, `rest` passes a turn, `down` off stairs gives `No stairs down here.`

## 3. Combat and monsters

- [ ] **T14** Bump-attack a monster until it dies. Steps: find a visible monster, walk adjacent, bump repeatedly. Expected: `You hit the ...` / `You miss the ...` messages, finally `You kill the ...! +N xp.` and `XP` in the status line increases.
- [ ] **T15** The monster hits back. Steps: same fight. Expected: `The ... hits you for N.` and `HP` in the status line drops.
- [ ] **T16** Monsters chase when visible. Steps: see a monster, then rest (`.`) several turns. Expected: the monster's distance to `@` shrinks.
- [ ] **T17** Levelling up. Steps: kill a monster worth 100 xp. Expected: `Level up` message, status `Lvl 2`, max HP increases.

## 4. Items

- [ ] **T18** Picking up. Steps: walk onto a visible item letter and send `,`. Expected: `You pick up ...` (or `You pick up N gold.`).
- [ ] **T19** Picking up on an empty floor. Steps: send `,` on empty floor. Expected: `Nothing here.`
- [ ] **T20** Inventory. Steps: `i` on a fresh game, then after picking something up. Expected: `Inventory is empty.`, later `Inventory: a: ...`.
- [ ] **T21** Wield a weapon. Steps: pick up `)`, then `w` + `a`. Expected: `You wield ...`, `Atk` in the status line increases.
- [ ] **T22** Wear armour. Steps: pick up `[`, then `W` + `a`. Expected: `You wear ...`, `Def` increases.
- [ ] **T23** Quaff a potion. Steps: pick up `!`, then `q` + `a`. Expected: `You quaff ... +N hp.`
- [ ] **T24** Read a scroll. Steps: pick up `?`, then `r` + `a`. Expected: scroll effect message, e.g. `The dungeon map reveals itself!`
- [ ] **T25** Zap a wand. Steps: pick up `/`, then `z` + `a` + direction. Expected: `Zap which way?`, then `Your bolt hits ...` or `The bolt fizzles into the wall.`
- [ ] **T26** Using an item with an empty inventory. Steps: fresh game, send `q`. Expected: `No potion in your inventory.`

## 5. Traps

- [ ] **T27** Stepping on a trap. Steps: find a visible `^` (dart trap config) and walk onto it. Expected: `A dart trap hits you for N.` and HP drops.

## 6. Stairs and dungeon depth

- [ ] **T28** Descending. Steps: find `>`, stand on it, send `>`. Expected: status shows `Depth 2/2` (2-deep test config), new map.
- [ ] **T29** Descending without stairs. Steps: send `>` on plain floor. Expected: `No stairs down here.`
- [ ] **T30** Ascending above the surface. Steps: on depth 1 send `<`. Expected: `No stairs up here.`
- [ ] **T31** Ascending back (stair dancing). Steps: descend to depth 2, find `<`, send `<`. Expected: `You climb up to depth 1.`, status `Depth 1/2`.

## 7. Winning and dying

- [ ] **T32** Winning the game. Steps (1-deep config): find `&`, send `,` (`You take the Golden Die!`), find `<`, send `<`. Expected: `*** YOU WIN ***` frame and win message; `Q` then exits 0.
- [ ] **T33** Dying (permadeath). Steps: 3-HP config with a dragon, bump the `D` until it hits. Expected: `You die in the dark... Game over.`, then `Q` exits 0.

## 8. Save and load

- [ ] **T34** Save and reload. Steps: play a few turns, send `s` (`Game saved.`, file exists), quit; restart with the same `--save`, answer `y` at the prompt. Expected: `Game loaded.`, same depth and `@` position as at save time.
- [ ] **T35** Declining the load. Steps: same, but answer `n`. Expected: `New game.`
- [ ] **T36** Quitting without saving. Steps: start with a fresh `--save` path, send `Q` immediately. Expected: no save file is created.
- [ ] **T37** Saving twice. Steps: send `s`, move, send `s` again. Expected: both times `Game saved.`, a single file, holding the later state.
- [ ] **T38** Corrupted save file. Steps: write garbage into the save file, start, answer `y`. Expected: recorded behaviour (must not hang; see result note).

## 9. Configuration file

- [ ] **T39** Extending the game with a new monster. Steps: config with `monster X testbeast 4 2 0 3 1`, explore until visible. Expected: `X` appears on the map.
- [ ] **T40** Malformed config line. Steps: start with a config containing an incomplete `monster` line. Expected: startup error, non-zero exit (no half-parsed game).

## 10. Terminal UI (tty)

- [ ] **T41** Real terminal UI under a pty. Steps: `--ui tty`, send an arrow key (`\x1b[C`) and `Q`. Expected: ANSI frame with hidden/restored cursor (`\x1b[?25l` / `\x1b[?25h`), arrow key moves `@`, exit code 0.
- [ ] **T42** Bumping into the friendly NPC. Steps: find `H`, walk into it. Expected: recorded behaviour (see result note).
