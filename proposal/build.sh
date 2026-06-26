#!/usr/bin/env bash
#
# build.sh — Compila la propuesta de investigación (LaTeX + BibLaTeX/Biber).
#
# Uso:
#   ./build.sh              Compilación normal (latexmk)
#   ./build.sh --clean      Limpia artefactos auxiliares y recompila desde cero
#   ./build.sh --clean-only Solo limpia artefactos (no compila)
#   ./build.sh --manual     Usa la secuencia manual pdflatex→biber→pdflatex×2
#   ./build.sh --watch      Recompila automáticamente al detectar cambios
#   ./build.sh --help       Muestra esta ayuda
#
# Requisitos: pdflatex, biber, latexmk (todos en PATH).
#
set -euo pipefail

# --- Configuración -----------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAIN="main.tex"
PDF="main.pdf"
ENGINE="pdflatex"
BIBENGINE="biber"

# Colores (si la terminal los soporta)
if [[ -t 1 ]]; then
  C_RED='\033[0;31m'; C_GRN='\033[0;32m'; C_YLW='\033[1;33m'
  C_BLU='\033[0;34m'; C_RST='\033[0m'
else
  C_RED=''; C_GRN=''; C_YLW=''; C_BLU=''; C_RST=''
fi

log()  { printf "${C_BLU}[build]${C_RST} %s\n" "$*"; }
ok()   { printf "${C_GRN}[ OK ]${C_RST} %s\n" "$*"; }
warn() { printf "${C_YLW}[WARN]${C_RST} %s\n" "$*"; }
err()  { printf "${C_RED}[FAIL]${C_RST} %s\n" "$*" >&2; }

# --- Artefactos auxiliares a limpiar -----------------------------------------
AUX_EXT=(
  aux bcf bbl blg fdb_latexmk fls log out run.xml toc lof lot
  nav snm vrb idx ilg ind xdv synctex.gz
)

