"""
test_split_latex.py - Unit tests for the latex-section-splitter skill script.
"""

import sys
from pathlib import Path
import pytest

# Add skill script directory to sys.path
SKILL_SCRIPT_DIR = Path(__file__).resolve().parents[2] / ".agents/skills/latex-section-splitter/scripts"
sys.path.insert(0, str(SKILL_SCRIPT_DIR))

import split_latex


def test_slugify():
    assert split_latex.slugify("Metodología y Fases") == "metodología_y_fases"
    assert split_latex.slugify("Subsection 1.1: \\textbf{Core}") == "subsection_11_core"


def test_estimate_tokens():
    text_es = "Este es un texto de prueba en español."  # 8 words
    assert split_latex.estimate_tokens(text_es, lang="es") == 14

    text_en = "This is a test text in English."  # 7 words
    assert split_latex.estimate_tokens(text_en, lang="en") == 9

    assert split_latex.estimate_tokens("word word word", custom_multiplier=2.0) == 6


def test_split_latex_file(tmp_path):
    sample_tex = tmp_path / "10_metodologia.tex"
    sample_content = (
        "\\section{Metodología}\n"
        "Texto introductorio de la sección.\n\n"
        "\\subsection{Fase 1: Recolección de Datos}\n"
        "Detalle de la fase 1.\n"
        "\\begin{equation}\n"
        "E = mc^2\n"
        "\\end{equation}\n\n"
        "\\subsection{Fase 2: Modelamiento y Validación}\n"
        "Detalle de la fase 2.\n"
    )
    sample_tex.write_text(sample_content, encoding="utf-8")

    parent_file, sub_files = split_latex.split_latex_file(sample_tex, target_level="subsection", verbose=False)

    assert parent_file == sample_tex
    assert len(sub_files) == 3  # intro, fase 1, fase 2

    # Check directory created
    sub_dir = tmp_path / "10_metodologia"
    assert sub_dir.is_dir()

    # Check contents of parent driver file
    driver_text = parent_file.read_text(encoding="utf-8")
    assert "\\input{" in driver_text
    assert "01_intro.tex" in driver_text
    assert "02_fase_1_recolección_de_datos.tex" in driver_text
    assert "03_fase_2_modelamiento_y_validación.tex" in driver_text

    # Check sub-file environment integrity
    fase1_text = (sub_dir / "02_fase_1_recolección_de_datos.tex").read_text(encoding="utf-8")
    assert "\\begin{equation}" in fase1_text
    assert "\\end{equation}" in fase1_text


def test_dry_run_mode(tmp_path):
    sample_tex = tmp_path / "04_estado_arte.tex"
    sample_content = (
        "\\section{Estado del Arte}\n"
        "Intro\n"
        "\\subsection{Visión General}\n"
        "Contenido 1\n"
        "\\subsection{Modelos Recientes}\n"
        "Contenido 2\n"
    )
    sample_tex.write_text(sample_content, encoding="utf-8")

    parent_file, sub_files = split_latex.split_latex_file(sample_tex, dry_run=True, verbose=False)
    sub_dir = tmp_path / "04_estado_arte"

    # Directory should NOT be created in dry-run mode
    assert not sub_dir.exists()
    assert sample_tex.read_text(encoding="utf-8") == sample_content


def test_environment_safety(tmp_path):
    sample_tex = tmp_path / "14_cronograma.tex"
    sample_content = (
        "\\section{Cronograma}\n"
        "Intro\n"
        "\\subsection{Gantt General}\n"
        "\\begin{ganttchart}{1}{12}\n"
        "% \\subsection{Fake Inner Heading}\n"
        "\\ganttbar{Fase A}{1}{6}\n"
        "\\end{ganttchart}\n"
        "\\subsection{Entregables}\n"
        "Lista de entregables\n"
    )
    sample_tex.write_text(sample_content, encoding="utf-8")

    parent_file, sub_files = split_latex.split_latex_file(sample_tex, verbose=False)
    sub_dir = tmp_path / "14_cronograma"

    assert len(sub_files) == 3
    gantt_sub_text = (sub_dir / "02_gantt_general.tex").read_text(encoding="utf-8")
    assert "\\begin{ganttchart}" in gantt_sub_text
    assert "\\end{ganttchart}" in gantt_sub_text
    assert "Fake Inner Heading" in gantt_sub_text


