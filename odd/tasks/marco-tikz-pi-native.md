# Feature: bucle de figuras rápido + runtime Pi-native + independencia de Engram

## Goal

Depurar tres defectos de framework detectados con evidencia medida en la corrida
`2026-09-tept-depresion-ia-portable`, y devolver el trabajo a la propuesta de salud
mental.

1. **Bucle de figuras**: bajar de **~29 min por figura** (medido) a **< 3 min**
   generación + validación. Arquitectura elegida por el operador:
   **renderizador determinista + 1 agente** (no LLM dibujando layout).
2. **Modelos Pi-native**: el proyecto no debe depender de `claude-bridge` (puente al
   Claude Agent SDK) ni de archivos sin versionar. La tabla de modelos se valida y
   confirma con el usuario en `/propuesta-init`, contrastada contra el perfil activo
   de `gentle:profiles`.
3. **Independencia de Engram**: ninguna regla, proceso o aprendizaje puede vivir solo
   en Engram. En un clon nuevo el flujo debe funcionar completo desde los `.md`, `.py`
   y `.sh` versionados; Engram queda como espejo local opcional.

## Evidencia (medida, no inferida)

`artefactos/pipeline/30-fase2.md`, Fase 2 de la corrida de salud mental:

| Despacho | Duración | Resultado |
|---|---|---|
| `disenador-tikz` intento 1/4 | 565 923 ms (9,4 min) | falló sin reporte |
| `disenador-tikz` intento 2/4 | 373 254 ms (6,2 min) | falló sin reporte |
| `disenador-tikz` intento 3/4 | 440 174 ms (7,3 min) | falló sin reporte |
| `tikz-optimizer` (fix de sobreflujo) | 96 297 ms (1,6 min) | OK |
| `revisor-figuras` (auditoría visual) | 254 515 ms (4,2 min) | PASS |
| **Total del bucle de una figura** | **1 730 163 ms (~28,8 min)** | |

`python3 redaccion/scripts/compile_tikz.py <name>:tikz` (pdflatex + pdftoppm +
pdftocairo) tarda **~1,0 s**. La compilación nunca fue el cuello de botella.

### Causas raíz

- **R1 — agotamiento del presupuesto de salida.** `disenador-tikz` corría en
  `nan/deepseek-v4-flash` con `effort: high` y `maxTokens=32768` (tope del proveedor
  `nan`). Patrón ya diagnosticado en la misma corrida para `grant-flow-auditor`:
  `stopReason: length`, ~16 000 tokens de razonamiento y **cero tokens de texto** → el
  agente nunca emite reporte. Tres reintentos ≈ 23 min perdidos por figura. Ocurrió
  también en Fase 1 (árbol de problemas) y en `revisor-figuras` (dos veces, ver
  `odd/tasks/revision-figuras-equipo-anexos.md`).
- **R2 — el LLM dibuja el layout a mano.** `diag_estado_arte.tex` = 254 líneas de
  anclas manuales, `text width` y grupos `fit`. Depurar layout es lo caro; elegir el
  contenido es barato. Todo el catálogo de defectos que `revisor-figuras` persigue
  (traslapes, anclas flotantes, desbordes de texto, hiphenación) es geometría
  determinista, no juicio estético.
- **R3 — 3 despachos mínimo por figura**, cada uno recargando el prompt del agente más
  los fragmentos de guía inyectados.
- **R4 — auditoría visual sobre un PNG de 658 KB a 200 DPI** (~10 tool-uses). 6 de sus
  8 criterios son mecánicos y un script los resuelve en < 1 s.
- **R5 — capa Pi sin versionar.** `.pi/subagents.json` (los perfiles `nan/*`) está
  *untracked* y **no** figura en `kit-manifest.json`. En un clon nuevo ese archivo no
  existe, así que los 10 agentes caen al `model:` de su frontmatter, que es
  `claude-bridge/claude-sonnet-5` o `claude-bridge/claude-opus-5`. `.pi/agents/`,
  `.pi/prompts/`, `.pi/skills/` y `.pi/README.md` tampoco están en `kit_paths`, así que
  `marco init` no instala el runtime Pi.
- **R6 — Engram como única caché de extracción de insumos** (`insumos-observador.md`).
  Degrada bien si falla, pero en un clon nuevo se re-extrae todo. Además hay un bug de
  ruta en las tres copias: `artefactos/artefactos/vault/insumos/<slug>.md`.

## Decisiones del operador (autoridad)

- **D1 (arquitectura)**: renderizador determinista + 1 agente.
- **D2 (modelos)**: validar al iniciar sesión con el usuario y contrastar contra el
  perfil activo en `gentle:profiles`.

## Contexto verificado del runtime

