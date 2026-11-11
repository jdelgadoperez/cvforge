#!/usr/bin/env python3
"""
Backward-compatible wrapper around ``cvforge build``.

    python3 markdown_to_resume_pdf.py <input.md> [output.pdf] [--force]

is equivalent to

    cvforge build <input.md> [output.pdf] [--force]

Prefer ``uv run cvforge build ...``; see README.md.
"""

import sys

from cvforge.cli import main

if __name__ == "__main__":
    sys.exit(main(["build", *sys.argv[1:]]))
