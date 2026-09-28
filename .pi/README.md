# `.pi/` — Pi runtime port (GENERATED, never hand-edited)

Pi is a supported secondary runtime of this framework. Everything in this
directory except this file is generated, deterministically and with zero LLM
calls, from the canonical Claude Code sources under `.claude/`:

```bash
python3 scripts/gen-pi.py          # write .pi/
python3 scripts/gen-pi.py --check  # dry-run; non-zero exit on drift or diff
```

| Path | Generated from | Pi role |
|---|---|---|
| `.pi/agents/*.md` (9 files) | `.claude/agents/*.md` | Project subagents, dispatched with `subagent_run` |
| `.pi/prompts/*.md` (3 files) | `.claude/commands/*.md` | Prompt templates exposed as `/propuesta`, `/propuesta-init`, `/propuesta-limpiar` |

Both paths are Pi's documented project-level resource directories
(`docs/configuration.md`: "Project `.pi` directory"), so no setup step and no
`settings.json` entry is needed. They load **after project trust is granted**
(the interactive trust prompt, or `pi --approve`). Run `/reload` after
regenerating if a session is already open.

`coordinador-propuesta.md` is intentionally **not** ported: it is the canonical
pipeline reference document, never a dispatchable subagent (a subagent cannot
invoke other subagents). The generated `/propuesta` keeps the reference as a
bare filename.

## What the port changes, and why

The mapping rules live in `scripts/gen-pi.rules.json` (data only — the
generator has no project-specific knowledge):

- **Models**: `sonnet` → `claude-bridge/claude-sonnet-5`, `opus` →
  `claude-bridge/claude-opus-5` (both confirmed available by
  `pi --list-models`). Pi's `thinking` level is derived from the source tier
  (`medium` / `high`).
- **Tools**: an agent with an explicit Claude `tools:` value maps to Pi's
  equivalent (`Read, Grep, Glob` → `read, grep, find`). An agent with **no**
  `tools:` field omits the field in Pi too, keeping the harness default set —
  the port never narrows an agent beyond its Claude original.
- **Dispatch vocabulary**: `Task` → `subagent_run`, `.claude/agents/` →
  `.pi/agents/`, `Read/Grep/Glob` → `read/grep/find`.
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
