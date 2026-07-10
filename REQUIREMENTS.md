# Requirements — AI Research Proposal Writing Framework

All dependencies needed to run the multi-agent framework, build the knowledge graph, and compile the LaTeX proposal.

## 1. System tools

| Tool | Min version | Purpose | Install |
|------|-------------|---------|---------|
| **Python** | 3.11+ | graphify, scripting | `brew install python@3.11` |
| **uv** | 0.11+ | Python package manager (recommended) | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| **Node.js** | 20+ | MCP servers via npx | `brew install node` |
| **npm / npx** | 10+ | MCP server fetching | bundled with Node |
| **TeX Live** | 2024+ | LaTeX compilation (pdflatex + bibtex) | `brew install --cask mactex` |
| **git** | 2.40+ | Version control | `brew install git` |

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

All MCP servers run via `npx -y` (fetched on demand, no global install needed). Registered as Claude Code MCP servers — see `.mcp.json` for this project's currently active servers (`engram`, `consensus`); the servers below are used by the proposal agents as Claude Code tools:

| Server | npm package | Purpose |
|--------|-------------|---------|
| **arxiv** | `@cyanheads/arxiv-mcp-server` | arXiv paper search & full-text |
| **crossref** | `@cyanheads/crossref-mcp-server` | DOI metadata, references, funders |
| **openalex** | `@cyanheads/openalex-mcp-server` | Scholarly catalog, citation graphs |
| **pubmed** | `@cyanheads/pubmed-mcp-server` | PubMed/PMC search, full-text, MeSH |
| **semantic scholar** | `@xbghc/semanticscholar-mcp` | Paper search, citations, recommendations |
| **context7** | (remote, no install) | Library documentation lookup |

## 4. LaTeX packages (TeX Live)

All loaded in `proposal/main.tex`. Install via `tlmgr install <pkg>` or MacTeX/full:

| Package | Collection | Purpose |
|---------|-----------|---------|
| `inputenc` | latex-base | UTF-8 input |
| `fontenc` | latex-base | T1 font encoding |
| `babel` (spanish, es-tabla) | babel-spanish | Spanish hyphenation + tabla naming |
| `geometry` | geometry | Page margins (2.5cm) |
| `graphicx` | graphics | Logo embedding (header/footer) |
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
| `fancyhdr` | fancyhdr | Split header/footer with institutional logos (UNAL header; GCPDS/LabIA footer) |
| `natbib` (style=apalike, backend=bibtex) | natbib + apalike.bst | Citas autor-año APA (ver guiaProyectosIA_Agente.md §16) |
| `cm-super` | cm-super | T1-compatible Computer Modern fonts (Spanish) |

Compile sequence (or just run `./build.sh` / `./build.sh --manual`):
```bash
cd proposal
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## 5. Claude Code skills

| Skill | Source | Trigger |
|-------|--------|---------|
| **graphify** | `~/.claude/skills/graphify/SKILL.md` | `/graphify` |

Graphify is a Claude Code skill file + the `graphifyy` Python package (in `requirements.txt`).

## 6. Environment variables

| Variable | Required by | Description |
|----------|-------------|-------------|
| `CONTACT_EMAIL` | openalex, crossref, pubmed MCP | Polite-pool access (set in shell or `.env`) |
| `GEMINI_API_KEY` | graphify (optional) | Enables Gemini for semantic extraction |
| `GOOGLE_API_KEY` | graphify (optional) | Alternative to GEMINI_API_KEY |
| `CROSSREF_MAILTO` | crossref MCP | Polite-pool (falls back to CONTACT_EMAIL) |

## 7. Project structure

```
.
├── requirements.txt          # Python deps (this file's companion)
├── REQUIREMENTS.md           # This file
├── AGENTS.md                 # Framework playbook
├── guiaProyectosIA_Agente.md # Section-by-section writing guide
├── .claude/                  # CANONICAL runtime — single source of truth
│   ├── agents/               # 10 subagentes de propuesta (coordinador-propuesta,
│   │                         #   investigador, redactor, insumos-observador,
│   │                         #   bibliografo-propuesta, presupuestador, revisor,
│   │                         #   disenador-tikz, revisor-figuras, tikz-optimizer)
│   └── commands/
│       └── propuesta.md      # Comando /propuesta — dispatcher real del pipeline
├── info_data/                # User inputs (PDFs, DOCX) — vacío hasta la próxima corrida
├── proposal/                 # Framework skeleton committed to git:
│   ├── build.sh              # Compilación PDF/DOCX (logos header/footer)
│   ├── scripts/               # compile_tikz.py, prep_docx.py
│   ├── logos/                 # LabIA, UNAL, GCPDS logos
│   └── templates/reference.docx  # Plantilla pandoc para export DOCX
│   # Generados por cada corrida de /propuesta (no committeados, ver .gitignore):
│   #   main.tex, refs.bib, sections/*.tex, insumos.md, estado_propuesta.md,
│   #   guia_ajustada_TDR.md, pipeline/, scoping/
└── graphify-out/             # Knowledge graph outputs (gitignored)
```
