#!/usr/bin/env python3
"""Deterministic, zero-LLM generator: port .claude/ agents + commands into .pi/

  python3 scripts/gen-pi.py           # write .pi/
  python3 scripts/gen-pi.py --check   # dry-run; exit 3 on drift

Exit codes: 0 ok; 1 usage; 2 source/rules error; 3 drift.
Never writes under .claude/. Never hand-edit generated .pi/ as SSOT.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Default root is the repo root (parent of scripts/).  The --root CLI flag
# overrides this so marco init/upgrade can point the generator at the target
# portable-project folder instead of CWD.  All source reads (.claude/) and
# output writes (.pi/) are relative to this root.
REPO_ROOT: Path = Path(__file__).resolve().parent.parent
RULES_PATH = Path(__file__).resolve().parent / "gen-pi.rules.json"


class GeneratorError(Exception):
    pass


def load_rules() -> dict:
    if not RULES_PATH.is_file():
        raise GeneratorError(f"rules file not found: {RULES_PATH}")
    with RULES_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def load_project_config(root: Path) -> dict | None:
    """Read ``<root>/.marco/config.json`` and return the dict, or None if
    the file is absent or unparseable (backward compat for legacy projects)."""
    config_path = root / ".marco" / "config.json"
    if not config_path.is_file():
        return None
    try:
        with config_path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError):
        return None


def split_frontmatter(text: str, source_path: Path) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise GeneratorError(f"{source_path}: missing frontmatter opening '---'")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise GeneratorError(f"{source_path}: missing frontmatter closing '---'")
    fm_block = text[4:end]
    body = text[end + 5 :]
    frontmatter: dict[str, str] = {}
    for line in fm_block.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise GeneratorError(f"{source_path}: malformed frontmatter line: {line!r}")
        key, _, value = line.partition(":")
        frontmatter[key.strip()] = value.strip()
    return frontmatter, body


def apply_all_substitutions(body: str, rules: dict) -> str:
    for rule in rules.get("substitutions_all") or []:
        find = rule.get("find") or ""
        if not find:
            continue
        body = body.replace(find, rule.get("replace", ""))
    return body


def render_prompt_frontmatter(fm: dict[str, str]) -> str:
    lines = ["---"]
    if "description" in fm:
        lines.append(f"description: {fm['description']}")
    if "argument-hint" in fm:
        lines.append(f"argument-hint: {fm['argument-hint']}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def build_prompt(filename: str, rules: dict) -> tuple[str, str]:
    paths = rules["paths"]
    source_path = REPO_ROOT / paths["source_commands_dir"] / filename
    if not source_path.is_file():
        raise GeneratorError(f"source command missing: {source_path}")
    text = source_path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text, source_path)
    if "description" not in fm:
        raise GeneratorError(f"{source_path}: missing description")
    body = apply_all_substitutions(body, rules)
    preamble = rules.get("prompt_preamble") or ""
    # Avoid double preamble if source already starts with pi note
    if preamble and not body.lstrip().startswith("**Nota de ejecución (pi):**"):
        body = preamble + body
    out_rel = f"{paths['output_prompts_dir']}/{filename}"
    return out_rel, render_prompt_frontmatter(fm) + body


def build_role_reference(filename: str, rules: dict, agent_model: str | None = None) -> tuple[str, str]:
    paths = rules["paths"]
    source_path = REPO_ROOT / paths["source_agents_dir"] / filename
    if not source_path.is_file():
        raise GeneratorError(f"source agent missing: {source_path}")
    text = source_path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text, source_path)
    body = apply_all_substitutions(body, rules)
    desc = fm.get("description", filename)
    role_name = filename.removesuffix(".md")
    header = (
        f"# Role card: {role_name}\n\n"
        f"> Generated role card (canonical source is the Claude agents tree). "
        f"pi primary agent: Read this file and execute the role; "
        f"there is no nested subagent spawn.\n\n"
        f"**Description:** {desc}\n\n"
    )
    if agent_model is not None:
        header += f"**Model:** {agent_model}\n\n"
    header += "---\n\n"
    out_rel = f"{paths['output_references_agents_dir']}/{filename}"
    return out_rel, header + body


def build_steps(rules: dict) -> tuple[str, str] | None:
    paths = rules["paths"]
    src = REPO_ROOT / paths["steps_source"]
    if not src.is_file():
        return None
    body = apply_all_substitutions(src.read_text(encoding="utf-8"), rules)
    note = (
        "> Generated step table (canonical source is the Claude commands tree). "
        "Do not hand-edit.\n\n"
    )
    if not body.startswith(">"):
        body = note + body
    return paths["steps_output"], body


def build_skill(rules: dict) -> tuple[str, str]:
    sk = rules["skill"]
    content = f"""---
name: {sk["name"]}
description: {sk["description"]}
---

# Marco de propuestas (pi)

Pipeline multi-agente de propuestas de investigación en IA. **Fuente de verdad
de agentes/comandos: el árbol Claude del repo** — este skill y `.pi/` se
regeneran con `python3 scripts/gen-pi.py` (no editar a mano).

## Entrypoints (prompt templates)

En pi, escribí `/` y elegí:

| Comando | Uso |
|---------|-----|
| `/propuesta-init` | Drop zones bajo `info_data/` (tdr, draft, background, doc-secciones, ideas) |
| `/propuesta-analizar` | Intake only; idea desde args o `ideas/idea.md` |
| `/propuesta-continuar` | Una unidad del pipeline (`next_step`) |
| `/propuesta-auto` | Pipeline completo interactivo |
| `/propuesta` | Alias de auto |
| `/propuesta-limpiar` | Archivar corrida y reset |

