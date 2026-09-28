#!/usr/bin/env bash
# init-run.sh — Scaffold one /propuesta run folder under proposals/<run-id>/.
#
# Everything a run touches lives inside that one folder, split into exactly four
# subfolders so nothing ends up loose at the run root:
#
#   insumos/      user inputs: terms of reference (TDR), papers, base proposals,
#                 reference documents. The only folder the user fills by hand.
#   artefactos/   every artifact the pipeline generates that is not a LaTeX
#                 source: run state, structured inputs, the TDR-adjusted guide,
#                 the phase/gate log, the scoping corpus, and the Obsidian vault
#                 mirror.
#   grafos/       codebase-memory graph reports produced during the writing flow.
#   redaccion/    the LaTeX project: main.tex, sections/, refs.bib, figures and
#                 the built main.pdf / main.docx, plus the build tooling.
#
# Only _run.md sits at the run root, because it describes the folder itself.
#
# redaccion/ is a copy of the repo's proposal/ skeleton, so its internal relative
# layout (sections/, logos/, templates/, scripts/) is unchanged and build.sh and
# scripts/compile_tikz.py work there without modification.
#
# Deterministic and idempotent: re-running it on an existing run folder creates
# only what is missing and never truncates an existing file. It writes nothing
# outside proposals/<run-id>/, proposals/.current-run and proposals/registry.md.
#
# Usage (from anywhere; the repo root is resolved from this file's location):
#
#   scripts/init-run.sh <run-id> ["idea breve"]   # create/refresh + activate
#   scripts/init-run.sh --print-run-id            # print the active run-id
#   scripts/init-run.sh --no-activate <run-id>    # create without activating
#
# <run-id> must match [a-z0-9-]+ and by convention is <YYYY-MM>-<slug>
# (e.g. 2026-09-siun-alianzas). The active run-id is stored in
# proposals/.current-run, which is what the /propuesta dispatcher reads to
# resolve RUN_ROOT.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNS_DIR="$REPO_ROOT/proposals"
POINTER="$RUNS_DIR/.current-run"
REGISTRY="$RUNS_DIR/registry.md"
SKELETON="$REPO_ROOT/proposal"

die() { printf 'error: %s\n' "$1" >&2; exit 1; }

activate=1
run_id=""
idea=""

while [ $# -gt 0 ]; do
  case "$1" in
    --print-run-id)
      [ -f "$POINTER" ] || die "no active run: $POINTER does not exist (run scripts/init-run.sh <run-id>)"
      tr -d '[:space:]' < "$POINTER"
      printf '\n'
      exit 0
      ;;
    --no-activate) activate=0; shift ;;
    -h|--help) sed -n '2,37p' "${BASH_SOURCE[0]}"; exit 0 ;;
    --*) die "unknown option: $1" ;;
    *)
      if [ -z "$run_id" ]; then run_id="$1"; else idea="$1"; fi
      shift
      ;;
  esac
done

[ -n "$run_id" ] || die "missing <run-id> (usage: scripts/init-run.sh <run-id> [\"idea breve\"])"
printf '%s' "$run_id" | grep -Eq '^[a-z0-9-]+$' \
  || die "invalid run-id '$run_id': allowed characters are [a-z0-9-]"

RUN_ROOT="$RUNS_DIR/$run_id"
existed=0
[ -d "$RUN_ROOT" ] && existed=1

# --- the four subfolders --------------------------------------------------
for d in \
  "$RUN_ROOT" \
  "$RUN_ROOT/insumos" \
  "$RUN_ROOT/artefactos" \
  "$RUN_ROOT/artefactos/pipeline" \
  "$RUN_ROOT/artefactos/scoping" \
  "$RUN_ROOT/artefactos/scoping/papers" \
  "$RUN_ROOT/artefactos/vault" \
  "$RUN_ROOT/artefactos/vault/secciones" \
  "$RUN_ROOT/artefactos/vault/insumos" \
  "$RUN_ROOT/grafos" \
  "$RUN_ROOT/redaccion" \
  "$RUN_ROOT/redaccion/sections" \
; do
  mkdir -p "$d"
done

# --- LaTeX skeleton, copied (never symlinked: the run must stay
#     self-contained and readable after the framework moves on) -------------
for item in build.sh scripts logos templates; do
  src="$SKELETON/$item"
  dest="$RUN_ROOT/redaccion/$item"
  [ -e "$src" ] || die "framework skeleton missing: $src"
  if [ ! -e "$dest" ]; then
    cp -R "$src" "$dest"
  fi
