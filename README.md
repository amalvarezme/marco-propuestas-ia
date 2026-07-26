# Marco de Redacción de Propuestas de Investigación en IA - Laboratorio de IA - UNAL Manizales

<p align="center">
  <img src="https://raw.githubusercontent.com/amalvarezme/marco-propuestas-ia/main/logos/logo_labIA_readme.png" alt="Logo Laboratorio de IA" width="280">
  <br>
  <a href="https://amalvarezme.github.io/LaboratorioIA_UNAL/">amalvarezme.github.io/LaboratorioIA_UNAL</a>
</p>

Framework multi-agente que produce propuestas de investigación en IA en
**español**, como LaTeX, en `proposal/` (versión de referencia). En paralelo,
los agentes mantienen un mirror Markdown/Obsidian navegable en `vault/`
(`vault/secciones/`, `vault/insumos/`) — capa visual para explorar la
propuesta como grafo de ideas; **nunca** es fuente de verdad, ese rol lo
conserva `proposal/`. **Runtime canónico: Claude Code** (`.claude/agents/` +
`.claude/commands/`, la única fuente editada a mano). **OpenCode** y **pi**
son runtimes secundarios generados: `python3 scripts/gen-opencode.py` →
`.opencode/`; `python3 scripts/gen-pi.py` → `.pi/prompts` + role cards
(`.pi/references/agents/`) + skill `marco-propuestas`. No editar `.opencode/`
ni `.pi/` a mano. **Codex** no está soportado.
El asistente primario despacha 9 subagentes de dominio — `investigador`,
`redactor`, `revisor`, `bibliografo-propuesta`, `presupuestador`,
`insumos-observador`, `disenador-tikz`, `tikz-optimizer`, `revisor-figuras` —
usando el comando `/propuesta` (`.claude/commands/propuesta.md`), siguiendo la
referencia canónica del pipeline en `.claude/agents/coordinador-propuesta.md`
(el 10º archivo de `.claude/agents/`, no se despacha como subagente sino que
documenta el pipeline), avanzando por fases con puertas de revisión (gates).

**Eficiencia de tokens.** El dispatcher lee `guiaProyectosIA_Agente.md` (o la
guía ajustada al TDR generada en G0.5) **una sola vez por corrida** y le
inyecta a cada subagente solo el fragmento de sección que necesita (bloque
`## FRAGMENTO DE GUÍA`, ver "FORMATO EXACTO DE INYECCIÓN" en
`.claude/commands/propuesta.md`), en vez de que cada Task relea el archivo
completo — la única excepción es la auditoría final (Fase 7), que sí necesita
la guía íntegra. `insumos-observador` además cachea en Engram, por hash de
contenido, la extracción de cada archivo de `info_data/`: corridas repetidas
contra el mismo insumo (p. ej. la misma convocatoria) no vuelven a procesarlo
desde cero.

**Telemetría de uso por fase.** El dispatcher lee el bloque `<usage>` que
devuelve cada `Task` delegado (tokens, tool-uses, duración), lo acumula por
fase y lo persiste en `proposal/pipeline/_estado.md` (columnas `Tokens |
Tool-uses | Duración`) y en el frontmatter de cada evento de fase
(`proposal/pipeline/<NN>-<fase>.md`: `tokens_total`, `tool_uses`,
`duration_ms`). Cada cierre de gate agrega un 4º punto — "(d) Costo/tiempo" —
a la tríada habitual (resumen, veredicto, aprobación), y la Fase 7 cierra con
una tabla resumen de una fila por fase.

**Bucle de figuras: precheck de overflow y tope de reintentos.** Antes de la
revisión visual de `revisor-figuras`, `proposal/scripts/compile_tikz.py`
detecta determinísticamente `Overfull \hbox` en el log de `pdflatex` y lo
mapea a la línea del `.tex` fuente (token `OVERFULL: <diagrama> <N>
occurrence(s)`); si `N > 0`, el dispatcher reenvía directo a
`tikz-optimizer` sin gastar el `Read` visual de `revisor-figuras` en esa
iteración. Los 3 bucles de figura (árbol de problemas, estado del arte,
diagrama metodológico) comparten un tope de 4 intentos entre fallos de
overflow y fallos visuales, con escalamiento explícito al usuario si se
agota — nunca reintentan sin límite.

## Estructura

