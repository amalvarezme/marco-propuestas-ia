#!/usr/bin/env python3
"""Build standalone wrapper for a diagram source, compile, and render PNG.

Usage:
    python3 compile_tikz.py arbol_problemas:tikz metodologico:tikz gantt:gantt

For kind "tikz", looks for diag_<name>.tex under proposal/sections/. For kind
"gantt", the source is instead the Redactor's real §14 output,
`proposal/sections/14_cronograma_actividades.tex` — there is no standalone
diag_gantt.tex (single-owner fix: Disenador-TikZ does not produce a separate
Gantt file; Redactor owns §14 inline, as either a `tabular`+`tikz` table or a
`ganttchart` spec). Both relative to the repo root (this script lives at
proposal/scripts/compile_tikz.py, so the repo root is two parents up).  All
intermediate files (.tex wrappers, .pdf, .png, .log) go under
/tmp/propuesta/figopt/.

Requires: pdflatex, pdftoppm in PATH.
"""
import sys, subprocess, re, pathlib

# Repo root = parent of parent of this script's directory.
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
WORK = pathlib.Path("/tmp/propuesta/figopt")
WORK.mkdir(parents=True, exist_ok=True)

def build(name, kind):
    if kind == "gantt":
        # §14 Cronograma is authored inline by Redactor, not as a standalone
        # diag_gantt.tex — source from the real section file.
        src = ROOT / "proposal/sections" / "14_cronograma_actividades.tex"
    else:
        src = ROOT / "proposal/sections" / f"diag_{name}.tex"
    if not src.exists():
        raise SystemExit(
            f"no existe {src}. Los diagramas/secciones se generan por cada corrida de "
            "/propuesta (disenador-tikz o redactor); ejecuta /propuesta hasta esa fase antes de compilar figuras."
        )
    text = src.read_text(encoding='utf-8')

    if kind == "tikz":
        # extract the first tikzpicture
        m = re.search(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}', text, flags=re.DOTALL)
        if not m:
            raise SystemExit(f"no tikzpicture found in {src}")
        body = m.group(0)
        wrapper = WORK / f"wrap_{name}.tex"
        wrapper.write_text(
            "\\documentclass[tikz,border=10pt]{standalone}\n"
            "\\usepackage[utf8]{inputenc}\n"
            "\\usepackage[T1]{fontenc}\n"
            "\\usepackage[spanish,es-tabla,es-noshorthands]{babel}\n"
            "\\usepackage{amssymb}\n"
            "\\usetikzlibrary{positioning,arrows.meta,shapes.geometric,calc,fit,backgrounds}\n"
            "\\definecolor{azulUNAL}{HTML}{0066B3}\n"
            "\\definecolor{grisLabIA}{HTML}{666666}\n"
            "\\definecolor{verdeGCPDS}{HTML}{2E8B57}\n"
            "\\begin{document}\n"
            + body + "\n"
            + "\\end{document}\n", encoding='utf-8')
    elif kind == "gantt":
        # extract the ganttchart block. redactor.md permits two forms for §14:
        #   (a) a bare \begin{ganttchart}...\end{ganttchart}, or
        #   (b) a ganttchart wrapped in \begin{tikzpicture}...\end{tikzpicture}
        #       (e.g. alongside a legend drawn with tikz).
        # \end{ganttchart} is the authoritative close marker for the chart
        # body itself; we only extend the extraction out to a wrapping
        # \end{tikzpicture} when a matching \begin{tikzpicture} is actually
        # present around the ganttchart, so bare ganttchart blocks don't
        # crash looking for a tikzpicture wrapper that was never promised.
        idx = text.find(r'\begin{ganttchart}')
        if idx < 0:
            raise SystemExit(f"could not find ganttchart in {src}")
        idx_gc_end = text.find(r'\end{ganttchart}', idx)
        if idx_gc_end < 0:
            raise SystemExit(f"could not find matching \\end{{ganttchart}} in {src}")
        end = idx_gc_end + len(r'\end{ganttchart}')

        # Optional wrapping tikzpicture: a \begin{tikzpicture} before the
        # ganttchart that is not already closed before it starts, and whose
        # matching \end{tikzpicture} appears after the ganttchart closes.
        tikz_begin = text.rfind(r'\begin{tikzpicture}', 0, idx)
        if tikz_begin >= 0:
            tikz_begin_close = text.find(r'\end{tikzpicture}', tikz_begin, idx)
            if tikz_begin_close < 0:
                tikz_end = text.find(r'\end{tikzpicture}', end)
                if tikz_end >= 0:
                    idx = tikz_begin
                    end = tikz_end + len(r'\end{tikzpicture}')

        body = text[idx:end]
        # Use article class with explicit paper size to avoid standalone bbox detection issues
        wrapper = WORK / f"wrap_{name}.tex"
        wrapper.write_text(
            "\\documentclass[11pt]{article}\n"
            "\\usepackage[paperwidth=17cm,paperheight=24cm,margin=0.5cm]{geometry}\n"
            "\\usepackage[utf8]{inputenc}\n"
            "\\usepackage[T1]{fontenc}\n"
            "\\usepackage[spanish,es-tabla,es-noshorthands]{babel}\n"
            "\\usepackage{amssymb}\n"
            "\\usepackage{tikz}\n"
            "\\usepackage{pgfgantt}\n"
            "\\usetikzlibrary{positioning,arrows.meta,shapes.geometric,calc,fit,backgrounds}\n"
            "\\definecolor{azulUNAL}{HTML}{0066B3}\n"
            "\\definecolor{grisLabIA}{HTML}{666666}\n"
            "\\definecolor{verdeGCPDS}{HTML}{2E8B57}\n"
            "\\pagestyle{empty}\n"
            "\\begin{document}\n"
            "\\centering\n"
            + body + "\n"
            + "\\end{document}\n", encoding='utf-8')
    else:
        raise SystemExit(f"unknown kind: {kind}")

    log = WORK / f"log_{name}.txt"
    r = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
         "-output-directory", str(WORK), str(wrapper)],
        capture_output=True
    )
    # write log with safe decoding
    log.write_bytes(r.stdout + r.stderr)
    if r.returncode != 0:
        print(f"COMPILE FAILED for {name}, see {log}")
        sys.exit(1)
    pdf = WORK / f"wrap_{name}.pdf"
    if not pdf.exists():
        print(f"PDF not produced for {name}")
        sys.exit(1)
    # clean up old PNGs
    for old in WORK.glob(f"fig_{name}-*.png"):
        old.unlink()
    subprocess.run(["pdftoppm", "-png", "-r", "200", str(pdf), str(WORK / f"fig_{name}")], check=True)
    print(f"OK: {name}")

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        name, kind = arg.split(":")
        build(name, kind)
