# Marco de Redacción de Propuestas de Investigación en IA

Framework multi-agente que produce propuestas de investigación en IA en
**español**, como LaTeX, en `proposal/`. **Runtime canónico: Claude Code.**
El asistente primario despacha 8 subagentes de dominio — `investigador`,
`redactor`, `revisor`, `bibliografo-propuesta`, `insumos-observador`,
`disenador-tikz`, `tikz-optimizer`, `revisor-figuras` — usando el comando
`/propuesta` (`.claude/commands/propuesta.md`), siguiendo la referencia
canónica del pipeline en `.claude/agents/coordinador-propuesta.md`, avanzando
por fases con puertas de revisión (gates).

## Estructura

```
.
├── AGENTS.md                        # Playbook / reglas globales
├── guiaProyectosIA_Agente.md        # Guía autoritativa sección por sección
├── .mcp.json                        # Config de MCP servers
├── info_data/                       # Insumos del usuario (PDFs, papers)
├── .claude/
│   ├── agents/                      # 9 subagentes de propuesta
│   └── commands/
│       └── propuesta.md             # Comando /propuesta
└── proposal/                        # Salida LaTeX
    ├── main.tex
    ├── refs.bib
    ├── estado_propuesta.md
    └── sections/                    # .tex por sección (generados por agentes)
```

## Uso

Ejecuta el comando `/propuesta <idea>` en Claude Code. El asistente primario
despacha la Fase 0 (`insumos-observador` ingiere insumos) y avanza fase por
fase, deteniéndose en cada gate para aprobación del usuario.

## Dependencias

- **Claude Code** — runtime del pipeline (`.claude/agents/`, `.claude/commands/propuesta.md`).
- LaTeX (pdflatex + biber) para compilar `proposal/main.tex`.
- MCP servers usados por los agentes de propuesta: OpenAlex, Crossref, Semantic
  Scholar, PubMed, arXiv, Context7, Consensus. Ver `REQUIREMENTS.md` §3 para el
  detalle de paquetes; `.mcp.json` registra los servidores activos de este
  proyecto.

## Compilar la propuesta

```bash
cd proposal
pdflatex main && biber main && pdflatex main && pdflatex main
```
