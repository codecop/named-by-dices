---
name: naming
description: Load this skill whenever naming a local variable, parameter, field, method, class, module, package or folder.
---

# Naming

Follow the *Dice Namer* constraint: name everything using random dice - except test method names.

## Workflow

1. Run `bin\dices.exe` to get a random enterprise-style name (e.g. *Processor*, *Dummy*, *Factory*).
2. Use that name.
3. If the name is already used in the current context, roll the dice again.
4. Do **not** apply dice names to test method names - those keep their descriptive names.

## dices CLI

```
Usage: <repo root>/bin/dices [options] <1|2|3|variable|method|class>
```

Arguments: `1`/`variable`, `2`/`method`, `3`/`class` (shortcuts for the name type).
Will create camelCase names by default.

| Option | Description |
| ------ | ----------- |
| `-h`, `--help` | Show help message |
| `-p`, `--pascal` | Use PascalCase for all names |
| `-s`, `--snake` | Use snake_case for all names, where appropriate by language naming convention |

## Complete Vocabulary

The three dices contain the words

* "Builder", "Business", "Data", "Executor", "Object", "Processor"
* "Abstract", "Arolla", "Common", "Default", "Dummy", "I"
* "Factory", "Helper", "Impl", "Manager", "Service", "Utils"

## Clarifications (learned the hard way)

* In Java, `default` and `abstract` are keywords and cannot be used as identifiers - only the other 16 words are usable (camelCase: `builder`, `business`, `data`, `executor`, `object`, `processor`, `arolla`, `common`, `dummy`, `i`, `factory`, `helper`, `impl`, `manager`, `service`, `utils`).
* Uniqueness is required **per context only** (e.g. all method names within a class, all variables within a method) - different classes/methods may reuse the same names. There are not 30 independent variables; the pool is small, so roll again on collision within the current context and keep methods short with few locals.
* Only **test method names** are exempt from the dice constraint. Test *locals* are accepted by project decision, but all other self-declared identifiers (variables, parameters, fields, methods, classes, packages) must be dice names - `main` (the Java entry point) is also exempt.
* **Structural folders and build files are exempt** from the dice constraint: the task layout folders `src`, `src/test` and `docs` keep their conventional names, and so do build scripts and build test helpers (e.g. `Makefile`, smoke-test scripts such as `smoke_pty.py`). The constraint still applies to all code identifiers and to the names of source and test files inside `src/` (`<dice>.c` / `<dice>_test.c`).
* After coding, scan the sources for self-declared identifiers outside the vocabulary (e.g. `border`, `key`, `x`, `y`, catch variables like `e`) and rename them.
