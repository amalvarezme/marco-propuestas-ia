#!/usr/bin/env python3
"""
split_latex_section.py - Helper script in proposal/scripts/ to split LaTeX section files.
"""

import sys
from pathlib import Path

# Add skill script to path if present, or run direct logic
SKILL_SCRIPT = Path(__file__).resolve().parents[3] / ".agents/skills/latex-section-splitter/scripts/split_latex.py"

if SKILL_SCRIPT.exists():
    import importlib.util
    spec = importlib.util.spec_from_file_location("split_latex", SKILL_SCRIPT)
    split_latex = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(split_latex)
    if __name__ == "__main__":
        split_latex.main()
else:
    print(f"Error: Skill script not found at {SKILL_SCRIPT}", file=sys.stderr)
    sys.exit(1)
