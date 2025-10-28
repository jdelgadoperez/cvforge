"""
Example configuration file for the Resume PDF Generator.

CUSTOMIZATION INSTRUCTIONS:
===========================

This is an example configuration showing how to customize your resume's appearance.

TO USE THIS FILE:
1. Copy this file: cp config.example.py config_custom.py
2. Edit config_custom.py with your preferred settings
3. Import Config from config_custom in markdown_to_resume_pdf.py:

   Change this line:
   from modules import Config

   To this:
   from config_custom import Config

OR simply edit modules/config.py directly if you don't need multiple configurations.

WHAT YOU CAN CUSTOMIZE:
- Colors: Change the hex color codes for a different color scheme
- Fonts: Adjust font families and sizes
- Spacing: Modify margins, padding, and line spacing
- Layout: Change page size and content dimensions
- Features: Enable/disable duration calculations and other features

See the examples below for different customization scenarios.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch


# ====================
# EXAMPLE 1: Professional Green Theme
# ====================
class GreenThemeConfig:
    """Professional green color scheme - great for tech/environmental roles"""

    # Color scheme
    PRIMARY_COLOR = colors.HexColor("#047857")  # Emerald green
    ACCENT_COLOR = colors.HexColor("#065f46")   # Darker green
    LIGHT_GRAY = colors.HexColor("#6b7280")
    DARK_GRAY = colors.HexColor("#1f2937")

    # Fonts (same as default)
    FONT_FAMILY_BASE = "Helvetica"
    FONT_FAMILY_BOLD = "Helvetica-Bold"
    FONT_FAMILY_ITALIC = "Helvetica-Oblique"

    # Font sizes (same as default)
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

    # Page layout
    PAGE_SIZE = letter
    MARGIN_TOP = 0.5 * inch
    MARGIN_BOTTOM = 0.5 * inch
    MARGIN_LEFT = 0.75 * inch
    MARGIN_RIGHT = 0.75 * inch

    # Spacing
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
    SPACE_BEFORE_SECTION = 12

    LEADING_BULLET = 12
    LEADING_SUMMARY = 13
    LEADING_SKILL_LIST = 11

    BULLET_INDENT = 12

    # Content formatting
    DIVIDER_WIDTH = 7 * inch
    DIVIDER_THICKNESS = 1
    DIVIDER_COLOR = PRIMARY_COLOR
    BORDER_WIDTH = 0

    # File paths
    INPUTS_FOLDER = "~/Documents/resumes/input"
    EXPORTS_FOLDER = "~/Documents/resumes/output"

    # Features
    CALCULATE_DURATIONS = True
    KEEP_SECTIONS_TOGETHER = True


# ====================
# EXAMPLE 2: Compact Layout (More content per page)
# ====================
class CompactConfig:
    """Compact layout with smaller fonts and tighter spacing"""

    # Colors (professional blue)
    PRIMARY_COLOR = colors.HexColor("#1e40af")
    ACCENT_COLOR = colors.HexColor("#1e3a8a")
    LIGHT_GRAY = colors.HexColor("#6b7280")
    DARK_GRAY = colors.HexColor("#1f2937")

    # Fonts
    FONT_FAMILY_BASE = "Helvetica"
    FONT_FAMILY_BOLD = "Helvetica-Bold"
    FONT_FAMILY_ITALIC = "Helvetica-Oblique"

    # Smaller font sizes for compact layout
    FONT_SIZE_NAME = 22
    FONT_SIZE_SUBTITLE = 11
    FONT_SIZE_CONTACT = 8.5
    FONT_SIZE_SECTION_HEADER = 12
    FONT_SIZE_JOB_TITLE = 10.5
    FONT_SIZE_COMPANY_INFO = 9.5
    FONT_SIZE_BULLET = 9
    FONT_SIZE_SKILL_CATEGORY = 9.5
    FONT_SIZE_SKILL_LIST = 8.5
    FONT_SIZE_SUMMARY = 9.5

    # Tighter margins
    PAGE_SIZE = letter
    MARGIN_TOP = 0.4 * inch
    MARGIN_BOTTOM = 0.4 * inch
    MARGIN_LEFT = 0.6 * inch
    MARGIN_RIGHT = 0.6 * inch

    # Tighter spacing
    SPACE_AFTER_NAME = 4
    SPACE_AFTER_SUBTITLE = 8
    SPACE_AFTER_CONTACT = 16
    SPACE_AFTER_SECTION_HEADER = 6
    SPACE_AFTER_JOB_TITLE = 2
    SPACE_AFTER_COMPANY_INFO = 4
    SPACE_AFTER_BULLET = 3
    SPACE_AFTER_SKILL_CATEGORY = 2
    SPACE_AFTER_SKILL_LIST = 4
    SPACE_AFTER_SUMMARY = 10
    SPACE_BEFORE_SECTION = 10

    LEADING_BULLET = 11
    LEADING_SUMMARY = 12
    LEADING_SKILL_LIST = 10

    BULLET_INDENT = 10

    # Content formatting
    DIVIDER_WIDTH = 7.3 * inch  # Wider divider for wider margins
    DIVIDER_THICKNESS = 1
    DIVIDER_COLOR = PRIMARY_COLOR
    BORDER_WIDTH = 0

    # File paths
    INPUTS_FOLDER = "~/Documents/resumes/input"
    EXPORTS_FOLDER = "~/Documents/resumes/output"

    # Features
    CALCULATE_DURATIONS = True
    KEEP_SECTIONS_TOGETHER = False  # Allow page breaks for more content


# ====================
# EXAMPLE 3: Classic Black & White (ATS-Optimized)
# ====================
class ClassicConfig:
    """Traditional black and white resume - maximum ATS compatibility"""

    # Simple black/gray colors
    PRIMARY_COLOR = colors.HexColor("#000000")  # Pure black
    ACCENT_COLOR = colors.HexColor("#333333")   # Dark gray
    LIGHT_GRAY = colors.HexColor("#666666")     # Medium gray
    DARK_GRAY = colors.HexColor("#000000")      # Black

    # Fonts
    FONT_FAMILY_BASE = "Helvetica"
    FONT_FAMILY_BOLD = "Helvetica-Bold"
    FONT_FAMILY_ITALIC = "Helvetica-Oblique"

    # Standard font sizes
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

    # Standard margins
    PAGE_SIZE = letter
    MARGIN_TOP = 0.5 * inch
    MARGIN_BOTTOM = 0.5 * inch
    MARGIN_LEFT = 0.75 * inch
    MARGIN_RIGHT = 0.75 * inch

    # Standard spacing
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
    SPACE_BEFORE_SECTION = 12

    LEADING_BULLET = 12
    LEADING_SUMMARY = 13
    LEADING_SKILL_LIST = 11

    BULLET_INDENT = 12

    # Minimal formatting
    DIVIDER_WIDTH = 7 * inch
    DIVIDER_THICKNESS = 0.5  # Thinner line
    DIVIDER_COLOR = colors.HexColor("#000000")
    BORDER_WIDTH = 0

    # File paths
    INPUTS_FOLDER = "~/Documents/resumes/input"
    EXPORTS_FOLDER = "~/Documents/resumes/output"

    # Features
    CALCULATE_DURATIONS = True
    KEEP_SECTIONS_TOGETHER = True


# ====================
# TO USE ONE OF THESE CONFIGURATIONS:
# ====================
# 1. Copy the class you want (e.g., GreenThemeConfig)
# 2. Rename it to just "Config"
# 3. Save this file as config_custom.py
# 4. Update the import in markdown_to_resume_pdf.py

# Example: To use the Green Theme
# Config = GreenThemeConfig

# Example: To use the Compact Layout
# Config = CompactConfig

# Example: To use the Classic Black & White
# Config = ClassicConfig


# ====================
# CREATE YOUR OWN:
# ====================
# Copy any of the above examples and modify the values to create your own theme!
#
# Color picker tools:
# - https://htmlcolorcodes.com/
# - https://coolors.co/
# - https://colorhunt.co/
