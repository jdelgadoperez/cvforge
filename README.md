# Resume PDF Generator

Convert markdown resume to professional PDF with clean, customizable design.

## Quick Start

```bash
# Install dependencies
pip install reportlab python-dateutil

# Generate your resume
python3 markdown_to_resume_pdf.py resume.md
```

## Installation

### Quick Install (All Dependencies)

```bash
pip install reportlab python-dateutil
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### Minimal Install (Required Only)

```bash
pip install reportlab
```

Note: Without `python-dateutil`, duration calculations (e.g., "1 year 10 months") will be skipped, but the PDF will still generate successfully.

## Usage

### Basic Usage

```bash
python3 markdown_to_resume_pdf.py resume.md
```

This creates `resume.pdf` in the same directory.

### Specify Output File

```bash
python3 markdown_to_resume_pdf.py resume.md my_resume.pdf
```

## Features

✨ **Professional Design**

- Clean, modern color schemes
- Optimized spacing and typography
- ATS-friendly format

🎨 **Extensive Customization**

- **Colors**: Change primary, accent, and text colors
- **Fonts**: Customize font families and sizes
- **Spacing**: Adjust margins, padding, and line spacing
- **Layout**: Modify page size and content dimensions
- **Features**: Toggle duration calculations and section grouping

🤖 **Auto-Duration Calculation**

- Automatically calculates job duration from dates
- "Present" roles auto-update to current date
- Format: `December 2023 - Present (1 year 10 months)`

🏗️ **Modular Architecture**

- Clean separation of concerns
- Easy to extend and maintain
- Well-documented code

🛡️ **Smart Error Handling**

- Clear error messages
- File suggestions when not found
- Overwrite protection
- Graceful dependency handling

## Customization Guide

### Method 1: Edit Config File (Recommended)

The easiest way to customize your resume is to edit `modules/config.py`:

```python
# modules/config.py

class Config:
    # Change colors (use hex color codes)
    PRIMARY_COLOR = colors.HexColor("#1e40af")  # Your brand color
    ACCENT_COLOR = colors.HexColor("#1e3a8a")   # Complementary color

    # Adjust font sizes
    FONT_SIZE_NAME = 24
    FONT_SIZE_SECTION_HEADER = 13

    # Modify spacing
    MARGIN_TOP = 0.5 * inch
    MARGIN_LEFT = 0.75 * inch

    # Toggle features
    CALCULATE_DURATIONS = True
    KEEP_SECTIONS_TOGETHER = True
```

### Method 2: Use Example Themes

Check out `config.example.py` for pre-configured themes:

- **Green Theme**: Professional green color scheme
- **Compact Layout**: Smaller fonts and tighter spacing for more content
- **Classic Black & White**: Traditional ATS-optimized design

To use a theme:

```bash
cp config.example.py config_custom.py
# Edit config_custom.py to select your theme
# Update import in markdown_to_resume_pdf.py
```

### What You Can Customize

#### Colors

```python
PRIMARY_COLOR = colors.HexColor("#1e40af")  # Headers, dividers
ACCENT_COLOR = colors.HexColor("#1e3a8a")   # Subtitle
LIGHT_GRAY = colors.HexColor("#6b7280")     # Secondary text
DARK_GRAY = colors.HexColor("#1f2937")      # Body text
```

Find colors at:

- [HTML Color Codes](https://htmlcolorcodes.com/)
- [Coolors](https://coolors.co/)
- [Color Hunt](https://colorhunt.co/)

#### Font Sizes

```python
FONT_SIZE_NAME = 24           # Your name
FONT_SIZE_SECTION_HEADER = 13  # Section titles
FONT_SIZE_BULLET = 9.5        # Bullet points
```

#### Page Layout

```python
PAGE_SIZE = letter  # or A4
MARGIN_TOP = 0.5 * inch
MARGIN_LEFT = 0.75 * inch
```

#### Spacing

```python
SPACE_AFTER_NAME = 6
SPACE_BEFORE_SECTION = 12
BULLET_INDENT = 12
```

See `modules/config.py` for complete list of customizable options.

## Project Structure

```
resume/
├── markdown_to_resume_pdf.py  # Main entry point (90 lines)
├── config.example.py          # Example themes and customization guide
├── modules/
│   ├── __init__.py           # Package initialization
│   ├── config.py             # Configuration settings
│   ├── styles.py             # PDF style definitions
│   ├── parser.py             # Markdown parsing logic
│   ├── formatter.py          # Markdown to HTML conversion
│   ├── duration.py           # Date/duration calculations
│   ├── validators.py         # File validation and error handling
│   └── generator.py          # Core PDF generation
├── requirements.txt
└── README.md
```

### Module Responsibilities

- **config.py**: All configuration options (colors, fonts, spacing)
- **styles.py**: ReportLab paragraph style definitions
- **parser.py**: Parse markdown into structured data
- **formatter.py**: Convert markdown formatting to HTML
- **duration.py**: Calculate date ranges and durations
- **validators.py**: File validation and helpful error messages
- **generator.py**: Core PDF generation using ReportLab

## Markdown Format

The script expects a specific markdown format. Key structure:

```markdown
# Your Name

**Your Title/Tagline**

your.email@example.com | Location | [LinkedIn](url)

## PROFESSIONAL SUMMARY

Brief summary of your experience...

## TECHNICAL SKILLS

**Languages**
Python, JavaScript, Go

**Frameworks**
React, Django, Flask

## EXPERIENCE

### Company Name

**Job Title**
Start Date - End Date
• Achievement with metrics
• Another achievement
**Technologies:** Python, AWS, Docker

### Earlier Experience

**Company 1** | Role | Dates
**Company 2** | Role | Dates

## EDUCATION

**Degree Name**
University Name | Year
```

See example resume files for complete formatting details.

## Troubleshooting

### "ModuleNotFoundError: No module named 'reportlab'"

Install reportlab:

```bash
pip install reportlab
```

### "python-dateutil not installed" Warning

This is optional. Install for automatic duration calculations:

```bash
pip install python-dateutil
```

### "Permission denied" Error

The output file may be open in another application. Close it and try again.

### "Input file not found" Error

Check that the markdown file exists and the path is correct. The script will suggest similar files in the directory.

## Using as a Library

You can also use this as a Python library:

```python
from modules import parse_markdown_resume, generate_pdf_from_data

# Read and parse markdown
with open("resume.md") as f:
    data = parse_markdown_resume(f.read())

# Generate PDF
generate_pdf_from_data(data, "output.pdf")
print("PDF created!")
```

## Distribution

To share this tool with others:

1. **Clone/Fork**: Others can clone this repo and customize their own `config.py`
2. **Package**: Create a Python package with setuptools (see `setup.py` if provided)
3. **Docker**: Run in a containerized environment for consistency
4. **Documentation**: Share `config.example.py` with usage examples

## Contributing

Contributions welcome! The modular architecture makes it easy to:

- Add new style templates
- Support additional markdown features
- Enhance PDF formatting
- Improve error handling

## License

MIT License - feel free to use and modify for your needs.

## Support

For issues or questions:

1. Check dependencies: `pip list | grep -E "reportlab|dateutil"`
2. Verify markdown format matches expected structure
3. Check `modules/config.py` for customization options
4. Review `config.example.py` for theme examples
