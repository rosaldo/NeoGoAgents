---
name: mudanca-minima
description: Deliver the smallest complete change that solves the whole task, then review it in plain language.
metadata: { agent: minimal-change-engineer }
---

# Mudanca minima

The smallest change that **fully** solves the task. Lazy about the solution, never about the work.

## Before editing

Read the task and the code it touches. List every place the change must reach: callers, tests, fixtures, config, exports. Check what it could break for users: data destroyed or exposed, callers that stop working. That is the scope; extra features are not.

## The ladder

Take the first rung that fully works:

1. Does it need to exist? Skip features, options and flexibility nobody asked for; name them in one line.
2. Already in this codebase? Reuse the existing helper or pattern the way neighbours do.
3. Standard library or platform feature? Use it unless the house has its own component.
4. Installed dependency? Use it. Never add a dependency for a few lines.
5. One line a reader understands at a glance? One line.
6. Otherwise: the minimum code that works.

No abstraction with one implementation, no speculative config, no boilerplate "for later". Deletion beats addition. Keep values in the form the platform already returns. Comment only the *why* code cannot show. For a bug, grep every caller, then fix the root cause once in shared code. Code that moves keeps its error handling and validation.

## Never cut

Validation at trust boundaries, error handling that prevents data loss, security, accessibility, hardware calibration, or anything explicitly requested. Between equally small options, take the one correct on edge cases. Non-trivial new logic (a branch, a parser, money, security, data writes) leaves one small test or assert-based self-check. A known shortcut gets `shortcut: <limit>, <when to upgrade>` in a comment.

## Review order

Correct, safe, holds under real load, tested, fast, lean. Every finding needs a concrete input → wrong result case; no case, no finding. Read the connected code, not only the diff, and state the load you assumed.

End with one or two lines: what you skipped or did not check, and any risk the user must know.

## Provenance

- `ponytail` — `DietrichGebert/ponytail` · Licence: MIT — Copyright (c) 2026 DietrichGebert · ADOTAR — ponytail and ponytail-review techniques distilled.
  - Third-party gate: CAUTION — hooks, plugins and settings-file writers excluded; only minimal-change and review rules distilled.

Technique distilled from documentation and skill instructions; no upstream scripts, binaries, model files or verbatim SKILL.md bodies are vendored here. Attribution above is the record of origin.
