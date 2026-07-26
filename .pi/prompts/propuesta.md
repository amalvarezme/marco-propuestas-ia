---
description: Redactar propuesta de investigación en IA (alias de /propuesta-auto).
argument-hint: [idea o contexto inicial]
---
**Nota de ejecución (pi):** sos el agente primario de pi (no hay subagentes anidados tipo Task). Cuando el pipeline diga despachar un rol, leé `.pi/references/agents/<rol>.md` y ejecutá ese rol vos mismo con las herramientas de pi (read/bash/edit/write). Los gates de aprobación requieren sesión **interactiva** de pi — no uses `pi -p` de punta a punta sin gates. Tabla de unidades: `.pi/references/_propuesta-steps.md`.


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

Tabla de unidades: `.pi/references/_propuesta-steps.md`.  
Guía de operador: `docs/usage-modes.md`.

Entrada del usuario:

$ARGUMENTS
