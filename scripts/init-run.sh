#!/usr/bin/env bash
# init-run.sh — Scaffold one /propuesta run folder under proposals/<run-id>/.
#
# Every artifact a run produces (LaTeX sections, refs.bib, vault mirror,
# pipeline log, scoping corpus, build output) lives inside that single folder,
# so two runs never overwrite each other and archiving a run is a no-op: the
# folder IS the archive.
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
    -h|--help) sed -n '2,25p' "${BASH_SOURCE[0]}"; exit 0 ;;
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

# --- directories -----------------------------------------------------------
for d in \
  "$RUN_ROOT" \
  "$RUN_ROOT/info_data" \
  "$RUN_ROOT/proposal" \
  "$RUN_ROOT/proposal/sections" \
  "$RUN_ROOT/proposal/pipeline" \
  "$RUN_ROOT/proposal/scoping" \
  "$RUN_ROOT/proposal/scoping/papers" \
  "$RUN_ROOT/proposal/figures" \
  "$RUN_ROOT/vault" \
  "$RUN_ROOT/vault/secciones" \
  "$RUN_ROOT/vault/insumos" \
; do
  mkdir -p "$d"
done

# --- framework skeleton (copied, never symlinked: the run must stay
#     self-contained and readable after the framework moves on) -------------
for item in build.sh scripts logos templates; do
  src="$SKELETON/$item"
  dest="$RUN_ROOT/proposal/$item"
  [ -e "$src" ] || die "framework skeleton missing: $src"
  if [ ! -e "$dest" ]; then
    cp -R "$src" "$dest"
  fi
done

# --- empty artifacts the dispatcher fills in -------------------------------
for f in \
  "$RUN_ROOT/proposal/estado_propuesta.md" \
  "$RUN_ROOT/proposal/insumos.md" \
  "$RUN_ROOT/proposal/refs.bib" \
; do
  [ -e "$f" ] || : > "$f"
done

for f in \
  "$RUN_ROOT/vault/secciones/.gitkeep" \
  "$RUN_ROOT/vault/insumos/.gitkeep" \
  "$RUN_ROOT/info_data/.gitkeep" \
; do
  [ -e "$f" ] || : > "$f"
done

# --- codebase-memory ignore files (exclude noise from the two run indexes;
#     `!path` negations would NOT re-include .gitignore'd paths, which is why
#     each corpus is always indexed as its own repo_path root) --------------
if [ ! -e "$RUN_ROOT/vault/.cbmignore" ]; then
  cat > "$RUN_ROOT/vault/.cbmignore" <<'EOF'
# codebase-memory ignore file for the vault index (<run-id>-vault).
# Indexed as its own root: index_repository(repo_path="<RUN_ROOT>/vault").
.obsidian/
.obsidian/**
EOF
fi

if [ ! -e "$RUN_ROOT/proposal/scoping/.cbmignore" ]; then
  cat > "$RUN_ROOT/proposal/scoping/.cbmignore" <<'EOF'
# codebase-memory ignore file for the scoping corpus (<run-id>-papers).
# Only papers/ is the corpus; the derived reports are never part of it.
graph-report.md
graph-report-*-snapshot.md
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

Todos los artefactos de esta corrida viven bajo \`RUN_ROOT\`: \`proposal/\`
(fuente de verdad LaTeX), \`vault/\` (espejo Markdown/Obsidian),
\`info_data/\` (insumos del usuario). Nada de esto se versiona
(\`.gitignore\`: \`proposals/*/\`); solo \`proposals/registry.md\` lo hace.

Índices de \`codebase-memory\` de esta corrida:
\`$run_id-papers\` (\`proposal/scoping/papers\`) y \`$run_id-vault\` (\`vault\`).
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
printf 'RUN_ROOT: proposals/%s/\n' "$run_id"
exit 0
