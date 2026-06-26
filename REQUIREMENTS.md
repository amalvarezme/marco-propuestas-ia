# Requirements — AI Research Proposal Writing Framework

All dependencies needed to run the multi-agent framework, build the knowledge graph, and compile the LaTeX proposal.

## 1. System tools

| Tool | Min version | Purpose | Install |
|------|-------------|---------|---------|
| **Python** | 3.11+ | graphify, scripting | `brew install python@3.11` |
| **uv** | 0.11+ | Python package manager (recommended) | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| **Node.js** | 20+ | MCP servers via npx | `brew install node` |
| **npm / npx** | 10+ | MCP server fetching | bundled with Node |
| **TeX Live** | 2024+ | LaTeX compilation (pdflatex + biber) | `brew install --cask mactex` |
| **git** | 2.40+ | Version control | `brew install git` |
| **opencode** | 1.17+ | Agent orchestration runtime | `npm install -g opencode-ai` |
| **oh-my-opencode-slim** | 2.0.5 (pinned) | Panthéon de agentes generales (orchestrator, oracle, librarian, explorer, designer, fixer, observer, council). **Vendored** en `.opencode/package.json`; cargado desde `.opencode/node_modules/oh-my-opencode-slim/dist/index.js` | `npm install --prefix .opencode` (regenera `node_modules` gitignored) |
| **bun** (o `npx`) | 1.1+ | Instalador del plugin OMO-slim | `curl -fsSL https://bun.sh \| bash` |

## 2. Python packages (`requirements.txt`)

Install:
```bash
uv tool install --upgrade graphifyy
pip install -r requirements.txt
```

Core:
- `graphifyy>=0.8.41` — knowledge graph extraction, clustering, visualization
- `networkx>=3.4` — graph data structures
- `numpy>=1.21` — numerical ops
- `rapidfuzz>=3.0` — fuzzy string matching
- `tree-sitter` + 16 language grammars — AST extraction for code files

Optional extras (used in this project):
- `pypdf` + `markdownify` — PDF parsing (convocatoria, papers)
- `python-docx` — DOCX parsing (Anexo 2 proposal)
- `graspologic` — Leiden community detection
- `matplotlib` — SVG graph export
- `faster-whisper` + `yt-dlp` — video/audio transcription
- `watchdog` — `--watch` auto-rebuild mode

## 3. Node.js / MCP servers

All MCP servers run via `npx -y` (fetched on demand, no global install needed). Configured in `opencode.jsonc`:

| Server | npm package | Purpose |
|--------|-------------|---------|
| **arxiv** | `@cyanheads/arxiv-mcp-server` | arXiv paper search & full-text |
| **crossref** | `@cyanheads/crossref-mcp-server` | DOI metadata, references, funders |
| **openalex** | `@cyanheads/openalex-mcp-server` | Scholarly catalog, citation graphs |
| **pubmed** | `@cyanheads/pubmed-mcp-server` | PubMed/PMC search, full-text, MeSH |
| **semantic scholar** | `@xbghc/semanticscholar-mcp` | Paper search, citations, recommendations |
| **context7** | (remote, no install) | Library documentation lookup |

opencode plugin:
- `@opencode-ai/plugin@1.17.11` — in `.opencode/package.json` (plugin SDK types)
- `oh-my-opencode-slim@2.0.5` — el panthéon de agentes generales, **vendored**
  (pin en `.opencode/package.json`, `autoUpdate: false`). Cargado desde
  `.opencode/node_modules/oh-my-opencode-slim/dist/index.js` (regenerado por
  `npm install --prefix .opencode`). Configurado por proyecto en
  `.opencode/oh-my-opencode-slim.jsonc` (preset `opencode-go`, observer
  habilitado). La primera vez, genera la config global y las skills del panthéon
  con `bunx oh-my-opencode-slim@2.0.5 install --preset=opencode-go --no-tui --skills=yes`.

