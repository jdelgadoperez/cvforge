"""
cvforge - markdown resume to PDF generator.

A professional markdown-to-PDF resume generator with extensive customization options.
The command-line interface lives in cvforge.cli (installed as the ``cvforge`` script).

Modules:
    - config: Configuration settings (colors, fonts, spacing)
    - styles: ReportLab paragraph style definitions
    - parser: Markdown parsing into structured data
    - formatter: Markdown to HTML conversion
    - duration: Date and duration calculations
    - validators: File validation and error handling
    - generator: Core PDF generation logic
    - structured: Parsed resume -> stable JSON-ready structure (``cvforge parse``)
    - cli: argparse command-line interface (``cvforge build`` / ``cvforge parse``)

Usage:
    from cvforge import config, parser, generator

    # Parse markdown
    data = parser.parse_markdown_resume(markdown_content)

    # Generate PDF
    generator.generate_pdf_from_data(data, "output.pdf")

Customization:
    Modify cvforge/config.py to customize:
    - Color scheme
    - Font sizes and families
    - Page margins and layout
    - Spacing between elements
    - Feature flags

Author: Jess Delgado Perez
License: MIT
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("cvforge")
except PackageNotFoundError:  # running from a source checkout without installing
    __version__ = "0.0.0+unknown"
__author__ = "Jess Delgado Perez"

# Convenient imports for common usage
from .config import Config
from .parser import parse_markdown_resume, validate_parsed_data
from .generator import generate_pdf_from_data
from .structured import SCHEMA_VERSION, to_structured
from .validators import (
    check_dependencies,
    validate_input_file,
    validate_file_extension,
    check_output_file_overwrite,
    read_markdown_file,
    validate_output_path,
    generate_output_filename,
)
from .duration import is_dateutil_available, warn_if_dateutil_unavailable

__all__ = [
    "Config",
    "parse_markdown_resume",
    "validate_parsed_data",
    "generate_pdf_from_data",
    "SCHEMA_VERSION",
    "to_structured",
    "check_dependencies",
    "validate_input_file",
    "validate_file_extension",
    "check_output_file_overwrite",
    "read_markdown_file",
    "validate_output_path",
    "generate_output_filename",
    "is_dateutil_available",
    "warn_if_dateutil_unavailable",
]
