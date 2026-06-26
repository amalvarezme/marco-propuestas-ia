#!/usr/bin/env python3
"""Build standalone wrapper for a diag_*.tex, compile, and render PNG.

Usage:
    python3 compile_tikz.py arbol_problemas:tikz metodologico:tikz gantt:gantt

Looks for diag_<name>.tex under proposal/sections/ relative to the repo root
(this script lives at proposal/scripts/compile_tikz.py, so the repo root is
two parents up).  All intermediate files (.tex wrappers, .pdf, .png, .log) go
under /tmp/opencode/figopt/.

Requires: pdflatex, pdftoppm in PATH.
"""
import sys, subprocess, re, pathlib

# Repo root = parent of parent of this script's directory.
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
WORK = pathlib.Path("/tmp/opencode/figopt")
WORK.mkdir(parents=True, exist_ok=True)

def build(name, kind):
    src = ROOT / "proposal/sections" / f"diag_{name}.tex"
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
        # extract the ganttchart block AND the legend tikzpicture block
        idx = text.find(r'\begin{ganttchart}')
        idx2 = text.find(r'\end{tikzpicture}', idx)
        if idx < 0 or idx2 < 0:
            raise SystemExit(f"could not find ganttchart/tikzpicture in {src}")
        body = text[idx:idx2 + len(r'\end{tikzpicture}')]
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