- `gentle:profiles` vive en `~/.pi/gentle-ai/profiles.json`
  (`kind: gentle-pi.agent_model_profiles`, `version: 1`). Perfil activo:
  **`andres_nan`** — todos los agentes globales en `nan/*`, sin `claude-bridge`.
  Orquestador: `nan/deepseek-v4-flash`, thinking `high`.
- El perfil activo **no cubre** los 10 agentes del marco de propuestas: esos se
  resuelven por `.pi/subagents.json` (proyecto) y, en su defecto, por el frontmatter
  del agente.
- Precedencia verificada en `pi-subagents-j0k3r/src/profile-resolver.ts`:
  `project_model_profiles[agent]` → `definition.model` (frontmatter) → `default_model`
  → modelo del orquestador. `src/config.ts` lee el proyecto desde
  `<cwd>/.pi/subagents.json`.
- Los ids `nan/*` de `.pi/subagents.json` existen en `pi --list-models`
  (`nan/glm5.3-flash`, `nan/deepseek-v4-flash`, `nan/mimo-v2.5`, `nan/mimo-v2.6-flash`,
  `nan/gemma4`, `nan/qwen3.6`, `nan/qwen3.8-flash`).

## Tasks

- [x] T1 Registro del plan (este documento + espejo Engram)
- [x] T2 `render_tikz.py` — TikZ determinista desde spec JSON
      (`arbol`, `estado_arte`, `metodologico`); geometría calculada, no dibujada
- [x] T3 Autofix determinista de sobreflujo (sustituye el bucle LLM de layout)
- [x] T4 `audit_tikz.py` — los criterios mecánicos de `revisor-figuras` en JSON
- [x] T5 `figura.py` — entrada única render + compile + audit, presupuesto 3 min
- [x] T6 Rewire de agentes TikZ y de los bucles de figura (fases 1, 2, 5.5) en
      `propuesta.md`, `_propuesta-steps.md` y `AGENTS.md`
- [x] T7 Modelos Pi-native: `.pi/subagents.json` versionado + SSOT de modelos +
      frontmatter sin `claude-bridge`
- [x] T8 `/propuesta-init`: validación de runtime y confirmación de modelos contra
      `gentle:profiles`
- [x] T9 Independencia de Engram: caché de insumos en disco + fix de la ruta
      `artefactos/artefactos/`
- [x] T10 `kit-manifest.json`: versionar `.pi/`, generadores y `graph_html.py`
- [x] T11 Tests, `--check` de generadores, docs sincronizados y commit
- [ ] T12 Propuesta de salud mental: T3 del round anterior (rediseño de
      `diag_estado_arte.tex`) con el pipeline nuevo

## Evidence

(pendiente — se completa por tarea)

## Allowed edit surfaces

- `plantilla/scripts/`
- `.claude/agents/`, `.claude/commands/`, `.claude/skills/`
- `scripts/`
- `.pi/`
- `docs/`
- `tests/`
- `AGENTS.md`, `.gitignore`
- `odd/tasks/`

Fuera de alcance: cualquier ruta bajo `proposals/<run-id>/redaccion/` salvo la T12
(que solo toca `diag_estado_arte.tex` y sus figuras).

## Evidence

- **T1**: este documento + espejo Engram (observación `marco-propuestas/tikz-pi-native-diagnostico`).
- **T2**: `plantilla/scripts/render_tikz.py` — render determinista desde spec JSON para
  `arbol`, `estado_arte` y `metodologico`. Render medido: **0,037 s**. Dos renders del mismo
  spec son **byte-idénticos** (test `test_render_is_byte_identical_across_runs`). Valida la spec
  con mensajes que nombran el campo (ids duplicados, enlace a un clúster inexistente, arista que
  apunta fuera de su clúster, rol de fuente desconocido) y verifica el **balance de llaves** del
  documento generado: una llave faltante producía `Undefined control sequence` en el `\node`
  siguiente, sin relación aparente con la causa.
- **T3**: autofix determinista en `render_tikz.py --fix-overfull <línea>:<pt>`, dirigido por el
  mapa línea→nodo derivado del `.tex` generado. Salta directo al ancho canónico en vez de subir
  centímetro a centímetro. Caso limpio: **1 compilación, 1,00 s**. Peor caso (5 roles sembrados
  con anchos imposibles): **6 compilaciones, 5,47 s, PASS** (test
  `test_overfull_is_fixed_deterministically`).
- **T4**: `audit_tikz.py` — 15 chequeos mecánicos en JSON, ~0,001 s. PASS en los tres tipos.
  Reporta además el **tamaño físico** de la figura en cm y, si se pide `--page-fit WxH`, si cabe.
- **T5**: `figura.py <name> --spec …` = render + compile + autofix + audit + presupuesto de reloj.
  Sale con código distinto de cero si supera `--budget-s` (180 s por defecto).
