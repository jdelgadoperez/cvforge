"""
Resume PDF Generator - Modular Components

A professional markdown-to-PDF resume generator with extensive customization options.

Modules:
    - config: Configuration settings (colors, fonts, spacing)
    - styles: ReportLab paragraph style definitions
    - parser: Markdown parsing into structured data
    - formatter: Markdown to HTML conversion
    - duration: Date and duration calculations
    - validators: File validation and error handling
    - generator: Core PDF generation logic

Usage:
    from modules import config, parser, generator

    # Parse markdown
    data = parser.parse_markdown_resume(markdown_content)

    # Generate PDF
    generator.generate_pdf_from_data(data, "output.pdf")

Customization:
    Modify modules/config.py to customize:
    - Color scheme
    - Font sizes and families
    - Page margins and layout
    - Spacing between elements
    - Feature flags

Author: Jess Delgado Perez
License: MIT
"""

__version__ = "2.0.0"
__author__ = "Jess Delgado Perez"

# Convenient imports for common usage
from .config import Config
from .parser import parse_markdown_resume, validate_parsed_data
from .generator import generate_pdf_from_data
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
