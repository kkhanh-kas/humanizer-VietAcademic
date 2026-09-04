# Guide for agents

This file explains how to change Humanizer without breaking its package or prompt.

## What this repo contains

Humanizer is an agent skill written in Markdown. `SKILL.md` is the prompt that agents read. The repo has no build step.

Keep the skill portable. Do not write instructions that limit it to one or two agent tools.

## Key files

- `SKILL.md` is the repo's only skill file and the prompt agents read. It contains portable YAML metadata, 37 numbered patterns, their examples, and pointers to the bundled files below.
- `README.md` explains installation, use, patterns, and version history.
- `patterns/*.yml` is the machine-readable rule catalog. Each rule carries an ID, a severity, the registers it applies to, and its signal regex or phrase list.
- `patterns/schema.json` defines the shape and the allowed enum values for those rules.
- `references/*.md` holds the long-form guidance an agent reads only when a case calls for it.
- `benchmarks/` holds the evaluation rubric and the standard cases.
- `.claude-plugin/plugin.json` describes the Claude plugin and points its skill loader at the root `SKILL.md`.
- `.claude-plugin/marketplace.json` lets users add this repo as a Claude marketplace.
- `scripts/catalog.py` is the only reader of the YAML catalog. Every other script gets its rules from it.
- `scripts/kiem_tra.py` is the mechanical linter, `scripts/test-kiem-tra.py` its regression tests.
- `scripts/validate-package.py`, `scripts/validate-patterns.py`, and `scripts/run-benchmark.py` are the three checks that run in CI.

## Rules for changes

Keep `SKILL.md` and `README.md` in sync.

- **Patterns:** The skill has 37 numbered patterns. If you add, remove, or renumber a pattern, update the README table, heading, validator, and every pattern reference. Keep each pattern in the same section in both files, because the validator compares the groupings.
- **One source per rule:** Define a signal regex or phrase list once, in `patterns/*.yml`. Do not copy it into a script. `scripts/kiem_tra.py` maps its own error codes to pattern IDs and reads the signals from the catalog.
- **Registers:** The `che_do` field decides which registers a rule applies to, and the linter skips a rule outside them. Update `references/registers.md` when you change that field.
- **False positives:** A rule that fires on valid academic Vietnamese is a defect. Add the counter-example to `scripts/test-kiem-tra.py` before you narrow the rule.
- **Version:** Keep the same version in `SKILL.md` under `metadata.version`, the first README version entry, and `.claude-plugin/plugin.json`. Do not add a top-level `version` field to the skill.
- **Compatibility:** Keep install and use instructions neutral across agents. Names such as Claude Code, OpenCode, and Codex are examples, not limits.
- **History:** Add a short README version note for any behavior change or non-obvious fix.
- **Checks:** Before publishing, run `python3 scripts/validate-package.py`, `python3 scripts/validate-patterns.py`, `python3 scripts/test-kiem-tra.py`, `python3 scripts/run-benchmark.py`, `npx skills add . --list`, and `claude plugin validate .`.

## Writing style

Use Plain Language in code comments, prompts, documentation, descriptions, validation messages, and progress reports.

- Lead with the main point.
- Use common words and active voice.
- Keep sentences and paragraphs short.
- Use one term for the same item.
- Use `must` for requirements.
- Use headings, lists, and tables when they help the reader.
- Remove repeated or unnecessary words.
- Limit acronyms and explain technical terms.
- Avoid double negatives.
- Keep exact identifiers, commands, paths, schema fields, quotations, watched phrases, and behavior-bearing examples.
- Keep the full technical meaning.

## Editing the skill

- Keep the YAML metadata valid.
- Treat the prompt below the metadata as the product.
- Prefer a short, clear instruction over another exception or repeated explanation.
