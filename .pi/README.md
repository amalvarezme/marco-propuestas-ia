# `.pi/` — Pi runtime port (GENERATED, never hand-edited)

Pi is a supported secondary runtime of this framework. Everything in this
directory except this file is generated, deterministically and with zero LLM
calls, from the canonical Claude Code sources under `.claude/`:

```bash
python3 scripts/gen-pi.py            # write .pi/
python3 scripts/gen-pi.py --check    # dry-run; non-zero exit on drift or diff
python3 scripts/gen-pi.py --root DIR # write DIR/.pi (used by `marco init`)
```

| Path | Generated from | Pi role |
|---|---|---|
| `.pi/agents/*.md` (10 files) | `.claude/agents/*.md` + `scripts/agent-models.json` | Project subagents, dispatched with `subagent_run` |
| `.pi/prompts/*.md` (7 files) | `.claude/commands/*.md` | Prompt templates exposed as `/propuesta`, `/propuesta-init`, `/propuesta-insumos`, `/propuesta-analizar`, `/propuesta-continuar`, `/propuesta-limpiar`, plus the frontmatter-less `_propuesta-steps.md` step table they reference |
| `.pi/skills/**/SKILL.md` (1 file) | `.claude/skills/**/SKILL.md` | Project skills, advertised by name+description and loadable with `/skill:estilo-natural-es` |
| `.pi/subagents.json` | `scripts/agent-models.json` | Project-scope subagent profile store: the model and thinking level each of the 10 agents actually runs on |

Both paths are Pi's documented project-level resource directories
(`docs/configuration.md`: "Project `.pi` directory"), so no setup step and no
`settings.json` entry is needed. They load **after project trust is granted**
(the interactive trust prompt, or `pi --approve`). Run `/reload` after
regenerating if a session is already open.

`coordinador-propuesta.md` is intentionally **not** ported: it is the canonical
pipeline reference document, never a dispatchable subagent (a subagent cannot
invoke other subagents). The generated `/propuesta` keeps the reference as a
bare filename.

OpenCode needs no skill port: it discovers project `.claude/skills/**/SKILL.md`
automatically, so the canonical skill is generated only into `.pi/skills/` and
`.agent/skills/`, never into `.opencode/skills/` (a second copy would raise a
duplicate-name warning).

## What the port changes, and why

The mapping rules live in `scripts/gen-pi.rules.json` (data only — the
generator has no project-specific knowledge):

- **Models**: resolved **per agent**, not from the Claude tier, out of
  `scripts/agent-models.json`. The canonical `.claude/` source declares a Claude
  tier (`sonnet`/`opus`) because Claude Code is its native runtime; the Pi port
  resolves each of the 10 agents to a concrete Pi model from that file's
  `tiers` (`reasoning` / `analysis` / `mechanical`). This is deliberate: a
  direct tier mapping produced `claude-bridge/claude-sonnet-5` and
  `claude-bridge/claude-opus-5`, and `claude-bridge` is a bridge to the Claude
  Agent SDK — an external Claude dependency this framework must not acquire.
  The generator **fails** on a bridge model unless `allow_claude_bridge` is set
  to `true` deliberately in `agent-models.json`.
- **One source of truth for two outputs**: the same file produces both the
  `model:`/`thinking:` frontmatter of `.pi/agents/*.md` and the whole of
  `.pi/subagents.json`. Pi's subagent resolver gives a project profile
  precedence over the agent's own frontmatter, so emitting both from one source
  means the declared fallback and the effective profile cannot drift apart.
  `.pi/subagents.json` **must stay versioned**: without it a fresh clone falls
  back to the agent frontmatter alone.
- **Reconciliation at session start**: `/propuesta-init` re-reads the operator's
  **active** `gentle:profiles` profile (`~/.pi/gentle-ai/profiles.json`), checks
  every model id against `pi --list-models`, shows the resulting table, and only
  then confirms or rewrites `agent-models.json`. The generator never inspects
  the operator's machine.
- **Tools**: an agent with an explicit Claude `tools:` value maps to Pi's
  equivalent (`Read, Grep, Glob` → `read, grep, find`). An agent with **no**
  `tools:` field omits the field in Pi too, keeping the harness default set —
  the port never narrows an agent beyond its Claude original.
- **Dispatch vocabulary**: `Task` → `subagent_run`, `.claude/agents/` →
  `.pi/agents/`, `Read/Grep/Glob` → `read/grep/find`.
- **Skills**: `.claude/skills/**/SKILL.md` → `.pi/skills/**/SKILL.md`, keeping
  only the Agent Skills frontmatter Pi understands
  (`name`, `description`, `license`, `compatibility`, `metadata`,
  `allowed-tools`, `disable-model-invocation`). Agent/command prose references a
  skill by name and the dispatcher passes its exact `SKILL.md` path, so no
  runtime-specific skill path is hardcoded in generated files.
- **Interactive-session note** injected at the top of `/propuesta`: the
  approval gates need a live or resumed session (`pi`, `pi -c`); `pi -p`
  cannot stop to wait for a human at a gate.

A drift lint fails the generator (exit 3) if `Claude Code`, `.claude/`,
`` `Task` `` or `Task tool` survives into any generated file, so a future edit
to a `.claude/` source cannot silently leak Claude-specific instructions into
the Pi port.

## Requirements

`.mcp.json` declares the MCP servers the pipeline uses, including
`codegraph` (**codebase-memory**, `codegraph serve --mcp`), which the
dispatcher calls for the run's two graph indexes. Pi reads project MCP servers
from its own configuration; if a ported agent reports no MCP tools, add an
explicit `tools` value for it in `gen-pi.rules.json` instead of narrowing the
others.

This file is versioned so the directory travels with the repository: without
it a collaborator cloning the repo would see `.claude/` and `.opencode/`, no
`.pi/`, and reasonably conclude Pi is not supported. It is.
