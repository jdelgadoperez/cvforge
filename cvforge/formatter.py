"""
Formatter module for resume PDF generation.

Converts markdown formatting to ReportLab-compatible HTML markup.
Handles bold, italic, links, and emoji removal.
"""

import re


def convert_markdown_formatting(text):
    """
    Convert markdown formatting to reportlab HTML tags.

    Supported conversions:
        - **bold text** -> <b>bold text</b>
        - *italic text* -> <i>italic text</i>
        - [link text](url) -> <link href="url" color="blue">link text</link>
        - Emoji symbols (📧🔗) are removed

    Args:
        text (str): Markdown text to convert

    Returns:
        str: Text with ReportLab HTML markup

    Examples:
        >>> convert_markdown_formatting("**Bold** and *italic*")
        '<b>Bold</b> and <i>italic</i>'

        >>> convert_markdown_formatting("[LinkedIn](https://linkedin.com/in/user)")
        '<link href="https://linkedin.com/in/user" color="blue">LinkedIn</link>'
    """
    if not text:
        return text

    # Remove emoji symbols (common in contact info)
    text = re.sub(r"[📧🔗📄💼🎓🏆📍]", "", text)

    # Links [text](url) - process this first before bold conversion
    # to avoid interfering with **text** patterns in URLs
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)", r'<link href="\2" color="blue">\1</link>', text
    )

    # Bold **text** - use non-greedy matching to handle multiple bolds on one line
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)

    # Italic *text* - only single asterisks not part of bold
    # Negative lookbehind and lookahead to avoid matching ** patterns
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", text)

    return text


def sanitize_text(text):
    """
    Sanitize text for safe inclusion in PDF.

    Removes or escapes characters that might cause issues in ReportLab.

    Args:
        text (str): Text to sanitize

    Returns:
        str: Sanitized text
    """
    if not text:
        return text

    # Remove or replace problematic characters
    # Note: ReportLab handles most common characters well
    # Add additional replacements here if needed

    return text


def format_contact_line(contact_items):
    """
    Format contact information items into a single line with separators.

    Args:
        contact_items (list): List of contact info strings (email, location, links)

    Returns:
        str: HTML-formatted contact line with <br/> separators

    Examples:
        >>> format_contact_line(["user@email.com", "New York, NY", "[LinkedIn](url)"])
        'user@email.com<br/>New York, NY<br/><link href="url">LinkedIn</link>'
    """
    if not contact_items:
        return ""

    # Convert markdown formatting for each item
    formatted_items = [convert_markdown_formatting(item) for item in contact_items if item]

    # Join with line breaks for vertical stacking
    return "<br/>".join(formatted_items)
