"""
Styles module for resume PDF generation.

Creates and manages ReportLab paragraph styles used throughout the resume.
All style properties are configured via the Config class.
"""

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from .config import Config


def create_custom_styles():
    """
    Create custom paragraph styles for the resume.

    Returns:
        StyleSheet: A complete set of styles configured from Config settings

    Styles created:
        - Name: Large centered name at top of resume
        - Subtitle: Job title/tagline below name
        - Contact: Contact information line
        - SectionHeader: Section titles (e.g., "Experience", "Education")
        - JobTitle: Job position titles
        - CompanyInfo: Company name, dates, location
        - ResumeBullet: Bullet points describing achievements
        - SkillCategory: Skill category headers (e.g., "Languages")
        - SkillList: List of skills in each category
        - Summary: Professional summary paragraph
    """
    styles = getSampleStyleSheet()

    # Name/Title style
    styles.add(
        ParagraphStyle(
            name="Name",
            parent=styles["Heading1"],
            fontSize=Config.FONT_SIZE_NAME,
            textColor=Config.PRIMARY_COLOR,
            spaceAfter=Config.SPACE_AFTER_NAME,
            alignment=TA_CENTER,
            fontName=Config.FONT_FAMILY_BOLD,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Subtitle",
            parent=styles["Normal"],
            fontSize=Config.FONT_SIZE_SUBTITLE,
            textColor=Config.ACCENT_COLOR,
            spaceAfter=Config.SPACE_AFTER_SUBTITLE,
            alignment=TA_CENTER,
            fontName=Config.FONT_FAMILY_BASE,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Contact",
            parent=styles["Normal"],
            fontSize=Config.FONT_SIZE_CONTACT,
            textColor=Config.LIGHT_GRAY,
            spaceAfter=Config.SPACE_AFTER_CONTACT,
            alignment=TA_CENTER,
            fontName=Config.FONT_FAMILY_BASE,
        )
    )

    # Section headers
    styles.add(
        ParagraphStyle(
            name="SectionHeader",
            parent=styles["Heading2"],
            fontSize=Config.FONT_SIZE_SECTION_HEADER,
            textColor=Config.PRIMARY_COLOR,
            spaceAfter=Config.SPACE_AFTER_SECTION_HEADER,
            spaceBefore=Config.SPACE_BEFORE_SECTION,
            fontName=Config.FONT_FAMILY_BOLD,
            borderWidth=Config.BORDER_WIDTH,
            borderColor=Config.PRIMARY_COLOR,
            borderPadding=0,
        )
    )

    # Job title
    styles.add(
        ParagraphStyle(
            name="JobTitle",
            parent=styles["Normal"],
            fontSize=Config.FONT_SIZE_JOB_TITLE,
            textColor=Config.DARK_GRAY,
            spaceAfter=Config.SPACE_AFTER_JOB_TITLE,
            fontName=Config.FONT_FAMILY_BOLD,
        )
    )

    # Company/dates
    styles.add(
        ParagraphStyle(
            name="CompanyInfo",
            parent=styles["Normal"],
            fontSize=Config.FONT_SIZE_COMPANY_INFO,
            textColor=Config.LIGHT_GRAY,
            spaceAfter=Config.SPACE_AFTER_COMPANY_INFO,
            fontName=Config.FONT_FAMILY_ITALIC,
        )
    )

    # Bullet points
    styles.add(
        ParagraphStyle(
            name="ResumeBullet",
            parent=styles["Normal"],
            fontSize=Config.FONT_SIZE_BULLET,
            textColor=Config.DARK_GRAY,
            spaceAfter=Config.SPACE_AFTER_BULLET,
            leftIndent=Config.BULLET_INDENT,
            fontName=Config.FONT_FAMILY_BASE,
            leading=Config.LEADING_BULLET,
        )
    )

    # Skills
    styles.add(
        ParagraphStyle(
            name="SkillCategory",
            parent=styles["Normal"],
            fontSize=Config.FONT_SIZE_SKILL_CATEGORY,
            textColor=Config.DARK_GRAY,
            spaceAfter=Config.SPACE_AFTER_SKILL_CATEGORY,
            fontName=Config.FONT_FAMILY_BOLD,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SkillList",
            parent=styles["Normal"],
            fontSize=Config.FONT_SIZE_SKILL_LIST,
            textColor=Config.DARK_GRAY,
            spaceAfter=Config.SPACE_AFTER_SKILL_LIST,
            fontName=Config.FONT_FAMILY_BASE,
            leading=Config.LEADING_SKILL_LIST,
        )
    )

    # Summary
    styles.add(
        ParagraphStyle(
            name="Summary",
            parent=styles["Normal"],
            fontSize=Config.FONT_SIZE_SUMMARY,
            textColor=Config.DARK_GRAY,
            spaceAfter=Config.SPACE_AFTER_SUMMARY,
            fontName=Config.FONT_FAMILY_BASE,
            leading=Config.LEADING_SUMMARY,
            alignment=TA_LEFT,
        )
    )

    return styles
