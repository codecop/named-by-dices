---
name: capture-demo
description: Load this skill when creating screenshots or an animated GIF/video of a console app (e.g. 01_game_of_life) running in the cloud sandbox.
---

# Capture Demo (Screenshots / Video)

Creates screenshots and an animated GIF ("video") of a running console app (here: `01_game_of_life`) so you can quickly verify visually that everything works. Output goes to `01_game_of_life/docs/` (`frame-generation-N.png`, `demo.gif`).

## Cloud sandbox prerequisites (short form)

The toolchain setup is generic cloud-instance setup, not demo-specific. In short: no root, `curl`/`wget` blocked; `git`/`gh`/`python3` work. Fetch JDK 21 (Adoptium tarball) and Maven (`dlcdn.apache.org`) with python3 urllib into `~/tools/` and put them on `PATH`; `pip3 install pillow` for rendering (`ImageFont.load_default(size=22)` needs no system font); push via `scripts/api_push.py` (see the `commit` skill), because `git push` is blocked (403).

## Procedure

1. Build: `cd 01_game_of_life && mvn -B package` (tests run along, must be green).
2. Run the app headless and capture frames (delayed `q` as quit key):
   ```
   (sleep 1.6; printf 'q') | java -jar target/IServiceProcessor-1.0-SNAPSHOT.jar \
       --cols 30 --rows 12 --delay 120 > /tmp/run.raw 2>&1
   ```
3. Parse frames: the raw output is separated by ANSI clear `\x1b[2J\x1b[H`; strip remaining escapes (`\x1b[?25l`, `\x1b[?25h`). Each frame is a text block (border, title with generation, grid rows, footer).
4. Render with Pillow (914x474, dark background, `#` green, `.` gray, title blue): first/middle/last frames as `frame-generation-N.png`, all frames (300 ms/frame, loop) as `demo.gif` into `01_game_of_life/docs/`.
5. Verify: extract a GIF frame via `Image.seek(n)` and inspect it visually (generation in the title, glider/blinker visible, border/footer aligned).
6. Commit and push (see the `commit` skill, do not forget the footer).

## Naming

The `naming` skill applies to code names; doc/image files (`docs/demo.gif`, skill files) follow the usual directory structure.
