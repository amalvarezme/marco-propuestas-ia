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
| **engram** | 1.18+ | Persistent memory MCP server (required: `.mcp.json`'s `engram` server invokes this binary directly) | `brew install gentleman-programming/tap/engram` |
| **gentle-ai** (recommended) | 1.43+ | SDD workflow orchestration, skill registry, model-assignment dispatch for `/sdd-*` commands | `brew install gentleman-programming/tap/gentle-ai` |
| **OpenCode** (optional) | — | Secondary runtime for `.opencode/agents/` + `.opencode/commands/propuesta.md` (generated from `.claude/` via `scripts/gen-opencode.py`, stdlib-only, no new Python deps); interactive session required — gates don't work under `opencode run` headless | see [opencode.ai](https://opencode.ai) |

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

**Scope note:** every package above is consumed by the `graphify`/`graphifyy`
CLI tool itself (when it indexes PDFs/DOCX/media dropped into `info_data/` or
`vault/`) — none of the proposal-writing pipeline's own Python scripts import
them. `proposal/scripts/compile_tikz.py`, `proposal/scripts/prep_docx.py`, and
`scripts/gen-opencode.py` are stdlib-only (no third-party imports, nothing
from this file); `requirements.txt` exists entirely for the graphify/CodeGraph
tooling layer, not for the pipeline's own agents/scripts.

## 3. Node.js / MCP servers

All MCP servers run via `npx -y` (fetched on demand, no global install needed). All eight are registered as Claude Code MCP servers in `.mcp.json` (`engram`, `consensus`, and the six below); the six below are used directly by the proposal agents as Claude Code tools for literature/citation search:

| Server | npm package | Purpose |
|--------|-------------|---------|
| **arxiv** | `@cyanheads/arxiv-mcp-server` | arXiv paper search & full-text |
| **crossref** | `@botanicastudios/crossref-mcp` | DOI metadata, references, funders |
| **openalex** | `@cyanheads/openalex-mcp-server` | Scholarly catalog, citation graphs |
| **pubmed** | `@cyanheads/pubmed-mcp-server` | PubMed/PMC search, full-text, MeSH |
| **semantic scholar** | `@xbghc/semanticscholar-mcp` | Paper search, citations, recommendations |
| **context7** | `@upstash/context7-mcp` | Library documentation lookup |

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
├── requirements.txt          # Python deps (this file's companion) — graphify/CodeGraph tooling only
├── REQUIREMENTS.md           # This file
├── AGENTS.md                 # Framework playbook
├── guiaProyectosIA_Agente.md # Section-by-section writing guide
├── logos/                    # Repo/README branding logos (LabIA, UNAL, GCPDS)
├── scripts/                  # Repo tooling (NOT proposal-run-specific): gen-opencode.py +
│                              #   gen-opencode.rules.json — Claude Code → OpenCode agent-portability generator
├── .claude/                  # CANONICAL runtime — single source of truth, hand-edited
│   ├── agents/                # 10 files: 9 dispatchable subagents (investigador, redactor,
│   │                           #   insumos-observador, bibliografo-propuesta, presupuestador,
│   │                           #   revisor, disenador-tikz, revisor-figuras, tikz-optimizer)
│   │                           #   + coordinador-propuesta (canonical pipeline reference,
│   │                           #   never dispatched — Claude Code subagents can't invoke subagents)
│   └── commands/
│       └── propuesta.md      # Comando /propuesta — dispatcher real del pipeline
├── .opencode/                 # Secondary runtime — GENERATED from .claude/, never hand-edited
│   ├── agents/                 # 9 ported subagents (1:1 with .claude/agents/, no coordinador)
│   └── commands/propuesta.md   # Ported /propuesta command
├── info_data/                # User inputs (PDFs, DOCX) — vacío hasta la próxima corrida
├── vault/                     # Navigable Obsidian/Markdown mirror — visual layer only, NEVER
│   │                           #   the source of truth (that's proposal/*.tex, LaTeX)
│   ├── secciones/              # Mirrors proposal/sections/*.tex, one note per section
│   └── insumos/                # Mirrors proposal/insumos.md
├── proposals/                 # Registry + archived /propuesta runs
│   └── registry.md             # Append-only table: run-id, estado, archivo, commit
├── proposal/                 # Framework skeleton committed to git:
│   ├── build.sh              # Compilación PDF/DOCX (logos header/footer)
│   ├── scripts/               # compile_tikz.py, prep_docx.py — LaTeX/DOCX build-specific,
│   │                           #   distinct from the root-level scripts/ (repo tooling)
│   ├── logos/                 # LabIA, UNAL, GCPDS logos embedded in the built PDF
│   └── templates/reference.docx  # Plantilla pandoc para export DOCX
│   # Generados por cada corrida de /propuesta (no committeados, ver .gitignore):
│   #   main.tex, refs.bib, sections/*.tex, insumos.md, estado_propuesta.md,
│   #   guia_ajustada_TDR.md, pipeline/, scoping/
└── graphify-out/             # Knowledge graph outputs (gitignored)
```
