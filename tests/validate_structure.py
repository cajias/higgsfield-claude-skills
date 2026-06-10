#!/usr/bin/env python3
r"""Deterministic structural validator for the Higgsfield Claude-skills marketplace.

Guards two things that have broken before:

1. Marketplace + plugin wiring: marketplace.json and each plugin.json parse, carry
   the expected names, and every plugin source is a local "./" path.
2. SKILL.md YAML frontmatter: the `name`/`description` block must parse as YAML.
   Several descriptions embed colons and escaped double-quotes (e.g. the cinematic
   skill's `... even if the user doesn't explicitly say \\"cinematic\\" ...`), which
   previously produced invalid YAML. This is the regression guard for that bug.

It also checks the Playwright -> MCP migration left no browser-automation residue in
the automation skills, that seedance-auto-generate points at the corrected slash
commands, and that every evals.json lines up with its sibling SKILL.md.

Stdlib only; PyYAML is used opportunistically with a regex fallback. Prints PASS/FAIL
per check and exits nonzero on any failure.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from types import ModuleType

yaml: ModuleType | None
try:
    import yaml
except ImportError:  # degrade gracefully to a regex frontmatter check
    yaml = None

ROOT = Path(__file__).resolve().parent.parent
KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PLAYWRIGHT_LEFTOVERS = re.compile(r"browser_|playwright|data-lexical-editor|hf:tour-image-prompt", re.I)
FAILURES: list[str] = []


def check(label: str, ok: bool, detail: str = "") -> bool:
    """Print a PASS/FAIL line, record failures, and return the boolean result."""
    print(f"{'PASS' if ok else 'FAIL'}: {label}" + (f" -- {detail}" if detail else ""))
    if not ok:
        FAILURES.append(label)
    return ok


def parse_frontmatter(text: str) -> dict[str, Any]:
    """Return the SKILL.md frontmatter as a dict (YAML if available, else regex)."""
    if not text.startswith("---"):
        msg = "no opening frontmatter fence"
        raise ValueError(msg)
    parts = text.split("---", 2)
    if len(parts) < 3:
        msg = "no closing frontmatter fence"
        raise ValueError(msg)
    block = parts[1]
    if yaml is not None:
        data = yaml.safe_load(block)
        if not isinstance(data, dict):
            msg = "frontmatter is not a YAML mapping"
            raise ValueError(msg)
        return data
    # Fallback: pull `name:` / `description:` off their own lines.
    out: dict[str, Any] = {}
    for key in ("name", "description"):
        m = re.search(rf"^{key}:\s*(.+?)\s*$", block, re.M)
        if m:
            out[key] = m.group(1).strip().strip('"').strip("'")
    return out


def nonempty_str(v: object) -> bool:
    """Return True when `v` is a non-blank string."""
    return isinstance(v, str) and v.strip() != ""


# --- 1. marketplace.json -----------------------------------------------------
mk_path = ROOT / ".claude-plugin" / "marketplace.json"
mk: dict[str, Any] = {}
try:
    mk = json.loads(mk_path.read_text())
    check("marketplace.json parses", True)
except Exception as e:  # noqa: BLE001
    check("marketplace.json parses", False, str(e))
check("marketplace has non-empty name", nonempty_str(mk.get("name")))
plugins = mk.get("plugins")
check("marketplace has plugins[]", isinstance(plugins, list) and len(plugins) > 0)
for i, p in enumerate(plugins or []):
    src = p.get("source", "")
    check(
        f"marketplace plugin[{i}] has name + ./ source",
        nonempty_str(p.get("name")) and isinstance(src, str) and src.startswith("./"),
        f"name={p.get('name')!r} source={src!r}",
    )

# --- 2. each plugin.json -----------------------------------------------------
for p in plugins or []:
    src = p.get("source", "")
    pj_path = ROOT / src.lstrip("./") / ".claude-plugin" / "plugin.json"
    name = "?"
    try:
        name = json.loads(pj_path.read_text()).get("name")
        ok = nonempty_str(name) and bool(KEBAB.match(name))
        check(f"{src}/plugin.json parses with kebab-case name", ok, f"name={name!r}")
    except Exception as e:  # noqa: BLE001
        check(f"{src}/plugin.json parses with kebab-case name", False, str(e))

# --- 3. every SKILL.md frontmatter parses as YAML ----------------------------
skill_files = sorted(ROOT.glob("plugins/*/skills/*/SKILL.md"))
skill_names: dict[Path, str] = {}  # skill dir -> frontmatter name
check("at least one SKILL.md found", len(skill_files) > 0, f"{len(skill_files)} files")
for sf in skill_files:
    rel = sf.relative_to(ROOT)
    try:
        fm = parse_frontmatter(sf.read_text())
        ok = nonempty_str(fm.get("name")) and nonempty_str(fm.get("description"))
        check(f"frontmatter parses w/ name+description: {rel}", ok)
        if ok:
            skill_names[sf.parent] = fm["name"]
    except Exception as e:  # noqa: BLE001
        check(f"frontmatter parses w/ name+description: {rel}", False, str(e))

# --- 4. no Playwright leftovers in automation skills -------------------------
for sf in sorted(ROOT.glob("plugins/higgsfield-automation/skills/*/SKILL.md")):
    rel = sf.relative_to(ROOT)
    hits = sorted({m.group(0) for m in PLAYWRIGHT_LEFTOVERS.finditer(sf.read_text())})
    check(f"no Playwright leftovers: {rel}", not hits, f"found {hits}" if hits else "")

# --- 5. seedance-auto-generate references corrected slash commands -----------
sa = ROOT / "plugins/higgsfield-automation/skills/seedance-auto-generate/SKILL.md"
sa_text = sa.read_text()
check("seedance-auto-generate references /seedance-cinematic", "/seedance-cinematic" in sa_text)
check("seedance-auto-generate has no stale /01-cinematic", "/01-cinematic" not in sa_text)

# --- 6. every evals.json is well-formed and matches its sibling SKILL.md ------
eval_files = sorted(ROOT.glob("plugins/*/skills/*/evals/evals.json"))
total_evals = 0
check("at least one evals.json found", len(eval_files) > 0, f"{len(eval_files)} files")
for ef in eval_files:
    rel = ef.relative_to(ROOT)
    skill_dir = ef.parent.parent
    try:
        data = json.loads(ef.read_text())
    except Exception as e:  # noqa: BLE001
        check(f"evals.json parses: {rel}", False, str(e))
        continue
    check(f"evals.json parses: {rel}", True)
    evals = data.get("evals")
    if not (nonempty_str(data.get("skill_name")) and isinstance(evals, list) and evals):
        check(f"evals.json has skill_name + evals[]: {rel}", False)
        continue
    check(f"evals.json has skill_name + evals[]: {rel}", True)
    expected = skill_names.get(skill_dir)
    check(
        f"evals skill_name matches SKILL.md name: {rel}",
        expected is not None and data["skill_name"] == expected,
        f"eval={data['skill_name']!r} skill={expected!r}",
    )
    bad = [
        e.get("id")
        for e in evals
        if not (
            isinstance(e.get("id"), int) and nonempty_str(e.get("prompt")) and isinstance(e.get("expected_output"), str)
        )
    ]
    check(f"every eval has id:int, prompt, expected_output: {rel}", not bad, f"bad ids {bad}" if bad else "")
    total_evals += len(evals)

# --- summary -----------------------------------------------------------------
print("-" * 60)
if FAILURES:
    print(f"FAILED ({len(FAILURES)} check(s)): " + "; ".join(FAILURES))
    sys.exit(1)
print(f"ALL CHECKS PASSED ({len(skill_files)} skills, {len(eval_files)} eval files, {total_evals} evals)")
sys.exit(0)
