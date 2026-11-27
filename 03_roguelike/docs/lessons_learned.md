# Lessons learned: 03_roguelike session

Analysis of the full session: building the roguelike, the manual play-test plan
([test_plan.md](test_plan.md)) and the demo capture. What went wrong, what was corrected, and how
to prevent it. British English, per repo convention.

## 1. Errors during the build (own mistakes, tooling)

- **Silent zero-test run**: test methods lacked the `test_` prefix, so unittest reported "OK"
  with 0 tests. Caught only later.
- **Dice-naming violations found late**: plain-English identifiers (`game`, `player`, `config`,
  `handle`, `play`) in later modules, discovered by the `review-dices` AST scan instead of
  incrementally.
- **`search_replace` with a stale anchor** on `ci-build-action/SKILL.md` failed (`old_str not
  found`) because the file had not been re-read first.
- **`pkill -f "src.main"` matched the own shell** (pattern appears in the own command line) and
  killed it — twice.
- **Force-push after rebase rejected** with `stale info`: no local remote-tracking ref existed,
  so `--force-with-lease` had nothing to compare against. Fixed with an explicit lease value
  (`--force-with-lease=<branch>:<sha>`).
- **Test-runner bugs**: quitting via `Q` in the stdin UI (lowercased to `q` = quaff, so processes
  never exited and were SIGKILLed); the runner deleted the save file before load scenarios; BFS
  treated traps as walls (rooms behind traps unreachable); determinism check stripped ANSI before
  splitting frames; message-text assertions were flaky because the message line shows only the
  last event of a turn.
- **Background game process killed by tool timeouts** (same process group) — restarted with
  `setsid`.
- **Fully automated 42-scenario runner hit the 570 s timeout** (long frame timeouts per turn).
  Exploratory parts are now played live, scripted checks stay short.

## 2. Game-logic errors found by the manual test plan

All fixed with regression tests (100% coverage kept):

- **Artefact spawned on shallow levels**: the random item pool included `artefact`, so the Golden
  Die appeared on depths 1, 2, ... (seen live on depth 1). Fixed: artefact excluded from the random
  pool, placed only on the deepest level. Property test added: no artefact above max depth.
- **Startup crashes for minimal configs**: `IndexError` when no monsters are configured
  (`builder.choice` on empty list), `KeyError: 'artefact'` on the deepest level without an
  artefact line, `IndexError` when no items are configured. Fixed: guards in `processor_utils.py`
  and `impl_object.py`; edge-case config tests added.
- **Win/death screen never rendered**: the game loop exited before the final frame, so
  `*** YOU WIN ***` / `Game over` were never shown (and the overlay text "press Q to quit" was
  wrong). Fixed: final frame is rendered after the loop; overlay text adjusted; loop tests added.
- **stdin UI could not send uppercase commands**: a single `W` is lowercased to `w` (wield), so
  "wear armour" was unreachable from the test UI. Fixed: word commands `wield`, `wear`, `quaff`,
  `read`, `zap` added to the stdin word map.
- **Recorded rough edges (not fixed, see open points)**: missing `--data` file and corrupted save
  file exit 1 with a Python traceback instead of a friendly error (scenarios T04/T38).

## 3. Design corrections requested by the user

- No Makefile: `run.sh` with one line for tests, one for the game (later split into `test.sh` +
  `run.sh`, both used by the CI action).
- No loosened linter limits: decomposed into more classes instead.
- No docstrings: removed everywhere; docstring rules disabled in `.pylintrc`.
- Tests in a top-level `test/` folder next to `src/`.
- Game data configurable via `game.txt` (extension of requirements.md).
- Coverage removed from the CI action (local only, report committed to `docs/`); noted in the
  `ci-build-action` skill.
- Branch rebased on `main`; updated `commit` skill adopted (single-line messages + footer).

## 4. Inconsistencies / user-side points

- "One script with two lines" was later changed to "two scripts, not everything in one" — both
  variants were implemented in sequence.
- requirements.md said "full coverage with docs in docs/"; I initially wired coverage into CI,
  the user wanted it local-only. Clarified afterwards.
- User instruction "rebase on main" conflicts with the updated `commit` skill ("NEVER rebase, work
  on main, no PRs"). Resolved in favour of the user (branch/PR workflow); noted as a conflict to
  be aware of.
- Video request was vague ("per capture-demo skill or similar") and later clarified as
  "video demo in docs committed"; the GIF format from the skill was chosen.
- Typos in user messages ("welcje", "pr") were interpreted by meaning; no impact.

## 5. Prevention measures (obvious, adopted)

- **Fail on zero tests**: `test.sh` / CI must fail if the unittest summary says `Ran 0 tests`
  (guards the `test_` prefix class of bug).
- **Naming scan after every increment**, not only at the end: run the `review-dices` AST check
  whenever new identifiers are added (optionally as a CI step).
- **Always re-read a file before editing it** (avoids stale-anchor `search_replace` failures).
- **Never `pkill -f` with a literal pattern that appears in the own command line** — build the
  pattern at runtime or kill by PID from `pgrep`.
- **Push rewritten history only with an explicit lease** `--force-with-lease=<branch>:<expected-sha>`.
- **Runner checklist for UI-driven tests**: quit via the `quit` word in the stdin UI; never
  delete the save file in load scenarios; treat traps as walkable; assert on status/inventory,
  not only on message text; split raw bytes on the frame delimiter before stripping ANSI.
- **Background processes across tool calls need `setsid`**.
- **Cap automated runs** (frame timeouts, turn limits); play exploratory scenarios live.
- **Property/edge tests for generation**: artefact only on the deepest level; configs without
  monsters/items/artefact/traps must start; game-over renders the final frame.
- **UI parity**: every tty-only command must be reachable from the stdin UI via a word.

## 6. Open points (discussed separately, not yet decided)

- Friendly one-line errors for a missing `--data` file and a corrupted save file (T04/T38
  currently exit 1 with a traceback).
- Message line shows only the last event of a turn; consider a small message log.
- `Q` quits in the tty UI but quaffs (`q`) in the stdin UI; `quit`/EOF/empty line quit there.
- Naming AST scan as a CI gate (needs a small script in the repo).
- "Ran 0 tests" guard inside `test.sh` (CI-only vs. script).
- Process rule for conflicts between a skill file and a direct user instruction.

## 7. Up-front process rules (per error, discussed one by one)

Rule of thumb: the prevention belongs into the scaffolding (run.sh, CI, conventions) *before the
first commit*, so the error class can never occur silently.

- **A1 silent zero-test run** -> from day one, a test run is only green if it ran tests:
  `test.sh`/CI fails on `Ran 0 tests`; the convention "test methods start with `test_`" is enforced
  by that guard.
