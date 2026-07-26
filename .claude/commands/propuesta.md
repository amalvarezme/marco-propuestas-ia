---
description: Redactar propuesta de investigación en IA (alias de /propuesta-auto).
argument-hint: [idea o contexto inicial]
---

# /propuesta — Modo automático

`/propuesta` es un alias de `/propuesta-auto`.

| Comando | Propósito |
|---------|-----------|
| `/propuesta-init` | Crear estructura inicial (`info_data/`, `proposal/`, `vault/`) |
| `/propuesta-analizar` | Inspeccionar insumos sin redactar; establece `next_step: fase1a` |
| `/propuesta-continuar` | Una unidad del pipeline; imprime el siguiente comando |
| `/propuesta-auto` | Pipeline completo (esta sesión) |
| `/propuesta` | Este alias → mismo que auto |
| `/propuesta-limpiar` | Archivar corrida activa y resetear workspace |

Tabla de unidades: `.claude/commands/_propuesta-steps.md`.  
Guía de operador: `docs/usage-modes.md`.

Entrada del usuario:

$ARGUMENTS
