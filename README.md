# Marco de Redacción de Propuestas de Investigación en IA

Framework multi-agente que produce propuestas de investigación en IA en
**español**, como LaTeX, en `proposal/`. **Runtime canónico: Claude Code.**
El asistente primario despacha 9 subagentes de dominio — `investigador`,
`redactor`, `revisor`, `bibliografo-propuesta`, `presupuestador`,
`insumos-observador`, `disenador-tikz`, `tikz-optimizer`, `revisor-figuras` —
usando el comando `/propuesta` (`.claude/commands/propuesta.md`), siguiendo la
referencia canónica del pipeline en `.claude/agents/coordinador-propuesta.md`
(el 10º archivo de `.claude/agents/`, no se despacha como subagente sino que
documenta el pipeline), avanzando por fases con puertas de revisión (gates).

## Estructura

```
.
├── AGENTS.md                        # Playbook / reglas globales
├── guiaProyectosIA_Agente.md        # Guía autoritativa sección por sección
├── .mcp.json                        # Config de MCP servers
├── info_data/                       # Insumos del usuario (vacío entre corridas)
├── .claude/
│   ├── agents/                      # 10 archivos: 9 subagentes + coordinador-propuesta
│   └── commands/
│       └── propuesta.md             # Comando /propuesta
└── proposal/                        # Framework de salida LaTeX
    ├── build.sh                     # Compilación PDF/DOCX
    ├── scripts/                     # compile_tikz.py, prep_docx.py
    ├── logos/                       # Logos institucionales
    ├── templates/reference.docx     # Plantilla pandoc (export DOCX)
    │   # Generados por cada corrida de /propuesta (no committeados):
    └── ...                         #   main.tex, refs.bib, sections/, estado_propuesta.md
```

## Uso

Ejecuta el comando `/propuesta <idea>` en Claude Code. El asistente primario
despacha la Fase 0 (`insumos-observador` ingiere insumos) y avanza fase por
fase, deteniéndose en cada gate para aprobación del usuario.

## Flujo del pipeline

Diagrama tipo BPMN del pipeline completo (fases, compuertas de aprobación y
los tres grafos de conocimiento transversales). Fuente editable y notas de
lectura en [`docs/pipeline-flow.md`](docs/pipeline-flow.md).

![Flujo del pipeline /propuesta](docs/pipeline-flow.svg)

## Dependencias

- **Claude Code** — runtime del pipeline (`.claude/agents/`, `.claude/commands/propuesta.md`).
- LaTeX (pdflatex + bibtex, estilo `natbib`/`apalike`) para compilar `proposal/main.tex`.
- MCP servers usados por los agentes de propuesta: OpenAlex, Crossref, Semantic
  Scholar, PubMed, arXiv, Context7, Consensus. Ver `REQUIREMENTS.md` §3 para el
  detalle de paquetes; `.mcp.json` registra los servidores activos de este
  proyecto.

## Compilar la propuesta

`proposal/main.tex` no está committeado: se genera en la Fase 7 (ensamble) de
`/propuesta`. Ejecuta el pipeline hasta completarla y luego:

```bash
cd proposal
./build.sh           # o: ./build.sh --manual (pdflatex→bibtex→pdflatex×2)
./build.sh --docx    # exporta a Word vía pandoc
```