def test_figures_and_subsections_preservation(tmp_path):
    sample_tex = tmp_path / "03_descripcion.tex"
    sample_content = (
        "\\section{Descripción del Problema}\n"
        "Contexto general.\n\n"
        "\\subsection{Diagnóstico y Árbol de Problemas}\n"
        "Análisis de causas y efectos.\n"
        "\\subsubsection{Detalle de Causas}\n"
        "Causas primarias.\n"
        "\\begin{figure}[htbp]\n"
        "  \\centering\n"
        "  \\includegraphics[width=0.8\\textwidth]{figuras/arbol.png}\n"
        "  \\caption{Árbol de Problemas}\n"
        "\\end{figure}\n\n"
        "\\subsection{Solución Propuesta}\n"
        "Descripción de la solución.\n"
    )
    sample_tex.write_text(sample_content, encoding="utf-8")

    parent_file, sub_files = split_latex.split_latex_file(sample_tex, target_level="subsection", verbose=False)
    sub_dir = tmp_path / "03_descripcion"

    assert len(sub_files) == 3
    diag_file = sub_dir / "02_diagnóstico_y_árbol_de_problemas.tex"
    diag_text = diag_file.read_text(encoding="utf-8")

    # Verify subsubsection is preserved inside the subsection file
    assert "\\subsubsection{Detalle de Causas}" in diag_text
    # Verify figure environment, includegraphics, and caption are preserved inside
    assert "\\begin{figure}" in diag_text
    assert "\\includegraphics[width=0.8\\textwidth]{figuras/arbol.png}" in diag_text
    assert "\\end{figure}" in diag_text


def test_complex_latex_structure_preservation(tmp_path):
    sample_tex = tmp_path / "05_propuesta_compleja.tex"
    sample_content = (
        "\\section{Resultados y Figuras}\n"
        "Visión general de los experimentos.\n\n"
        "\\subsection{Arquitectura y Diagramas}\n"
        "Descripción del sistema.\n"
        "\\subsubsection{Componente A}\n"
        "Detalle del componente A.\n"
        "\\paragraph{Especificación de Interfaz}\n"
        "Detalle de puertos API.\n"
        "\\begin{figure*}[t]\n"
        "  \\centering\n"
        "  \\includegraphics[scale=0.5]{figuras/arquitectura_completa.png}\n"
        "  \\caption{Diagrama Global del Sistema}\n"
        "  \\label{fig:diag_global}\n"
        "\\end{figure*}\n\n"
        "\\begin{table}[h]\n"
        "  \\centering\n"
        "  \\begin{tabular}{|c|c|}\n"
        "    Métrica & Valor \\\\\n"
        "    Accuracy & 0.95 \\\\\n"
        "  \\end{tabular}\n"
        "  \\caption{Métricas}\n"
        "\\end{table}\n\n"
        "\\subsection{Evaluación de Desempeño}\n"
        "Resultados finales.\n"
        "\\begin{itemize}\n"
        "  \\item Latencia baja\n"
        "  \\item Alta disponibilidad\n"
        "\\end{itemize}\n"
    )
    sample_tex.write_text(sample_content, encoding="utf-8")

    parent_file, sub_files = split_latex.split_latex_file(sample_tex, target_level="subsection", verbose=False)
    sub_dir = tmp_path / "05_propuesta_compleja"

    assert len(sub_files) == 3
    sub1_text = (sub_dir / "02_arquitectura_y_diagramas.tex").read_text(encoding="utf-8")
    sub2_text = (sub_dir / "03_evaluación_de_desempeño.tex").read_text(encoding="utf-8")

    # Verify subheadings (subsubsection, paragraph) preserved in sub1
    assert "\\subsubsection{Componente A}" in sub1_text
    assert "\\paragraph{Especificación de Interfaz}" in sub1_text

    # Verify figure*, includegraphics, caption, label preserved in sub1
    assert "\\begin{figure*}[t]" in sub1_text
    assert "\\includegraphics[scale=0.5]{figuras/arquitectura_completa.png}" in sub1_text
    assert "\\caption{Diagrama Global del Sistema}" in sub1_text
    assert "\\label{fig:diag_global}" in sub1_text
    assert "\\end{figure*}" in sub1_text

    # Verify table and tabular preserved in sub1
    assert "\\begin{table}[h]" in sub1_text
    assert "\\begin{tabular}{|c|c|}" in sub1_text
    assert "\\end{table}" in sub1_text

    # Verify itemize list preserved in sub2
    assert "\\begin{itemize}" in sub2_text
    assert "\\item Latencia baja" in sub2_text
    assert "\\end{itemize}" in sub2_text


def test_min_tokens_threshold(tmp_path):
    sample_tex = tmp_path / "short_section.tex"
    sample_content = (
        "\\section{Short}\n"
        "\\subsection{Part 1}\n"
        "Line 1\n"
        "\\subsection{Part 2}\n"
        "Line 2\n"
    )
    sample_tex.write_text(sample_content, encoding="utf-8")

    parent_file, sub_files = split_latex.split_latex_file(sample_tex, min_tokens=100000, lang="es", verbose=False)
    assert len(sub_files) == 0
    assert not (tmp_path / "short_section").exists()
