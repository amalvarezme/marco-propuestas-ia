#!/usr/bin/env python3
r"""Stage a docx-safe copy of proposal/main.tex for pandoc conversion.

Pandoc's LaTeX reader cannot parse raw `tikzpicture`/`ganttchart`
environments, so this script builds a staging tree that mirrors
`proposal/` but replaces each diagram section (`diag_*.tex`) with a plain
`\includegraphics` stub pointing at a PNG rasterized via `compile_tikz.py`
(reused as-is, via subprocess — kept a pure rasterizer per ADR-3).

§14 Cronograma (`14_cronograma_actividades.tex`) is a special case: Redactor
is the single owner of that section and may emit either a plain `tabular`
(pandoc-safe, copied verbatim) or a `ganttchart`/`tikzpicture` spec (needs
rasterization, same as the other diagrams). This module detects which form
is present before deciding whether to rasterize it.

Usage:
    python3 prep_docx.py --stage <dir>

Requires: pdflatex, pdftoppm in PATH (same as compile_tikz.py).
"""
import argparse
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PROP = ROOT / "proposal"
WORK = pathlib.Path("/tmp/propuesta/figopt")

# diag_<name>.tex -> (compile_tikz name, kind)
DIAGRAM_MAP = {
    "diag_arbol_problemas.tex": ("arbol_problemas", "tikz"),
    "diag_metodologico.tex": ("metodologico", "tikz"),
}

# §14 Cronograma: single owner is Redactor (not a diag_*.tex). Only
# rasterize it when it actually contains a diagram env; a plain tabular is
# pandoc-safe and gets copied verbatim.
CRONOGRAMA_FILE = "14_cronograma_actividades.tex"
_GANTT_ENV_RE = re.compile(r'\\begin\{(ganttchart|tikzpicture)\}')


def warn(msg: str) -> None:
    print(f"[WARN] {msg}", file=sys.stderr)


def cronograma_has_diagram_env(sections_dir: pathlib.Path) -> bool:
    """Detect whether Redactor's §14 output uses a `ganttchart`/`tikzpicture`
    env (needs rasterization for pandoc) vs. a plain `tabular` (pandoc-safe,
    copy verbatim)."""
    f = sections_dir / CRONOGRAMA_FILE
    if not f.exists():
        return False
    text = f.read_text(encoding="utf-8")
    return bool(_GANTT_ENV_RE.search(text))


def rasterize_diagrams(sections_dir: pathlib.Path) -> None:
    """Invoke compile_tikz.py for whichever diagrams actually exist in
    `sections_dir`. Only rasterizes what is present (main.tex may not
    reference all diagrams yet at every pipeline stage). §14 Cronograma is
    included only when it contains a diagram env (see
    `cronograma_has_diagram_env`)."""
    args = [
        f"{name}:{kind}"
        for filename, (name, kind) in DIAGRAM_MAP.items()
        if (sections_dir / filename).exists()
    ]
    if cronograma_has_diagram_env(sections_dir):
        args.append("gantt:gantt")
    if not args:
        return
    r = subprocess.run(
        [sys.executable, str(HERE / "compile_tikz.py"), *args],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(r.stdout)
        print(r.stderr, file=sys.stderr)
        raise SystemExit("prep_docx: compile_tikz.py failed to rasterize diagrams")


def stage_diagram_image(name: str, stage: pathlib.Path) -> str:
    """Copy the rasterized PNG(s) for `name` into `stage`.

    Gate-fix: glob `fig_<name>-*.png` (never hardcode `-1.png`) and WARN on
    multi-page overflow instead of silently truncating to page 1 — the
    Gantt wrapper uses a fixed paper size and can overflow to page 2 for an
    unusually long schedule.
    """
    pages = sorted(WORK.glob(f"fig_{name}-*.png"))
    if not pages:
        raise SystemExit(f"prep_docx: no rasterized PNG found for '{name}' in {WORK}")
    if len(pages) > 1:
        warn(
            f"diagram '{name}' rasterized to {len(pages)} pages "
            f"({', '.join(p.name for p in pages)}); only page 1 is embedded "
            "in the docx. The diagram likely overflowed its fixed paper size "
            "(e.g. a long Gantt chart) — shorten it or split it manually."
        )
    chosen = pages[0]
    dest_name = f"fig_{name}.png"
    shutil.copy2(chosen, stage / dest_name)
    return dest_name


def build_stage(stage: pathlib.Path) -> pathlib.Path:
    stage.mkdir(parents=True, exist_ok=True)
    (stage / "sections").mkdir(parents=True, exist_ok=True)

    main_tex = PROP / "main.tex"
    refs_bib = PROP / "refs.bib"
    logos_dir = PROP / "logos"
    sections_dir = PROP / "sections"

    if not main_tex.exists():
        raise SystemExit(f"prep_docx: {main_tex} does not exist — compile the PDF first")

    shutil.copy2(main_tex, stage / "main.tex")
    if refs_bib.exists():
        shutil.copy2(refs_bib, stage / "refs.bib")
    if logos_dir.exists():
        shutil.copytree(logos_dir, stage / "logos", dirs_exist_ok=True)

    if sections_dir.exists():
        rasterize_diagrams(sections_dir)
        cronograma_is_diagram = cronograma_has_diagram_env(sections_dir)
        for f in sorted(sections_dir.glob("*.tex")):
            if f.name in DIAGRAM_MAP:
                name, _kind = DIAGRAM_MAP[f.name]
                png_name = stage_diagram_image(name, stage)
                (stage / "sections" / f.name).write_text(
                    f"\\includegraphics[width=\\linewidth]{{{png_name}}}\n",
                    encoding="utf-8",
                )
            elif f.name == CRONOGRAMA_FILE and cronograma_is_diagram:
                png_name = stage_diagram_image("gantt", stage)
                (stage / "sections" / f.name).write_text(
                    f"\\includegraphics[width=\\linewidth]{{{png_name}}}\n",
                    encoding="utf-8",
                )
            else:
                shutil.copy2(f, stage / "sections" / f.name)

    return stage / "main.tex"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stage", required=True,
        help="staging directory to build the docx-safe tex tree in",
    )
    args = parser.parse_args()

    staged_main = build_stage(pathlib.Path(args.stage))
    print(staged_main)


if __name__ == "__main__":
    main()
