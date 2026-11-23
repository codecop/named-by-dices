# Dice-Constraint: Violations (ohne `main`)

Selbst deklarierte Identifier im Java-Projekt, die nicht aus Dice-Namen (`bin\dices.exe`) bestehen.
Testmethodennamen sind laut Naming-Skill ausgenommen. `main` (Java-Einstiegspunkt) ist ebenfalls ausgenommen.

## src\main\java\service

**Resolved:** all identifiers below were renamed to dice names from the vocabulary in the `naming` skill.

| Datei | Identifier |
| ------- | ----------- |
| `BuilderIImpl.java` | `grid`, `cell`, `offsets`, `x`, `y`, `j` |
| `DefaultObjectHelper.java` | `key`, `e` (Catch-Variable) |
| `ExecutorIFactory.java` | `border`, `row`, `text`, `width`, `grid`, `x`, `y` |

## src\test\java\service

**Accepted:** test method names are exempt from the dice constraint, and test locals are fine per project decision — no changes.

| Datei | Identifier |
| ------- | ----------- |
| `BuilderIImplTest.java` | `grid`, `first`, `second`, `alive` |
| `BusinessImplDefaultTest.java` | `grid`, `rows`, `expected`, `next`, `back`, `before`, `current`, `vertical`, `cell`, `xy` |
| `ExecutorIFactoryTest.java` | `renderer`, `grid`, `frame`, `lines` |