## Roles

No hay subagentes anidados. Cuando un prompt pida un especialista, leé:

`.pi/references/agents/<rol>.md`

(p. ej. `investigador.md`, `redactor.md`, `insumos-observador.md`).

## Pasos

`.pi/references/_propuesta-steps.md`

## Límites

- Gates requieren sesión **interactiva** de pi (no `pi -p` de punta a punta).
- Codex no está soportado.
- Tras editar fuentes canónicas Claude, regenerá: `python3 scripts/gen-pi.py`
"""
    rel = f"{paths_skill_dir(rules)}/{sk['dir']}/SKILL.md"
    return rel, content


def paths_skill_dir(rules: dict) -> str:
    return rules["paths"]["output_skills_dir"]


def drift_lint(text: str, rel: str, patterns: list[str]) -> list[str]:
    msgs = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for pattern in patterns:
            if pattern in line:
                msgs.append(
                    f'DRIFT: {rel}:{lineno}: unmapped pattern "{pattern}"'
                )
    return msgs


def config_drift_lint(
    built: list[tuple[str, str]], config: dict, ref_agents_dir: str, repo_root: Path
) -> list[str]:
    """Check each on-disk pi role card's ``**Model:**`` line against
    ``config["agent_models"]``.  Files that do not exist yet (first run)
    are not flagged -- the write phase will create them correctly.
    Returns a list of drift messages (empty = no drift).
    """
    agent_models: dict = config.get("agent_models", {})
    if not agent_models:
        return []

    messages: list[str] = []
    for relpath, _text in built:
        relpath_str = str(relpath)
        if not relpath_str.startswith(ref_agents_dir):
            continue
        filename = relpath_str[len(ref_agents_dir) + 1 :]
        agent_name = filename.removesuffix(".md")
        expected = agent_models.get(agent_name)
        if expected is None:
            continue
        dest = repo_root / relpath_str
        if not dest.is_file():
            continue  # not created yet -- not drift
        on_disk = dest.read_text(encoding="utf-8")
        found_model = False
        for line in on_disk.splitlines():
            if line.startswith("**Model:**"):
                found_model = True
                actual = line[len("**Model:**") :].strip()
                if actual != expected:
                    messages.append(
                        f'CONFIG-DRIFT: {relpath_str}: on-disk model is "{actual}", '
                        f'expected "{expected}" (from .marco/config.json)'
                    )
                break
        if not found_model:
            messages.append(
                f'CONFIG-DRIFT: {relpath_str}: missing "**Model:**" line, '
                f'expected "{expected}" (from .marco/config.json)'
            )
    return messages


def write_output(relpath: str, text: str, check: bool) -> bool:
    if relpath.startswith(".claude/") or "/.claude/" in relpath:
        raise GeneratorError(f"refusing to write under .claude/: {relpath}")
    if not relpath.startswith(".pi/"):
        raise GeneratorError(f"refusing to write outside .pi/: {relpath}")
    dest = REPO_ROOT / relpath
    previous = dest.read_text(encoding="utf-8") if dest.is_file() else None
    changed = previous != text
    if not check and changed:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
    return changed


def main(argv: list[str]) -> int:
    check = False
    root = None
    i = 1
    while i < len(argv):
        arg = argv[i]
        if arg == "--check":
            check = True
            i += 1
        elif arg == "--root":
            i += 1
            if i >= len(argv):
                print(f"error: --root requires an argument", file=sys.stderr)
                return 1
            root = Path(argv[i]).resolve()
            i += 1
        else:
            print(f"usage: {argv[0]} [--check] [--root DIR]", file=sys.stderr)
            return 1

    # Override REPO_ROOT when --root is given (backward compatible: no flag
    # keeps the original behaviour).
    global REPO_ROOT
    if root is not None:
        REPO_ROOT = root

    # Load project config (.marco/config.json) – may be None for legacy
    # projects, in which case we fall back to current behaviour.
    config = load_project_config(REPO_ROOT)
    agent_models: dict = (config or {}).get("agent_models", {})

    try:
        rules = load_rules()
    except GeneratorError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    paths = rules["paths"]
    ref_agents_dir = paths["output_references_agents_dir"]
    built: list[tuple[str, str]] = []
    try:
        for filename in paths["command_files"]:
            built.append(build_prompt(filename, rules))
        for filename in paths["agent_files"]:
            agent_name = filename.removesuffix(".md")
            agent_model = agent_models.get(agent_name)
            built.append(build_role_reference(filename, rules, agent_model=agent_model))
        steps = build_steps(rules)
        if steps:
            built.append(steps)
        built.append(build_skill(rules))
    except GeneratorError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    all_drift: list[str] = []
    for rel, text in built:
        all_drift.extend(drift_lint(text, rel, rules.get("drift_patterns") or []))

    # Config-drift check: if config is present, verify on-disk agent
    # model lines match the config.
    if config is not None:
        all_drift.extend(config_drift_lint(built, config, ref_agents_dir, REPO_ROOT))

    if all_drift:
        for msg in all_drift:
            print(msg, file=sys.stderr)
        return 3

    try:
        for rel, text in built:
            changed = write_output(rel, text, check)
            verb = (
                "would write"
                if check and changed
                else ("wrote" if changed else "unchanged")
            )
            print(f"{verb}: {rel}")
    except GeneratorError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if check:
        print("--check: no drift, no writes performed.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
