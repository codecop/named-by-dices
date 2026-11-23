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
