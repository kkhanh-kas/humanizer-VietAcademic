#!/usr/bin/env python3
"""Check Humanizer's package files without external dependencies."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = ROOT / "SKILL.md"
SKILL = SKILL_PATH.read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")
AGENTS = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
PLUGIN = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))


def require_match(match: re.Match[str] | None, message: str) -> re.Match[str]:
    if match is None:
        raise SystemExit(message)
    return match


yaml_metadata = require_match(
    re.match(r"\A---\n(.*?)\n---\n", SKILL, re.DOTALL),
    "SKILL.md must begin with YAML metadata",
).group(1)

for unsupported_field in ("compatibility:", "allowed-tools:"):
    if re.search(rf"(?m)^{re.escape(unsupported_field)}", yaml_metadata):
        raise SystemExit(f"Remove unsupported YAML field: {unsupported_field[:-1]}")

skill_version = require_match(
    re.search(r'(?m)^\s+version:\s*["\']([^"\']+)["\']\s*$', yaml_metadata),
    "Add metadata.version to SKILL.md",
).group(1)
readme_version = require_match(
    re.search(r"(?m)^- \*\*([0-9]+\.[0-9]+\.[0-9]+)\*\*", README),
    "Add a version entry to README.md",
).group(1)

package_versions = {skill_version, readme_version, str(PLUGIN.get("version", ""))}
if len(package_versions) != 1:
    raise SystemExit(
        f"Use one package version in all files: {sorted(package_versions)}"
    )

skill_files = {path.relative_to(ROOT) for path in ROOT.rglob("SKILL.md")}
if SKILL_PATH.is_symlink() or skill_files != {Path("SKILL.md")}:
    raise SystemExit("Keep one regular SKILL.md at the repo root")
if PLUGIN.get("skills") != ["./"]:
    raise SystemExit("Point the Claude plugin skill loader at the repo root")

plain_language_rules = (
    "## Writing style",
    "Lead with the main point.",
    "Use common words and active voice.",
    "Keep sentences and paragraphs short.",
    "Use `must` for requirements.",
    "Keep the full technical meaning.",
)
missing_plain_language_rules = [
    rule for rule in plain_language_rules if rule not in AGENTS
]
if missing_plain_language_rules:
    raise SystemExit(
        "Add the missing Plain Language rules to AGENTS.md: "
        + ", ".join(missing_plain_language_rules)
    )

pattern_numbers = [
    int(number)
    for number in re.findall(r"(?m)^### ([0-9]+)\. ", SKILL)
]
if pattern_numbers != list(range(1, 36)):
    raise SystemExit(f"Number SKILL.md patterns from 1 through 35: {pattern_numbers}")

def group_patterns(text: str, heading: str, row: str) -> dict[str, list[int]]:
    """Map each section heading to the pattern numbers listed under it."""
    groups: dict[str, list[int]] = {}
    current: str | None = None
    for line in text.splitlines():
        found_heading = re.match(heading, line)
        if found_heading:
            current = found_heading.group(1).strip()
            groups.setdefault(current, [])
            continue
        found_row = re.match(row, line)
        if found_row and current is not None:
            groups[current].append(int(found_row.group(1)))
    return {name: numbers for name, numbers in groups.items() if numbers}


skill_groups = group_patterns(SKILL, r"^## (.+)$", r"^### ([0-9]+)\. ")
readme_groups = group_patterns(README, r"^### (.+)$", r"^\| ([0-9]+) \|")
# Compare the groupings, not the heading text, so the README can be written in
# any language while SKILL.md stays in English.
if list(readme_groups.values()) != list(skill_groups.values()):
    raise SystemExit(
        "Split the README pattern tables into the same groups, in the same order, "
        "as the sections of SKILL.md. "
        f"SKILL.md has {list(skill_groups.values())} "
        f"but README.md has {list(readme_groups.values())}"
    )

readme_numbers = {number for numbers in readme_groups.values() for number in numbers}
if readme_numbers != set(range(1, 36)):
    raise SystemExit("List patterns 1 through 35 in the README table")

required_paths = (
    "patterns/schema.json",
    "patterns/layer1-grammar-syntax.yml",
    "patterns/layer2-rhetoric-style.yml",
    "references/false-positives.md",
    "references/registers.md",
    "references/chinese-source.md",
    "references/layer1-grammar-syntax.md",
    "benchmarks/rubric.md",
    "benchmarks/cases/academic-cases.json",
    "scripts/catalog.py",
    "scripts/kiem_tra.py",
    "scripts/test-kiem-tra.py",
    "scripts/validate-patterns.py",
    "scripts/run-benchmark.py",
)
missing_paths = [path for path in required_paths if not (ROOT / path).exists()]
if missing_paths:
    raise SystemExit("Add the missing bundled files: " + ", ".join(missing_paths))

unreferenced = [
    path for path in required_paths
    if path not in SKILL and path.rsplit("/", 1)[-1] not in README
]
if unreferenced:
    raise SystemExit(
        "Reference every bundled file from SKILL.md or README.md: " + ", ".join(unreferenced)
    )

if len(SKILL.splitlines()) > 500:
    raise SystemExit("Keep SKILL.md at 500 lines or fewer")

print(f"Humanizer package v{skill_version} is valid")