```
.
├── AGENTS.md                        # Playbook / reglas globales
├── guiaProyectosIA_Agente.md        # Guía autoritativa sección por sección
├── .mcp.json                        # Config de MCP servers
├── info_data/                       # Insumos del usuario (vacío entre corridas)
├── logos/                           # Logos institucionales (branding del repo/README)
├── scripts/                         # gen-opencode.py, gen-pi.py + rules JSON
├── .claude/                         # Runtime canónico — única fuente editada a mano
│   ├── agents/                      # 10 archivos: 9 subagentes + coordinador-propuesta
│   └── commands/                    # /propuesta-* + _propuesta-steps.md
├── .opencode/                       # GENERADO (gen-opencode.py) — no editar a mano
│   ├── agents/
│   └── commands/
├── .pi/                             # GENERADO (gen-pi.py) — no editar a mano
│   ├── prompts/                     # /propuesta-* (slash templates)
│   ├── references/agents/           # Role cards (primary ejecuta el rol)
│   └── skills/marco-propuestas/
├── vault/                           # Mirror Obsidian navegable (Markdown) — capa visual, no versión de verdad
│   ├── secciones/                   # Espejo de proposal/sections/*.tex por sección
│   └── insumos/                     # Espejo de proposal/insumos.md
├── proposals/                       # Índice + corridas archivadas de /propuesta (local, no en GitHub)
│   └── registry.md                  # Único archivo versionado: tabla append-only de metadatos
│                                     #   (run-id, estado, ruta local) — proposals/<run-id>/ en sí
│                                     #   está en .gitignore
└── proposal/                        # Framework de salida LaTeX (versión de referencia)
    ├── build.sh                     # Compilación PDF/DOCX
    ├── scripts/                     # compile_tikz.py, prep_docx.py — específico del build LaTeX/DOCX
    ├── logos/                       # Logos institucionales embebidos en el PDF (header/footer)
    ├── templates/reference.docx     # Plantilla pandoc (export DOCX)
    │   # Generados por cada corrida de /propuesta (gitignored, ver "Qué se versiona" abajo):
    └── ...                         #   main.tex, refs.bib, sections/, estado_propuesta.md
```

### Qué se versiona en GitHub (y qué no)

El repo remoto solo contiene lo necesario para **correr el pipeline en
local**: agentes (`.claude/agents/`, `.opencode/agents/`), comandos
(`.claude/commands/`, `.opencode/commands/`), tooling (`scripts/`,
`proposal/scripts/`, `proposal/build.sh`), plantillas/logos
(`proposal/templates/`, `proposal/logos/`), la guía
(`guiaProyectosIA_Agente.md`) y `proposals/registry.md` (solo metadatos:
run-id, fechas, idea breve, ruta local — nunca contenido de la propuesta).

**Nunca** se sincroniza el contenido de una propuesta, ni de la corrida
activa ni de las archivadas: `proposal/sections/`, `proposal/refs.bib`,
`proposal/main.tex/.pdf/.docx`, `vault/secciones/`, `vault/insumos/`,
`info_data/` y `proposals/<run-id>/` completo están en `.gitignore`. El
comando `/propuesta-limpiar` (§Uso) archiva la corrida activa a
`proposals/<run-id>/` — **solo en disco local** — y resetea `proposal/` y
`vault/` a scaffolding limpio, sin residuos de build ni cachés, listos para
la próxima corrida.

`scripts/` (raíz) y `proposal/scripts/` son intencionalmente distintos: el
primero es tooling del repo (portabilidad de agentes Claude Code → OpenCode,
no depende de una corrida de `/propuesta`); el segundo es específico del
build LaTeX/DOCX de una corrida (compilación de diagramas TikZ, export a
Word) y solo tiene sentido una vez `proposal/sections/` existe.

## Inicio rápido: proyecto portable

El entrypoint recomendado para corridas reales es `marco init`, que crea
una carpeta de proyecto autocontenida y copiable:

```bash
marco init ~/propuestas/mi-proyecto --title "Título del proyecto"
```

**Cheat-sheet de comandos:**

```bash
marco init <dir> --title "Título de la propuesta"
marco status <dir>
marco upgrade <dir>
marco --help
```

Para el detalle completo de flags, entorno, manifest y flujo, ver
[`docs/marco-cli.md`](docs/marco-cli.md).

> El flujo de trabajar en la raíz del monorepo queda como **demo / dev kit
> workspace**; para corridas reales usá `marco init`.

## Uso

