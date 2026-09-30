# Feature: Spanish natural-prose skill (`estilo-natural-es`) + pipeline wiring

## Goal

Add a proposal-safe Spanish prose-polishing skill to the framework so the
writing flow can remove mechanical "AI texture" from the proposal narrative,
without the deceitful framing or quality-degrading techniques of the upstream
community skill it is derived from.

## Provenance

Derived from the community skill `humanizar-texto-es`
(`majiayu000/claude-skill-registry`, `skills/productivity/…-humanizar-texto-es-11`).
That skill is framed as *AI-detection evasion* and includes deliberate typos,
artificial imprecision, emotional insertions and register mixing. Those parts
are rejected here (user decision, option "Adaptar a propuesta").

## Decisions

- Canonical source: `.claude/skills/estilo-natural-es/SKILL.md` (Claude/OpenCode
  read `.claude/skills/` natively; OpenCode also auto-scans project
  `.claude/skills/**/SKILL.md`).
- Pi port: generated into `.pi/skills/estilo-natural-es/SKILL.md`.
- Antigravity port: generated into `.agent/skills/estilo-natural-es/SKILL.md`.
- OpenCode: **no** generated copy, to avoid a duplicate-name warning — it
  auto-discovers the canonical `.claude/skills/`.
- Wiring: the skill is applied as a new pass of the existing `grant-flow-auditor`
  (prose micro-style auditor) that already runs before every `revisor` gate. No
  new agent is added; the roster stays at 11.
- Skill instructions in English (framework convention for agent/skill system
  prompts; see `AGENTS.md` rule 1), Spanish linguistic examples as data.

## Red lines encoded in the skill

Fidelity of numbers/dates/citations/LaTeX, no invented sources, no deliberate
typos, no manufactured vagueness, no colloquial or emotional register, no new
output files (edit in place).

## Tasks

- [x] T1 Canonical skill `.claude/skills/estilo-natural-es/SKILL.md`
- [x] T2 Wire into `grant-flow-auditor`, `propuesta.md`, `coordinador-propuesta.md`, `AGENTS.md`, `docs/pipeline-flow.md`
- [x] T3 `gen-pi.py` + rules port skills
- [x] T4 `gen-antigravity.py` + rules port skills
- [x] T5 `kit-manifest.json` path + version bump
- [x] T6 Regenerate ports + `.pi/README.md`
- [x] T7 Tests for skill porting and generator `--check`
- [x] T8 Full suite + all `--check` green

## Evidence

- Generator check: `python3 scripts/gen-pi.py --check`, `gen-antigravity.py --check`,
  `gen-opencode.py --check` all exit 0.
- Tests: `python3 -m unittest discover -s tests` green.
- Commit: (not committed). The working tree already carried unrelated in-flight changes (graph_html work) and `odd/tasks/` is new; committing would have entangled them. Left to the maintainer as an explicit decision.
