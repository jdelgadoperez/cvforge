"""
Configuration module for the resume generator.

To customize colors, fonts, spacing, or other settings:
1. Copy this file to config_custom.py
2. Modify the values in config_custom.py
3. Import from config_custom instead of config in markdown_to_resume_pdf.py

Or modify this file directly for your needs.
"""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch


class Config:
    """Global configuration for resume PDF generation"""

    # ====================
    # COLOR SCHEME
    # ====================
    # Customize these hex colors to match your personal brand
    # Use online color pickers like https://htmlcolorcodes.com/

    PRIMARY_COLOR = colors.HexColor(
        "#1e40af"
    )  # Darker professional blue - used for headers and dividers
    ACCENT_COLOR = colors.HexColor("#1e3a8a")  # Even darker blue - used for subtitles
    LIGHT_GRAY = colors.HexColor(
        "#6b7280"
    )  # Gray for secondary text (dates, locations)
    DARK_GRAY = colors.HexColor("#1f2937")  # Almost black for main text

    # ====================
    # FONT SETTINGS
    # ====================
    # Available fonts: Helvetica, Helvetica-Bold, Helvetica-Oblique, Times-Roman, Courier

    FONT_FAMILY_BASE = "Helvetica"
    FONT_FAMILY_BOLD = "Helvetica-Bold"
    FONT_FAMILY_ITALIC = "Helvetica-Oblique"

    # Font sizes (in points)
    FONT_SIZE_NAME = 24
    FONT_SIZE_SUBTITLE = 12
    FONT_SIZE_CONTACT = 9
    FONT_SIZE_SECTION_HEADER = 13
    FONT_SIZE_JOB_TITLE = 11
    FONT_SIZE_COMPANY_INFO = 10
    FONT_SIZE_BULLET = 9.5
    FONT_SIZE_SKILL_CATEGORY = 10
    FONT_SIZE_SKILL_LIST = 9
    FONT_SIZE_SUMMARY = 10

    # ====================
    # PAGE LAYOUT
    # ====================

    PAGE_SIZE = letter  # letter (8.5" x 11") or A4

    # Page margins (in inches)
    MARGIN_TOP = 0.5 * inch
    MARGIN_BOTTOM = 0.5 * inch
    MARGIN_LEFT = 0.75 * inch
    MARGIN_RIGHT = 0.75 * inch

    # ====================
    # SPACING SETTINGS
    # ====================

    # Spacing after elements (in points)
    SPACE_AFTER_NAME = 6
    SPACE_AFTER_SUBTITLE = 12
    SPACE_AFTER_CONTACT = 20
    SPACE_AFTER_SECTION_HEADER = 8
    SPACE_AFTER_JOB_TITLE = 2
    SPACE_AFTER_COMPANY_INFO = 6
    SPACE_AFTER_BULLET = 4
    SPACE_AFTER_SKILL_CATEGORY = 2
    SPACE_AFTER_SKILL_LIST = 6
    SPACE_AFTER_SUMMARY = 12

    # Spacing before elements (in points)
    SPACE_BEFORE_SECTION = 12

    # Leading (line height) for multi-line text
    LEADING_BULLET = 12
    LEADING_SUMMARY = 13
    LEADING_SKILL_LIST = 11

    # Indentation
    BULLET_INDENT = 12  # Left indent for bullet points

    # ====================
    # CONTENT FORMATTING
    # ====================

    # Section divider line
    DIVIDER_WIDTH = 7 * inch
    DIVIDER_THICKNESS = 1
    DIVIDER_COLOR = PRIMARY_COLOR  # Uses PRIMARY_COLOR by default

    # Border settings
    BORDER_WIDTH = 0

    # ====================
    # FILE PATHS
    # ====================

    # Default input/output directories (can be overridden via command line)
    # Set to empty string to disable and use current directory instead
    INPUTS_FOLDER = "inputs"  # os.path.expanduser("~/projects/sandbox/inputs")
    OUTPUTS_FOLDER = (
        "outputs"  # os.path.expanduser("~/projects/sandbox/resume/outputs")
    )

    # ====================
    # FEATURE FLAGS
    # ====================

    # Enable/disable automatic duration calculation
    CALCULATE_DURATIONS = True

    # Keep sections together to avoid page breaks (may cause formatting issues with long sections)
    KEEP_SECTIONS_TOGETHER = True
