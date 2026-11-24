---
name: review-dices
description: > Load this skill when reviewing code against the Dice Namer constraint. It checks that every identifier (variables, parameters, fields, methods, classes, files, folders) is a random name produced by bin\dices.exe - except test class names, test method names, and test local names, which keep descriptive names. Structural folders (`src`, `src/test`, `docs`), build scripts (`Makefile`) and build test helpers (e.g. `smoke_pty.py`) are exempt too. Use it for code reviews, or when asked whether identifiers satisfy the dice constraint.
---

# Dice Code Review

Review code so that it satisfies the *Dice Namer* constraint from the `naming` skill.

## Constraint

- Every identifier (variable, parameter, field, method, class, file) must be a name listed in the dice vocabulary.
- **Exception:** test class names, test method names, and test locals keep their descriptive names. Also exempt per the `naming` skill: structural folders (`src`, `src/test`, `docs`), build scripts (e.g. `Makefile`) and build test helpers (e.g. `smoke_pty.py`).

## Review activities

1. **Use the dice vocabulary from the `naming` skill.** The `naming` skill defines the name source (`bin\dices.exe`) and its base vocabulary - do not re-roll to collect it; validate identifiers against the names and base words defined there.
2. **Extract identifiers.** For each source file, strip comments and string/char literals, then extract all identifiers. Remove language keywords and JDK/library symbols (e.g. `System.out.println`, `Math.floorMod`, package names like `java.util`, `org.junit`) - those are not renameable and do not count as violations.
3. **Classify test code.** Exempt test class names, test method names (e.g. methods annotated `@Test` with descriptive names), and test locals. All other identifiers in test files (helper methods) must follow the dice constraint.
4. **Check each identifier.** An identifier is compliant if it is a dice name itself or composed entirely of dice base words (camelCase/PascalCase combination). Entry points fixed by the language (e.g. Java `main`) are exempt.
5. **Report violations.** List every non-compliant self-declared identifier grouped by file in a table: file - identifiers. Do not list exempt categories (test class names, test method names, test locals, `main`, JDK/library symbols, structural folders, build scripts, build test helpers).
