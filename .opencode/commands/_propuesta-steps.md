# Canonical pipeline step table (SSOT)

**Not a slash command.** Reference fragment for `/propuesta-continuar`,
`/propuesta-auto`, and `/propuesta-analizar`. Full Task recipes, graphify
rules, and gate prose live in `.opencode/commands/propuesta-auto.md` (body
ported from the historical monolith). This file defines **unit ids**,
**order**, and **what each unit covers** so stepped and auto modes cannot
diverge.

Also summarized in `.opencode/agents/coordinador-propuesta.md`.

## Control de ejecución (`proposal/estado_propuesta.md`)

Every run that uses analizar / continuar / auto MUST maintain:

```markdown
## Control de ejecución
- mode: stepped | auto
- next_step: <id> | done
- next_command: /propuesta-continuar | (none)
- last_completed: <id or gate id or empty>
- intake_complete: true | false
```

| Field | Meaning |
|-------|---------|
| `mode` | `stepped` after `/propuesta-analizar` or when using continuar; `auto` for `/propuesta-auto` / `/propuesta` |
| `next_step` | Unit id to run next (see table below) |
| `next_command` | Usually `/propuesta-continuar` in stepped mode; `(none)` when `done` or in pure auto mid-session |
| `last_completed` | Last finished unit or gate |
| `intake_complete` | `true` after Fase 0 (+ G0.5 if applicable) finished |
| `idea` / `idea_source` | Resolved research idea and source (`arguments` \| `ideas/idea.md` \| `ideas/*` \| `user`) |

**Clearing state:** `/propuesta-limpiar` and ARCHIVADO-Y-REINICIO rewrite
`proposal/estado_propuesta.md` to empty (0 bytes) — no stale `next_step`.

## Step sequence (post-intake)

| `next_step` | Unit | Gate | On PASS → next |
|-------------|------|------|----------------|
| `fase1a` | Early scoping (bibliógrafo MODE=scope, graphify scoping, investigador early) | G1a | `fase1b` |
| `fase1b` | SOTA corpus expansion + WRITE-REFS + vault graphify once | G1b | `fase1` |
| `fase1` | §3 problema + árbol de problemas (fig loop) + revisor | G1 | `fase2` |
| `fase2` | §4 SOTA + §5 hipótesis + mapa SOTA (fig) + revisor | G2 | `fase3` |
| `fase3` | §2 justificación + revisor | G3 | `fase4` |
| `fase4` | §6–§7 objetivos + revisor | G4 | `fase5` |
| `fase5` | §8 marco + §9 equipo + revisor | G5 | `fase5_5` |
| `fase5_5` | §10 metodología + diagrama (fig) + revisor | G5.5 | `fase6` |
| `fase6` | §11 resultados + §12 ética (no own gate) | — | `fase6_4` |
| `fase6_4` | §13 presupuesto + revisor | G budget | `fase6_45` |
| `fase6_45` | §14 cronograma + §15 productos + §16 bib (no own gate) | — | `fase6_5` |
| `fase6_5` | Front-matter + revisor | G front | `fase7` |
| `fase7` | Final audit + assemble `main.tex` | G final | `done` |
| `done` | Pipeline complete | — | print `cd proposal && ./build.sh` |

**Pre-intake units** (only in analizar / start of auto, not as `next_step` after
intake):

| Logical unit | Command | Sets after success |
|--------------|---------|-------------------|
| `fase0` | run-id, collision, insumos-observador, INTAKE, TDR/draft routing | (internal) |
| `g0_5` | Optional guide adjusted to TDR | `next_step: fase1a`, `intake_complete: true` |

## Stepped vs auto

| Mode | Behavior |
|------|----------|
| **stepped** | `/propuesta-continuar` runs **exactly one** row from the table, then stops and prints the next command |
| **auto** | Loop all rows in one session; stop only at gates that already require user approval |

Units without a formal gate (`fase6`, `fase6_45`) still **stop once** in
stepped mode after the unit finishes, so the operator always re-invokes
`/propuesta-continuar` deliberately.

## Recipe authority

For each unit id, execute the matching **Fase …** block in
`.opencode/commands/propuesta-auto.md` (same content as the historical
`propuesta.md` pipeline). Do not invent alternate Task graphs.

## Standardized Next Steps Output Banner (`## 🎯 NEXT STEPS`)

Every proposal command and agent execution phase MUST append a standardized `## 🎯 NEXT STEPS` block at the end of its response report.

Format:
```markdown
## 🎯 NEXT STEPS
- **Phase Completed**: [Phase / Step Name]
- **Files Modified**: `proposal/...`, `vault/...`
- **Action Required**: Review changes or provide gate approval
- **Next Command**: `/propuesta-continuar` (or compilation instructions if done)
```