done

# --- empty artifacts the dispatcher fills in -------------------------------
for f in \
  "$RUN_ROOT/artefactos/estado_propuesta.md" \
  "$RUN_ROOT/artefactos/insumos.md" \
  "$RUN_ROOT/redaccion/refs.bib" \
; do
  [ -e "$f" ] || : > "$f"
done

for f in \
  "$RUN_ROOT/insumos/.gitkeep" \
  "$RUN_ROOT/grafos/.gitkeep" \
  "$RUN_ROOT/artefactos/vault/secciones/.gitkeep" \
  "$RUN_ROOT/artefactos/vault/insumos/.gitkeep" \
; do
  [ -e "$f" ] || : > "$f"
done

# --- codebase-memory ignore file for the vault index ----------------------
# Only the vault needs one: the papers corpus root (artefactos/scoping/papers)
# holds nothing but papers, and the graph reports live in grafos/, outside both
# corpora. Note that `!path` negations here would NOT re-include a .gitignore'd
# path, which is why each corpus is always indexed as its own repo_path root.
if [ ! -e "$RUN_ROOT/artefactos/vault/.cbmignore" ]; then
  cat > "$RUN_ROOT/artefactos/vault/.cbmignore" <<'EOF'
# codebase-memory ignore file for the vault index (<run-id>-vault).
# Indexed as its own root:
#   index_repository(repo_path="<RUN_ROOT>/artefactos/vault")
.obsidian/
.obsidian/**
EOF
fi

# --- run manifest ----------------------------------------------------------
today="$(date +%Y-%m-%d)"
if [ ! -e "$RUN_ROOT/_run.md" ]; then
  cat > "$RUN_ROOT/_run.md" <<EOF
# Corrida \`$run_id\`

| Campo | Valor |
|---|---|
| run-id | \`$run_id\` |
| creada | $today |
| cerrada | — |
| estado | activa |
| idea | ${idea:-—} |
| RUN_ROOT | \`proposals/$run_id/\` |

Este es el único archivo en la raíz de la corrida; todo lo demás vive en una de
las cuatro subcarpetas:

| Subcarpeta | Qué contiene | Quién la llena |
|---|---|---|
| \`insumos/\` | TDR, papers, propuestas base, documentos de referencia | el usuario |
| \`artefactos/\` | \`estado_propuesta.md\`, \`insumos.md\`, \`guia_ajustada_TDR.md\`, \`pipeline/\`, \`scoping/\`, \`vault/\` | el pipeline |
| \`grafos/\` | reportes de \`codebase-memory\` (\`papers-graph-report.md\`, \`vault-graph-report.md\`) | el dispatcher |
| \`redaccion/\` | \`main.tex\`, \`sections/\`, \`refs.bib\`, \`main.pdf\`, \`main.docx\`, \`build.sh\`, \`scripts/\`, \`logos/\`, \`templates/\` | el pipeline |

Nada de esto se versiona (\`.gitignore\`: \`proposals/*/\`); solo
\`proposals/registry.md\` lo hace.

Índices de \`codebase-memory\` de esta corrida: \`$run_id-papers\`
(\`artefactos/scoping/papers\`) y \`$run_id-vault\` (\`artefactos/vault\`).
EOF
fi

# --- registry row ----------------------------------------------------------
if [ -f "$REGISTRY" ] && ! grep -q "\`$run_id\`" "$REGISTRY"; then
  printf '| `%s` | %s | — | activa | %s | `proposals/%s/` (local) | — |\n' \
    "$run_id" "$today" "${idea:-—}" "$run_id" >> "$REGISTRY"
fi

# --- activate --------------------------------------------------------------
if [ "$activate" -eq 1 ]; then
  printf '%s\n' "$run_id" > "$POINTER"
fi

if [ "$existed" -eq 1 ]; then
  printf 'refreshed existing run folder: proposals/%s/\n' "$run_id"
else
  printf 'created run folder: proposals/%s/\n' "$run_id"
fi
[ "$activate" -eq 1 ] && printf 'active run (proposals/.current-run): %s\n' "$run_id"
printf 'RUN_ROOT: proposals/%s/  (insumos/ artefactos/ grafos/ redaccion/)\n' "$run_id"
exit 0
