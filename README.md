# Marco de Redacción de Propuestas de Investigación en IA

Framework multi-agente (estilo oh-my-opencode-slim) que produce propuestas de
investigación en IA en **español**, como LaTeX, en `proposal/`. Un
**Orquestador** coordina especialistas — `investigador`, `redactor`,
`revisor`, `bibliotecario`, `observador`, `diseñador` — avanzando por fases con
puertas de revisión (gates).

## Estructura

```
.
├── AGENTS.md                        # Playbook / reglas globales
├── guiaProyectosIA_Agente.md        # Guía autoritativa sección por sección
├── secciones_subsecciones_propuesta.md  # (histórico, superseded)
├── opencode.jsonc                   # Configuración opencode + MCP servers
├── info_data/                       # Insumos del usuario (PDFs, papers)
├── proposal/                        # Salida LaTeX
│   ├── main.tex
│   ├── refs.bib
│   ├── estado_propuesta.md
│   └── sections/                    # .tex por sección (generados por agentes)
└── .opencode/
    ├── agents/                      # Definiciones de agentes
    └── command/propuesta.md         # Comando /propuesta
```

## Uso

Ejecuta el comando `/propuesta <idea>` en opencode. El Orquestador despacha
la Fase 0 (Observador ingiere insumos) y avanza fase por fase, deteniéndose en
cada gate para aprobación del usuario.

## Dependencias

- [opencode](https://opencode.ai) con el agente `orquestador` por defecto.
- LaTeX (pdflatex + biber) para compilar `proposal/main.tex`.
- MCP servers (free, no paid API): OpenAlex, Crossref, Semantic Scholar,
  PubMed, arXiv, Context7.

## Compilar la propuesta

```bash
cd proposal
pdflatex main && biber main && pdflatex main && pdflatex main
```