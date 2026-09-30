# Feature: Fase 2 cierre — compuerta G2 (§4 estado del arte + §5 hipótesis)

## Goal

Resume the interrupted Fase 2 of the proposal run
`2026-09-tept-depresion-ia-portable` and drive it to the user-approval gate
G2, without re-authoring already-delivered content.

Authoritative run state stays in
`proposals/2026-09-tept-depresion-ia-portable/artefactos/estado_propuesta.md`
(the pipeline's own state machine). This ODD file only mirrors the remaining
sub-steps for traceability.

## Already delivered (do not re-author)

- `redaccion/sections/04_estado_arte.tex` — 5 SOTA subsections, 51 distinct
  citation keys, gate_status pending.
- `redaccion/sections/05_hipotesis.tex` — single-paragraph hypothesis,
  gate_status pending.
- `redaccion/sections/diag_estado_arte.tex` — state-of-the-art map, authored
  from the commented spec block of §4; `fig_estado_arte-1.png` + `.svg`
  already rendered by `compile_tikz.py`.

## Tasks

- [x] T1 Deterministic OVERFULL precheck for `estado_arte` (figure loop step 1)
- [x] T2 Visual audit of `fig_estado_arte-1.png` → `revisor-figuras` PASS/FAIL
- [x] T3 Prose audit of §4 and §5 → `grant-flow-auditor` (skill `estilo-natural-es`)
- [x] T4 Gate G2 → `revisor` PASS/FAIL over §4 + §5
- [x] T5 Gate artifacts: `main.tex` (+ §4, §5, estado-del-arte figure) and `./build.sh`
- [x] T6 State docs: `estado_propuesta.md`, `artefactos/pipeline/30-fase2.md`,
      `_estado.md`, vault mirrors `gate_status`
- [x] T7 Present G2 to the user for explicit approval

## Evidence

- **T1**: forechecked twice — first pass `OVERFULL: estado_arte 1 occurrence(s)
  (first: 1.51376pt too wide at diag_estado_arte.tex:84)`; after `tikz-optimizer`
  widened `ctitulo` to 4.45 cm, `OVERFULL: estado_arte 0 occurrence(s)`.
  Independently re-run by the parent, not trusted from the subagent report.
- **T2**: `revisor-figuras` PASS (scale 12/14 pt and 14/17 pt intact, centering,
  no overlaps, institutional palette, 20 intra-cluster + 3 inter-cluster arrows,
  25 paper nodes with blue concept phrases, 5 red limitante phrases).
- **T3**: `grant-flow-auditor` edited both files in place. Parent verification:
  §4 kept 51 body citation commands with 51 distinct keys, all resolving in
  `refs.bib`, 5 `\subsection*`, 15 prose paragraphs, 241 lines; §5 ended as a
  single paragraph with its 3 citation keys byte-identical. Baseline snapshot of
  the pre-audit invariants: `artefactos/pipeline/30-fase2-audit-baseline.txt`.
- **T4**: `revisor` VEREDICTO **PASS**, with `[ASESOR-GRAFO]` advisory only.
- **T5**: `redaccion/main.pdf`, 14 pages, 0 LaTeX errors, 1 pre-existing
  `Overfull \hbox` warning inherited from G1.
- **T6**: `artefactos/pipeline/30-fase2.md` (gate log with measured telemetry),
  `_estado.md` row `fase2 | G2 | PASS`, `estado_propuesta.md` with
  `next_step: fase3`, vault mirrors at `gate_status: pass`, refreshed vault graph
  report/json/html (31 nodes / 30 edges).
- **T7**: pending user approval.

## Root-cause fix delivered on the way

`grant-flow-auditor` had failed four times across the run with "assistant
returned no final report". Diagnosis from the child task record: the last
assistant message ended with `stopReason: length` after 16,259 reasoning tokens
and zero text tokens — it exhausted its output budget while reasoning none.
Fix: `.pi/subagents.json` profile for that agent moved from `effort: high` to
`effort: medium`; the next three dispatches completed. This removed the
pipeline's last degraded step.

## Notes

- The figure loop shares one 4-attempt budget across the three diagrams.
- `grant-flow-auditor` previously failed 3x in this runtime and is
  non-blocking; its routing was fixed and its Pi port now exists
  (`.pi/agents/grant-flow-auditor.md`), so this phase retries it.