**Flujo stepped (recomendado):**

```text
/propuesta-init                  # drop zones: tdr draft background doc-secciones ideas
# completá ideas/idea.md (opcional si pasás la idea en el comando)
/propuesta-analizar [idea]       # intake; idea desde args o ideas/; para antes de scoping
/propuesta-continuar             # una unidad por vez; imprime el siguiente comando
```

**Flujo auto (una sesión):** `/propuesta-auto [idea]` o alias `/propuesta [idea]`
— pipeline completo con gates en la misma sesión interactiva. La idea también
puede venir de `ideas/idea.md` si omitís args.

Los mismos comandos se generan para OpenCode (`.opencode/commands/`) y pi
(`.pi/prompts/` → `/propuesta-*`). Regenerar tras editar Claude:

```bash
python3 scripts/gen-opencode.py && python3 scripts/gen-pi.py
```

Requieren sesión **interactiva** (gates). **No** hay run unattended sin gates
ni soporte Codex. En pi: confiá el proyecto para cargar `.pi/`; los roles son
archivos de referencia (sin subagentes anidados).

| Comando | Rol |
|---------|-----|
| `/propuesta-init` | Zonas `tdr/` `draft/` `background/` `doc-secciones/` `ideas/` |
| `/propuesta-analizar` | Intake + clasificación (idea: args o `ideas/`) |
| `/propuesta-continuar` | Siguiente unidad del pipeline |
| `/propuesta-auto` / `/propuesta` | Pipeline completo |
| `/propuesta-limpiar` | Archivar y resetear workspace |

**Guía de operador:** [`docs/usage-modes.md`](docs/usage-modes.md) (modos TDR /
borrador, stepped vs auto, shell CLIs). “Continuar” un **borrador** (draft-base)
= semilla + reescritura completa — no reanudar `proposal/sections/` a medias.
`/propuesta-continuar` es el **siguiente paso del pipeline**, no mid-run resume
arbitrario.

`/propuesta-limpiar` archiva la corrida activa a `proposals/<run-id>/` (disco
local) y deja `proposal/` + `vault/` limpios (incluye estado `next_step`).

**No hay un CLI de producto** que reemplace los slash commands. Compilación
PDF/DOCX: `proposal/build.sh` (guía §3).

## Flujo del pipeline

Diagrama tipo BPMN del pipeline completo (fases, compuertas de aprobación y
los tres grafos de conocimiento transversales). Fuente editable y notas de
lectura en [`docs/pipeline-flow.md`](docs/pipeline-flow.md).

![Flujo del pipeline /propuesta](docs/pipeline-flow.svg)

## Dependencias

- **Claude Code** — runtime canónico (`.claude/agents/`, `.claude/commands/`).
- **OpenCode** (opcional) — `python3 scripts/gen-opencode.py` → `.opencode/`;
  allow-list `permission.task` en tu `opencode.json` (ver docstring del
  generador). Sesión interactiva para gates.
- **pi** (opcional) — `python3 scripts/gen-pi.py` → `.pi/prompts` + role cards
  + skill; confiá el proyecto en pi para cargar `.pi/`. Sesión interactiva
  para gates; sin subagentes anidados (el primario lee
  `.pi/references/agents/`).
- **engram** (`brew install gentleman-programming/tap/engram`) — memoria persistente; requerido porque el servidor MCP `engram` de `.mcp.json` invoca este binario directamente.
- **gentle-ai** (recomendado, `brew install gentleman-programming/tap/gentle-ai`) — orquestación del workflow SDD (`/sdd-*`), registro de skills y asignación de modelos por fase.
- LaTeX (pdflatex + bibtex, estilo `natbib`/`apalike`) para compilar `proposal/main.tex`.
- MCP servers usados por los agentes de propuesta: OpenAlex, Crossref, Semantic
  Scholar, PubMed, arXiv, Context7, Consensus. Ver `REQUIREMENTS.md` §1 para el
  detalle de instalación y §3 para el detalle de paquetes; `.mcp.json` registra
  los servidores activos de este proyecto.

## Compilar la propuesta

`proposal/main.tex` no está committeado: se genera en la Fase 7 (ensamble) de
`/propuesta`. Ejecuta el pipeline hasta completarla y luego:

```bash
cd proposal
./build.sh           # o: ./build.sh --manual (pdflatex→bibtex→pdflatex×2)
./build.sh --docx    # exporta a Word vía pandoc
```
