# Dice-Constraint: Violations (ohne `main`)

Selbst deklarierte Identifier im Java-Projekt, die nicht aus Dice-Namen (`bin\dices.exe`) bestehen.
Testmethodennamen sind laut Naming-Skill ausgenommen. `main` (Java-Einstiegspunkt) ist ebenfalls ausgenommen.

## src\main\java\service

| Datei | Identifier |
| ------- | ----------- |
| `BuilderIImpl.java` | `grid`, `cell`, `offsets`, `x`, `y`, `j` |
| `DefaultObjectHelper.java` | `key`, `e` (Catch-Variable) |
| `ExecutorIFactory.java` | `border`, `row`, `text`, `width`, `grid`, `x`, `y` |

## src\test\java\service

| Datei | Identifier |
| ------- | ----------- |
| `BuilderIImplTest.java` | `grid`, `first`, `second`, `alive` |
| `BusinessImplDefaultTest.java` | `grid`, `rows`, `expected`, `next`, `back`, `before`, `current`, `vertical`, `cell`, `xy` |
| `ExecutorIFactoryTest.java` | `renderer`, `grid`, `frame`, `lines` |
