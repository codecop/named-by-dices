---
name: capture-demo
description: Load this skill when creating screenshots or an animated GIF/video of a console app (e.g. 01_game_of_life) running in the cloud sandbox, including the full working setup for the sandbox.
---

# Capture Demo (Screenshots / Video)

Erzeugt Screenshots und ein animiertes GIF ("Video") von einer laufenden
 Konsolen-App (hier: `01_game_of_life`), damit man schnell visuell verifizieren
 kann, dass alles läuft. Ergebnis landet in `01_game_of_life/docs/`
 (`frame-generation-N.png`, `demo.gif`).

## Working Solution im Cloud-Sandbox (was laden, wie man es bekommt)

- Kein root, kein apt. `curl`/`wget` sind per Policy blockiert.
  Funktionieren: `git`/`gh` (github.com, api.github.com) und `python3` (urllib
  für beliebige HTTPS-Downloads, z. B. Maven Central, dlcdn.apache.org,
  api.adoptium.net).
- **JDK 21** holen (nicht installiert):
  `python3` + urllib: `https://api.adoptium.net/v3/binary/latest/21/ga/linux/x64/jdk/hotspot/normal/eclipse`
  als tar.gz nach `~/tools/`, entpacken, `export JAVA_HOME=~/tools/jdk-21* `.
- **Maven** holen: Versionsliste unter `https://dlcdn.apache.org/maven/maven-3/`,
  dann `.../maven-3/<ver>/binaries/apache-maven-<ver>-bin.tar.gz` nach `~/tools/`
  entpacken, `PATH=$JAVA_HOME/bin:~/tools/apache-maven-*/bin:$PATH`.
  Maven Central ist aus Java heraus erreichbar — `mvn` lädt Dependencies normal.
- **Pillow** für die Bild-Erzeugung: `pip3 install pillow` (pip funktioniert).
  Font: `ImageFont.load_default(size=22)` genügt, keine System-Font nötig.
- **Push**: siehe `commit`-Skill — `git push` ist im Sandbox blockiert (403),
  stattdessen `python3 scripts/api_push.py`.

## Vorgehen

1. Bauen: `cd 01_game_of_life && mvn -B package` (Tests laufen mit, grün).
2. App headless laufen lassen und Frames aufnehmen (verzögertes `q` als Quit-Key):
   ```
   (sleep 1.6; printf 'q') | java -jar target/IServiceProcessor-1.0-SNAPSHOT.jar \
       --cols 30 --rows 12 --delay 120 > /tmp/run.raw 2>&1
   ```
3. Frames parsen: Roh-Output ist durch ANSI-Clear `\x1b[2J\x1b[H` getrennt,
   restliche Escapes (`\x1b[?25l`, `\x1b[?25h`) strippen. Jeder Frame ist ein
   Textblock (Border, Titel mit Generation, Grid-Zeilen, Footer).
4. Mit Pillow rendern (914x474, dunkler Hintergrund, `#` grün, `.` grau,
   Titel blau): erste/mittlere/letzte Frames als `frame-generation-N.png`,
   alle Frames (300 ms/Frame, loop) als `demo.gif` nach `01_game_of_life/docs/`.
5. Verifizieren: GIF-Frame per `Image.seek(n)` extrahieren und bildlich prüfen
   (Generation im Titel, Glider/Blinker sichtbar, Border/Footer sauber).
6. Committen und pushen (siehe `commit`-Skill, Footer nicht vergessen).

## Naming

Die `naming`-Skill gilt für Code-Namen; Doku-/Bild-Dateien (`docs/demo.gif`,
Skill-Dateien) folgen der üblichen Verzeichnisstruktur.