- **T6**: `disenador-tikz` (autor de la spec), `tikz-optimizer` (corrige la spec, nunca el `.tex`),
  `revisor-figuras` (solo los 4 criterios visuales, sobre el PNG de vista previa de 1400 px).
  El bucle de figuras quedó definido **una sola vez** ("Bucle de figuras (canónico)" en
  `propuesta.md`) y las Fases 1, 2 y 5.5 lo referencian; `AGENTS.md` y `coordinador-propuesta.md`
  alineados. `compile_tikz.py` emite además `fig_<name>-preview.png`.
- **T7**: `scripts/agent-models.json` (fuente de verdad: 3 tiers, 10 agentes, guardia
  `allow_claude_bridge: false`) → `gen-pi.py` escribe de ahí **tanto** el frontmatter de
  `.pi/agents/*.md` **como** todo `.pi/subagents.json`. Modelos efectivos:
  `nan/deepseek-v4-flash` y `nan/glm5.3-flash`. `claude-bridge` desapareció del flujo.
- **T8**: paso 0 obligatorio en `/propuesta-init` (genérico en `.claude/`, con el mecanismo Pi
  inyectado por sustitución): verificar el agente de código, listar modelos reales, contrastar
  contra el perfil activo de `gentle:profiles` (`~/.pi/gentle-ai/profiles.json`), mostrar la tabla
  y pedir confirmación explícita antes de crear la corrida.
- **T9**: la caché de extracción de insumos pasa a `artefactos/insumos-cache/<hash>.json`
  (**disco primario**), con Engram como **espejo opcional**; `init-run.sh` crea el directorio.
  Corregidas 9 rutas con `artefactos/artefactos/` duplicado en `.claude/`.
- **T10**: `kit-manifest.json` 0.4.0 → 0.5.0, 38 → 58 `kit_paths`: se añadieron los tres
  generadores con sus datos, `graph_html.py`, `convert_to_word.py`, los scripts de figura, docs
  markdown, tests y guías. **Los puertos de runtime (`.pi/`, `.opencode/`, `.agent/`) NO se
  listan**: `marco init/upgrade` los materializa ejecutando el generador de cada `--tools`, y
  listarlos rompía ese filtro (`init --tools claude` instalaba el puerto de OpenCode; detectado
  por la suite).
- **T11**: 62 tests OK (41 previos + 21 nuevos en `tests/test_figure_pipeline.py`), los tres
  generadores sin drift, `--check` en 0.
- **T12**: `specs/estado_arte.spec.json` construido desde el bloque autorizado de
  `04_estado_arte.tex` (5 clústeres × 5 papers, 16 aristas internas declaradas, limitante por
  clúster). Medición antes → después: **17,0 × 31,3 cm → 17,78 × 28,54 cm**, PASS en 1,1 s.

## Decisión del operador (resuelta el 2026-09-30)

Ante el blocker de página, el operador eligió **dos figuras**. Ejecutado:

- El mapa se partió en `specs/estado_arte_a.spec.json` (clústeres 1-3, `cols=3`) y
  `specs/estado_arte_b.spec.json` (clústeres 4-5 + cierre transversal, `cols=2`).
  La spec monolítica `specs/estado_arte.spec.json` se retiró.
- Tamaños medidos a tamaño natural, con `--page-fit 16.2x24` (el `\textwidth` real
  de la plantilla A4 es 16,26 cm con `margin=2.4cm`):

  | figura | tamaño | cabe |
  |---|---|---|
  | `arbol_problemas` | 15,71 × 19,08 cm | sí |
  | `estado_arte_a` (grupos 1-3) | 15,53 × 12,62 cm | sí |
  | `estado_arte_b` (grupos 4-5) | 9,47 × 15,57 cm | sí |

- `main.tex`: se eliminó el `\resizebox{!}{0.92\textheight}` y se pusieron dos
  entradas `\begin{figure}` con dos captions y dos `\label`
  (`fig:estado_arte_a`, `fig:estado_arte_b`).
- §4 (`04_estado_arte.tex`): la referencia cruzada pasó de
  `\Cref{fig:estado_arte}` a `\Cref{fig:estado_arte_a,fig:estado_arte_b}`.
- `main.pdf` recompilado desde cero: **15 páginas, 0 `Overfull \hbox`, 0
  referencias indefinidas, 3 figuras**. Los tamaños canónicos se imprimen ahora
  a su valor real en lugar de al ~74 %.

Además, `figura.py` permite `--page-fit WxH` (por defecto `none`): reporta
siempre el tamaño físico y solo lo exige cuando el operador pide que la figura
entre a tamaño natural. La convención quedó documentada en la sección "Tamaño de
página de las figuras" de `propuesta.md`, con la regla de partir en `<base>_a` /
`<base>_b` cuando un diagrama no cabe sin recortar contenido. El árbol de
problemas también se ajustó para entrar en `\textwidth` sin `resizebox`.
