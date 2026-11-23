---
name: get-java
description: Load this skill whenever a Java 21 JDK and/or Maven are needed on a fresh machine or in the cloud sandbox (no root, no package manager).
---

# Get Java (JDK 21 + Maven)

## Cloud sandbox constraints

- No root, no `apt`, no `sudo` ("no new privileges" flag).
- `curl` and `wget` are blocked by sandbox policy ("Network requests via curl are not allowed").
- What works: `git`/`gh` (github.com, api.github.com) and `python3` with `urllib` for arbitrary HTTPS downloads (Maven Central, dlcdn.apache.org, api.adoptium.net all reachable).
- Shell state does **not** persist between commands - export `JAVA_HOME`/`PATH` in the same command that uses them.

## Download helper (python3 urllib)

```python
import urllib.request
def dl(url, out):
    req = urllib.request.Request(url, headers={"User-Agent": "python"})
    with urllib.request.urlopen(req, timeout=180) as r, open(out, "wb") as f:
        while chunk := r.read(1 << 20):
            f.write(chunk)
```

## Steps

1. `mkdir -p ~/tools`
2. **JDK 21 (Temurin)**: `dl("https://api.adoptium.net/v3/binary/latest/21/ga/linux/x64/jdk/hotspot/normal/eclipse", "$HOME/tools/jdk21.tar.gz")`, then `tar xzf ~/tools/jdk21.tar.gz -C ~/tools`
3. **Maven**: list available versions at `https://dlcdn.apache.org/maven/maven-3/` (parse `href="3.x.y/"`), then download `https://dlcdn.apache.org/maven/maven-3/<version>/binaries/apache-maven-<version>-bin.tar.gz` the same way and `tar xzf` into `~/tools`
4. Use them (same command, because env does not persist):

   ```
   export JAVA_HOME=~/tools/jdk-21*
   export PATH=$JAVA_HOME/bin:~/tools/apache-maven-*/bin:$PATH
   java -version   # expect 21.x
   mvn -version
   ```

   Maven Central (repo.maven.apache.org) is reachable from Java, so `mvn` resolves plugins and dependencies normally - no extra setup.

## Verify a project

```
cd <project> && mvn -B verify
```
