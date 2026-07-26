---
name: marco-propuestas
description: Multi-agent research proposal pipeline for AI grants (LabIA/UNAL style). Use when writing or improving a convocatoria proposal: init drop zones, analyze TDR/draft/ideas, step through sections, or run full interactive pipeline.
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