## 4. LaTeX packages (TeX Live)

All loaded in `proposal/main.tex`. Install via `tlmgr install <pkg>` or MacTeX/full:

| Package | Collection | Purpose |
|---------|-----------|---------|
| `inputenc` | latex-base | UTF-8 input |
| `fontenc` | latex-base | T1 font encoding |
| `babel` (spanish, es-tabla) | babel-spanish | Spanish hyphenation + tabla naming |
| `geometry` | geometry | Page margins (2.5cm) |
| `graphicx` | graphics | Logo embedding (footer) |
| `amsmath` | amsmath | Math environments |
| `amssymb` | amsfonts | Math symbols (\bigstar) |
| `booktabs` | booktabs | Professional tables |
| `tabularx` | tools | Auto-width table columns |
| `longtable` | tools | Multi-page tables |
| `tikz` | pgf | Diagrams (arbol, metodológico) |
| `pgfgantt` | pgfgantt | Gantt chart |
| `hyperref` | hyperref | Clickable cross-references |
| `url` | url | URL formatting |
| `csquotes` | csquotes | Quote environments |
| `fancyhdr` | fancyhdr | Footer with institutional logos |
| `biblatex` (style=ieee, backend=biber) | biblatex + biber | IEEE-style bibliography |
| `cm-super` | cm-super | T1-compatible Computer Modern fonts (Spanish) |

Compile sequence:
```bash
cd proposal
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

## 5. opencode skills

| Skill | Source | Trigger |
|-------|--------|---------|
| **graphify** | `~/.claude/skills/graphify/SKILL.md` | `/graphify` |
| **ponytail** | `~/.cache/opencode/packages/@dietrichgebert/ponytail@latest/` | `ponytail` / lazy mode |
| **customize-opencode** | built-in | opencode config editing |

Ponytail is a cached opencode package — no pip install. It auto-loads when triggered.
Graphify is a Claude skill file + the `graphifyy` Python package (in `requirements.txt`).

## 6. Environment variables

| Variable | Required by | Description |
|----------|-------------|-------------|
| `CONTACT_EMAIL` | openalex, crossref, pubmed MCP | Polite-pool access (set in shell or `.env`) |
| `GEMINI_API_KEY` | graphify (optional) | Enables Gemini for semantic extraction |
| `GOOGLE_API_KEY` | graphify (optional) | Alternative to GEMINI_API_KEY |
| `CROSSREF_MAILTO` | crossref MCP | Polite-pool (falls back to CONTACT_EMAIL) |
| `OPENCODE_EXPERIMENTAL_BACKGROUND_SUBAGENTS` | oh-my-opencode-slim V2 | `true` habilita la orquestación scheduler-first (background subagents) |

## 7. Project structure

```
.
├── requirements.txt          # Python deps (this file's companion)
├── REQUIREMENTS.md           # This file
├── AGENTS.md                 # Framework playbook
├── guiaProyectosIA_Agente.md # Section-by-section writing guide
├── opencode.jsonc            # MCP server config + plugin OMO-slim + default_agent
├── .opencode/
│   ├── package.json          # opencode plugin deps
│   ├── oh-my-opencode-slim.jsonc  # OMO-slim config (presets opencode-go/openai)
│   ├── agents/               # Subagentes de propuesta + tikz-optimizer
│   └── command/              # Comando /propuesta
├── info_data/                # User inputs (PDFs, DOCX)
├── proposal/
│   ├── main.tex              # LaTeX assembly (footer with logos)
│   ├── refs.bib              # BibTeX (87 entries, IEEE)
│   ├── sections/             # One .tex per section + 3 TikZ diagrams
│   ├── logos/                # LabIA, UNAL, GCPDS logos
│   ├── insumos.md            # Shared context digest (Observador output)
│   └── estado_propuesta.md   # Phase tracker
└── graphify-out/             # Knowledge graph outputs (gitignored)
```
