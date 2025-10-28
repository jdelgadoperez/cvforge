"""
Generator module for resume PDF generation.

Core PDF generation logic using ReportLab.
Handles document creation, section rendering, and layout.
"""

import re
import sys
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
)

from .config import Config
from .styles import create_custom_styles
from .formatter import convert_markdown_formatting, format_contact_line
from .duration import calculate_duration


def create_section_divider():
    """
    Create a horizontal divider line for section headers.

    Returns:
        Table: ReportLab Table object configured as a divider line
    """
    line_table = Table([[""]], colWidths=[Config.DIVIDER_WIDTH])
    line_table.setStyle(
        TableStyle(
            [
                ("LINEABOVE", (0, 0), (-1, 0), Config.DIVIDER_THICKNESS, Config.DIVIDER_COLOR),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return line_table


def render_header(story, data, styles):
    """
    Render resume header with name, title, and contact info.

    Args:
        story (list): ReportLab story list to append elements to
        data (dict): Parsed resume data
        styles: ReportLab StyleSheet with custom styles
    """
    # Name
    story.append(Paragraph(data["name"], styles["Name"]))

    # Title/tagline
    story.append(Paragraph(data["title"], styles["Subtitle"]))

    # Contact info
    contact_text = format_contact_line(data["contact"])
    story.append(Paragraph(contact_text, styles["Contact"]))


def render_summary_section(story, section, styles):
    """
    Render professional summary section.

    Args:
        story (list): ReportLab story list to append elements to
        section (dict): Section data with name and content
        styles: ReportLab StyleSheet with custom styles
    """
    section_group = []

    # Section header and divider
    section_group.append(Paragraph(section["name"], styles["SectionHeader"]))
    section_group.append(create_section_divider())

    # Summary text - join all content into a paragraph
    summary_text = " ".join(section["content"])
    section_group.append(
        Paragraph(convert_markdown_formatting(summary_text), styles["Summary"])
    )

    # Keep summary together if configured
    if Config.KEEP_SECTIONS_TOGETHER:
        story.append(KeepTogether(section_group))
    else:
        story.extend(section_group)


def render_skills_section(story, section, styles):
    """
    Render skills section with categories and skill lists.

    Args:
        story (list): ReportLab story list to append elements to
        section (dict): Section data with name and content
        styles: ReportLab StyleSheet with custom styles
    """
    # Header and divider
    section_group = []
    section_group.append(Paragraph(section["name"], styles["SectionHeader"]))
    section_group.append(create_section_divider())

    if Config.KEEP_SECTIONS_TOGETHER:
        story.append(KeepTogether(section_group))
    else:
        story.extend(section_group)

    # Skills content
    for line in section["content"]:
        line = line.strip()
        if not line:
            continue

        if line.startswith("**") and line.endswith("**"):
            # Category header (e.g., **Languages**)
            category = line[2:-2].strip()
            if category:
                story.append(Paragraph(f"<b>{category}</b>", styles["SkillCategory"]))
        elif not line.startswith("**"):
            # Skills list
            converted = convert_markdown_formatting(line)
            if converted.strip():
                story.append(Paragraph(converted, styles["SkillList"]))


def render_experience_entry(story, subsection, styles):
    """
    Render a single experience entry (company with job details).

    Args:
        story (list): ReportLab story list to append elements to
        subsection (dict): Subsection data with company name and lines
        styles: ReportLab StyleSheet with custom styles
    """
    company = subsection["name"]

    # Special handling for "Earlier Experience" subsection
    if "Earlier" in company and "Experience" in company:
        render_earlier_experience(story, subsection, styles)
        return

    # Regular experience entry
    company_clean = company.replace("**", "")
    story.append(Paragraph(f"<b>{company_clean}</b>", styles["JobTitle"]))

    job_title = None
    dates = None
    bullets = []
    tech_line = None

    for i, line in enumerate(subsection["lines"]):
        line = line.strip()
        if not line:
            continue

        # First non-bullet line is likely the job title (starts with **)
        if job_title is None and line.startswith("**") and not line.startswith("•"):
            job_title = convert_markdown_formatting(line)
            # Check if next line is the dates
            if i + 1 < len(subsection["lines"]):
                next_line = subsection["lines"][i + 1].strip()
                if (
                    next_line
                    and not next_line.startswith("**")
                    and not next_line.startswith("•")
                ):
                    # Remove any existing duration in parentheses
                    dates_clean = re.sub(r"\s*\([^)]*\)\s*$", "", next_line).strip()
                    # Calculate duration
                    duration = calculate_duration(dates_clean)
                    # Combine dates with calculated duration
                    dates = f"{dates_clean} {duration}".strip()
            continue

        # Skip the dates line (already captured)
        if dates and line_matches_dates(line, dates):
            continue

        if line.startswith("•"):
            # Bullet point
            bullets.append(convert_markdown_formatting(line))
        elif (
            "Technologies:" in line or "Tech used:" in line or line.startswith("**Tech")
        ):
            # Technologies line
            tech_line = convert_markdown_formatting(line)

    # Add job title and dates
    if job_title and dates:
        combined_info = f"{job_title} | {dates}"
        story.append(Paragraph(combined_info, styles["CompanyInfo"]))
    elif job_title:
        story.append(Paragraph(job_title, styles["CompanyInfo"]))

    # Add bullets
    for bullet in bullets:
        if bullet.strip():
            story.append(Paragraph(bullet, styles["ResumeBullet"]))

    # Add tech line
    if tech_line and tech_line.strip():
        story.append(Paragraph(tech_line, styles["CompanyInfo"]))

    story.append(Spacer(1, 8))


def render_earlier_experience(story, subsection, styles):
    """
    Render "Earlier Experience" section with condensed entries.

    Parses lines in format: **Company** | Title | Dates
    Adds duration calculation to the dates.

    Args:
        story (list): ReportLab story list to append elements to
        subsection (dict): Subsection data with earlier experience entries
        styles: ReportLab StyleSheet with custom styles
    """
    company = subsection["name"]
    company_clean = company.replace("**", "")

    # Collect all Earlier Experience items in a group
    earlier_exp_group = []
    earlier_exp_group.append(Spacer(1, 12))  # Add space before
    earlier_exp_group.append(Paragraph(f"<b>{company_clean}</b>", styles["JobTitle"]))

    # Each line is a separate job entry (format: **Company** | Title | Dates)
    for line in subsection["lines"]:
        line = line.strip()
        if not line:
            continue
        if line.startswith("**") and "|" in line:
            # Parse the line to extract dates and add duration
            parts = line.split("|")
            if len(parts) >= 3:
                # Format: **Company** | Title | Dates
                company_part = parts[0].strip()
                title_part = parts[1].strip()
                dates_part = parts[2].strip()

                # Remove any existing duration in parentheses
                dates_clean = re.sub(r"\s*\([^)]*\)\s*$", "", dates_part).strip()

                # Calculate duration
                duration = calculate_duration(dates_clean)

                # Rebuild the line with duration
                if duration:
                    line_with_duration = f"{company_part} | {title_part} | {dates_clean} {duration}"
                else:
                    line_with_duration = line

                converted = convert_markdown_formatting(line_with_duration)
            else:
                # Fallback if format doesn't match expected pattern
                converted = convert_markdown_formatting(line)

            if converted.strip():
                earlier_exp_group.append(Paragraph(converted, styles["ResumeBullet"]))
                earlier_exp_group.append(Spacer(1, 4))

    earlier_exp_group.append(Spacer(1, 6))

    # Keep the entire Earlier Experience block together
    if Config.KEEP_SECTIONS_TOGETHER:
        story.append(KeepTogether(earlier_exp_group))
    else:
        story.extend(earlier_exp_group)


def render_experience_section(story, section, styles):
    """
    Render experience section with all job entries.

    Args:
        story (list): ReportLab story list to append elements to
        section (dict): Section data with subsections for each company
        styles: ReportLab StyleSheet with custom styles
    """
    # Header and divider
    section_group = []
    section_group.append(Paragraph(section["name"], styles["SectionHeader"]))
    section_group.append(create_section_divider())

    if Config.KEEP_SECTIONS_TOGETHER:
        story.append(KeepTogether(section_group))
    else:
        story.extend(section_group)

    # Experience entries
    for subsection in section["subsections"]:
        render_experience_entry(story, subsection, styles)


def render_generic_section(story, section, styles):
    """
    Render a generic section (education, certifications, etc.).

    Args:
        story (list): ReportLab story list to append elements to
        section (dict): Section data with name and content
        styles: ReportLab StyleSheet with custom styles
    """
    section_group = []

    # Section header and divider
    section_group.append(Paragraph(section["name"], styles["SectionHeader"]))
    section_group.append(create_section_divider())

    content_items = []

    for line in section["content"]:
        line = line.strip()
        if not line:
            continue

        # Check for company | title format (like Earlier Experience)
        if line.startswith("**") and "|" in line and not line.startswith("•"):
            # Format: **Company** | Title | Dates (all on one line)
            # Parse and add duration if possible
            parts = line.split("|")
            if len(parts) >= 3:
                company_part = parts[0].strip()
                title_part = parts[1].strip()
                dates_part = parts[2].strip()

                # Remove any existing duration in parentheses
                dates_clean = re.sub(r"\s*\([^)]*\)\s*$", "", dates_part).strip()

                # Calculate duration
                duration = calculate_duration(dates_clean)

                # Rebuild the line with duration
                if duration:
                    line_with_duration = f"{company_part} | {title_part} | {dates_clean} {duration}"
                else:
                    line_with_duration = line

                converted = convert_markdown_formatting(line_with_duration)
            else:
                # Fallback if format doesn't match expected pattern
                converted = convert_markdown_formatting(line)

            if converted.strip():
                content_items.append(Paragraph(converted, styles["ResumeBullet"]))
                content_items.append(Spacer(1, 6))
        elif line.startswith("•") or line.startswith("-"):
            # Bullet point
            converted = convert_markdown_formatting(line)
            if converted.strip():
                content_items.append(Paragraph(converted, styles["ResumeBullet"]))
        elif line.startswith("**") and line.endswith("**"):
            # Standalone bolded title
            clean_title = line.replace("**", "").strip()
            content_items.append(Paragraph(f"<b>{clean_title}</b>", styles["JobTitle"]))
        else:
            # Regular text
            converted = convert_markdown_formatting(line)
            if converted.strip():
                content_items.append(Paragraph(converted, styles["SkillList"]))

    # Keep short sections together (Education, Certifications, etc.)
    if should_keep_section_together(section["name"]):
        section_group.extend(content_items)
        section_group.append(Spacer(1, 6))
        story.append(KeepTogether(section_group))
    else:
        # For longer sections, add header then content separately
        story.extend(section_group)
        story.extend(content_items)
        story.append(Spacer(1, 6))


def should_keep_section_together(section_name):
    """
    Determine if a section should be kept together on one page.

    Args:
        section_name (str): Name of the section

    Returns:
        bool: True if section should be kept together, False otherwise
    """
    if not Config.KEEP_SECTIONS_TOGETHER:
        return False

    # Short sections that should stay together
    keep_together_keywords = ["EDUCATION", "CERTIFICATION", "AWARD", "HONOR"]
    return any(keyword in section_name.upper() for keyword in keep_together_keywords)


def line_matches_dates(line, dates):
    """
    Check if a line matches the dates string (to avoid duplicate rendering).

    Args:
        line (str): Line to check
        dates (str): Dates string with optional duration

    Returns:
        bool: True if line matches dates, False otherwise
    """
    if not dates:
        return False

    # Remove duration from both strings for comparison
    line_clean = re.sub(r"\s*\([^)]*\)\s*$", "", line).strip()
    dates_clean = re.sub(r"\s*\([^)]*\)\s*$", "", dates).strip()

    return line_clean == dates_clean


def generate_pdf_from_data(data, output_file):
    """
    Generate PDF resume from parsed data.

    Args:
        data (dict): Parsed resume data from parser.parse_markdown_resume()
        output_file (str): Path to output PDF file

    Returns:
        bool: True if successful, False otherwise

    Raises:
        PermissionError: If output file cannot be written
        Exception: For other PDF generation errors
    """
    # Create document
    doc = SimpleDocTemplate(
        output_file,
        pagesize=Config.PAGE_SIZE,
        rightMargin=Config.MARGIN_RIGHT,
        leftMargin=Config.MARGIN_LEFT,
        topMargin=Config.MARGIN_TOP,
        bottomMargin=Config.MARGIN_BOTTOM,
    )

    # Container for content
    story = []
    styles = create_custom_styles()

    # Render header
    render_header(story, data, styles)

    # Process sections
    for section in data["sections"]:
        section_name = section["name"]

        # Route to appropriate renderer based on section type
        if "SUMMARY" in section_name.upper() or "PROFESSIONAL SUMMARY" in section_name.upper():
            render_summary_section(story, section, styles)
        elif "SKILL" in section_name.upper():
            render_skills_section(story, section, styles)
        elif "EXPERIENCE" in section_name.upper():
            render_experience_section(story, section, styles)
        else:
            # Generic section (education, certifications, etc.)
            render_generic_section(story, section, styles)

    # Build PDF
    try:
        doc.build(story)
        return True
    except PermissionError:
        print(f"\n❌ Error: Permission denied writing to '{output_file}'")
        print(f"💡 Make sure the file isn't open in another application")
        return False
    except Exception as e:
        print(f"\n❌ Error creating PDF: {e}")
        return False