clean_artifacts() {
  log "Limpiando artefactos auxiliares..."
  for ext in "${AUX_EXT[@]}"; do
    rm -f "${SCRIPT_DIR}"/*.${ext} 2>/dev/null || true
  done
  # latexmk también deja _minted-* y auto-* en subdirectorios
  find "${SCRIPT_DIR}" -maxdepth 2 -type f \( -name "*.aux" -o -name "*.bbl" \
    -o -name "*.bcf" -o -name "*.log" -o -name "*.out" -o -name "*.fls" \
    -o -name "*.fdb_latexmk" -o -name "*.run.xml" -o -name "*.synctex.gz" \) \
    -delete 2>/dev/null || true
  ok "Artefactos eliminados."
}

# --- Verificación de dependencias --------------------------------------------
check_deps() {
  local missing=()
  for tool in "${ENGINE}" "${BIBENGINE}"; do
    if ! command -v "${tool}" >/dev/null 2>&1; then
      missing+=("${tool}")
    fi
  done
  if [[ ${#missing[@]} -gt 0 ]]; then
    err "Faltan dependencias: ${missing[*]}"
    err "Instala TeX Live (pdflatex, biber) o MiKTeX."
    exit 1
  fi
}

# --- Compilación con latexmk (por defecto) -----------------------------------
build_latexmk() {
  log "Compilando con latexmk (${ENGINE} + ${BIBENGINE})..."
  cd "${SCRIPT_DIR}"
  latexmk \
    -f \
    -pdf \
    -pdflatex="${ENGINE} -interaction=nonstopmode -synctex=1 %O %S" \
    -bibtex \
    -shell-escape \
    "${MAIN}" 2>&1 | sed 's/^/  /' || true
  # latexmk devuelve non-zero si hay errores de LaTeX, pero el PDF puede
  # haberse generado correctamente. Verificamos el PDF, no el exit code.
  # latexmk devuelve 0 incluso con warnings; verificar que el PDF existe
  if [[ -f "${PDF}" ]]; then
    local pages
    pages=$(pdfinfo "${PDF}" 2>/dev/null | awk '/^Pages:/{print $2}' || echo "?")
    local size
    size=$(du -h "${PDF}" | cut -f1)
    ok "Compilación exitosa: ${PDF} (${pages} páginas, ${size})"
    # Reportar errores y warnings de LaTeX aunque el PDF se generara
    # Nota: grep -c imprime 0 y sale con código 1 cuando no hay coincidencias;
    # el fallback || echo 0 concatenaría otro "0\n0" y rompería la aritmética.
    local errs warns
    errs=$(grep -c '^!' "${SCRIPT_DIR}/main.log" 2>/dev/null; true)
    errs="${errs:-0}"
    warns=$(grep -c 'Warning' "${SCRIPT_DIR}/main.log" 2>/dev/null; true)
    warns="${warns:-0}"
    if [[ "${errs}" -gt 0 ]]; then
      warn "LaTeX reportó ${errs} error(es) — revisa main.log"
    fi
    if [[ "${warns}" -gt 0 ]]; then
      warn "LaTeX emitió ${warns} advertencia(s) — revisa main.log"
    fi
  else
    err "No se generó ${PDF}. Revisa los errores arriba."
    exit 1
  fi
}

# --- Compilación manual (pdflatex → biber → pdflatex × 2) --------------------
build_manual() {
  log "Compilación manual: pdflatex → ${BIBENGINE} → pdflatex × 2"
  cd "${SCRIPT_DIR}"

  log "Paso 1/4: pdflatex (pass 1 — genera .bcf)..."
  if ! ${ENGINE} -interaction=nonstopmode -synctex=1 "${MAIN}" > /dev/null 2>&1; then
    warn "pdflatex (pass 1) reportó errores. Continuando (nonstopmode)..."
  fi

  log "Paso 2/4: ${BIBENGINE} (procesa bibliografía)..."
  if ! ${BIBENGINE} "$(basename "${MAIN}" .tex)" > /dev/null 2>&1; then
    warn "biber reportó advertencias. Continuando..."
  fi

  log "Paso 3/4: pdflatex (pass 2 — incorpora bibliografía)..."
  if ! ${ENGINE} -interaction=nonstopmode -synctex=1 "${MAIN}" > /dev/null 2>&1; then
    warn "pdflatex (pass 2) reportó errores. Continuando (nonstopmode)..."
  fi

  log "Paso 4/4: pdflatex (pass 3 — resuelve referencias cruzadas)..."
  if ! ${ENGINE} -interaction=nonstopmode -synctex=1 "${MAIN}" > /dev/null 2>&1; then
    warn "pdflatex (pass 3) reportó errores. Continuando (nonstopmode)..."
  fi

  if [[ -f "${PDF}" ]]; then
    local pages
    pages=$(pdfinfo "${PDF}" 2>/dev/null | awk '/^Pages:/{print $2}' || echo "?")
    local size
    size=$(du -h "${PDF}" | cut -f1)
    ok "Compilación exitosa: ${PDF} (${pages} páginas, ${size})"
  else
    err "No se generó ${PDF}."
    exit 1
  fi
}

# --- Modo watch --------------------------------------------------------------
build_watch() {
  log "Modo watch activo (latexmk -pvc). Ctrl+C para salir."
  cd "${SCRIPT_DIR}"
  latexmk \
    -pdf \
    -pdflatex="${ENGINE} -interaction=nonstopmode -synctex=1 %O %S" \
    -bibtex \
    -shell-escape \
    -pvc \
    "${MAIN}"
}

# --- Ayuda -------------------------------------------------------------------
show_help() {
  sed -n '2,/^$/p' "${BASH_SOURCE[0]}" | sed 's/^# \?//'
}

# --- Main --------------------------------------------------------------------
main() {
  local mode="latexmk"
  local do_clean=false

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --clean)        do_clean=true ;;
      --clean-only)   clean_artifacts; exit 0 ;;
      --manual)       mode="manual" ;;
      --watch)        mode="watch" ;;
      --help|-h)      show_help; exit 0 ;;
      *) err "Opción desconocida: $1"; show_help; exit 1 ;;
    esac
    shift
  done

  check_deps

  if [[ "${do_clean}" == true ]]; then
    clean_artifacts
  fi

  case "${mode}" in
    latexmk) build_latexmk ;;
    manual)  build_manual ;;
    watch)   build_watch ;;
  esac
}

main "$@"
