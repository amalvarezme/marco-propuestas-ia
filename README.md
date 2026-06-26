# Marco de Redacción de Propuestas de Investigación en IA

Framework multi-agente (estilo oh-my-opencode-slim) que produce propuestas de
investigación en IA en **español**, como LaTeX, en `proposal/`. El plugin
**oh-my-opencode-slim** aporta un panthéon de agentes generales (primario por
defecto: `orchestrator`). La capa de propuesta aporta subagentes de dominio —
`investigador`, `redactor`, `revisor`, `bibliografo-propuesta`,
`insumos-observador`, `diseñador-tikz`, `tikz-optimizer` — coordinados por el
subagente **`coordinador-propuesta`**, avanzando por fases con puertas de
revisión (gates).

## Estructura

```
.
├── AGENTS.md                        # Playbook / reglas globales
├── guiaProyectosIA_Agente.md        # Guía autoritativa sección por sección
├── opencode.jsonc                   # Config opencode + plugin OMO-slim-proyect + MCP servers
├── info_data/                       # Insumos del usuario (PDFs, papers)
├── proposal/                        # Salida LaTeX
│   ├── main.tex
│   ├── refs.bib
│   ├── estado_propuesta.md
│   └── sections/                    # .tex por sección (generados por agentes)
└── .opencode/
    ├── oh-my-opencode-slim.jsonc    # Configuración OMO-slim-proyect (presets, observer on)
    ├── agents/                      # Subagentes de propuesta + tikz-optimizer
    └── command/propuesta.md         # Comando /propuesta
```

## Uso

Ejecuta el comando `/propuesta <idea>` en opencode. El `orchestrator` delega
al subagente `coordinador-propuesta`, que despacha la Fase 0
(`insumos-observador` ingiere insumos) y avanza fase por fase, deteniéndose en
cada gate para aprobación del usuario.

## Dependencias

- **opencode** con el plugin **oh-my-opencode-slim** (registrado en
  `opencode.jsonc`). El agente primario por defecto es `orchestrator` (presets
  `opencode-go` / `openai` en `.opencode/oh-my-opencode-slim.jsonc`).
- LaTeX (pdflatex + biber) para compilar `proposal/main.tex`.
- MCP servers (free, no paid API): OpenAlex, Crossref, Semantic Scholar,
  PubMed, arXiv, Context7.

### Puesta en marcha (clonar y usar)

```bash
# 1) Materializa el plugin vendored (pinned en .opencode/package.json a 2.0.5).
#    Esto crea .opencode/node_modules/oh-my-opencode-slim/ (gitignored) — el
#    panthéon se carga desde ahí, sin fetch de red en cada arranque.
npm install --prefix .opencode --no-audit --no-fund

# 2) (Opcional, solo la primera vez) genera la config global del plugin y las
#    skills del panthéon si tu máquina no las tiene aún. No sobreescribe
#    .opencode/oh-my-opencode-slim.jsonc ya presente.
bunx oh-my-opencode-slim@2.0.5 install --preset=opencode-go --no-tui --skills=yes

# 3) Exporta el flag de background-subagents (orquestación V2 por defecto).
export OPENCODE_EXPERIMENTAL_BACKGROUND_SUBAGENTS=true   # o añade a ~/.bashrc

# 4) Autentica el proveedor opencode-go (u otro) y refresca modelos.
opencode auth login && opencode models --refresh

# 5) Verifica el panthéon y los subagentes de propuesta en opencode:
#    ping all agents
```

> Nota: si `bun` no está disponible, usa `npx oh-my-opencode-slim@2.0.5 install ...`.
> El plugin está **vendored** (pin en `.opencode/package.json`, `autoUpdate: false`
> en `.opencode/oh-my-opencode-slim.jsonc`) para que un clon obtenga la versión
> exacta del panthéon sin depender del cache de opencode ni de red en arranque.

## Compilar la propuesta

```bash
cd proposal
pdflatex main && biber main && pdflatex main && pdflatex main
```

Opencode plugin:
- `oh-my-opencode-slim` (registrado en `opencode.jsonc`; config en
  `.opencode/oh-my-opencode-slim.jsonc`). Las skills del panthéon (`deepwork`,
  `reflect`, `worktrees`, `codemap`, `clonedeps`, `oh-my-opencode-slim`) se
  instalan con el comando `bunx ... install --skills=yes` del paso 1.