"""
Duration calculation module for resume PDF generation.

Handles parsing date strings and calculating durations between dates.
Requires python-dateutil package (optional).
"""

import re
from datetime import datetime

# Try to import dateutil for automatic duration calculation (optional)
try:
    from dateutil import parser as date_parser
    from dateutil.relativedelta import relativedelta

    DATEUTIL_AVAILABLE = True
except ImportError:
    DATEUTIL_AVAILABLE = False

from .config import Config


def is_dateutil_available():
    """
    Check if python-dateutil is available for duration calculations.

    Returns:
        bool: True if dateutil is installed, False otherwise
    """
    return DATEUTIL_AVAILABLE


def calculate_duration(date_string):
    """
    Calculate duration from a date string like 'December 2023 - Present' or 'June 2018 - September 2021'.

    Args:
        date_string (str): A date range string with start and end dates separated by -, --, or |

    Returns:
        str: Formatted duration string like '(1 year 11 months)' or '(3 years 4 months)',
             or empty string if calculation is disabled, dateutil unavailable, or parsing fails

    Examples:
        >>> calculate_duration("December 2023 - Present")
        "(1 year 2 months)"

        >>> calculate_duration("June 2018 - September 2021")
        "(3 years 4 months)"

        >>> calculate_duration("March 2024 - April 2024")
        "(1 month)"
    """
    # Check if duration calculation is enabled in config
    if not Config.CALCULATE_DURATIONS:
        return ""

    # Check if dateutil is available
    if not DATEUTIL_AVAILABLE:
        return ""

    try:
        # Split on various separators (-, --, em-dash, en-dash, pipe)
        parts = re.split(r"\s*[-–—|]\s*", date_string)
        if len(parts) != 2:
            return ""

        start_str, end_str = parts

        # Parse start date
        try:
            start_date = date_parser.parse(start_str, fuzzy=True)
        except:
            return ""

        # Parse end date (handle "Present" as today)
        if "present" in end_str.lower() or "current" in end_str.lower():
            end_date = datetime.now()
        else:
            try:
                end_date = date_parser.parse(end_str, fuzzy=True)
            except:
                return ""

        # Calculate difference
        delta = relativedelta(end_date, start_date)

        years = delta.years
        months = delta.months

        # Format duration string
        parts = []
        if years > 0:
            parts.append(f"{years} year{'s' if years != 1 else ''}")
        if months > 0:
            parts.append(f"{months} month{'s' if months != 1 else ''}")

        if not parts:
            # Less than a month
            return "(less than 1 month)"

        return f"({' '.join(parts)})"

    except Exception:
        # If anything goes wrong, return empty string
        return ""


def warn_if_dateutil_unavailable():
    """
    Print a warning message if python-dateutil is not installed.

    This should be called at the start of the program to inform users
    about missing optional functionality.
    """
    if not DATEUTIL_AVAILABLE:
        print("\n⚠️  Optional: python-dateutil not installed")
        print("💡 Duration calculation will be skipped (e.g., '1 year 10 months')")
        print("   Install with: pip install python-dateutil")
        print("   (Resume will still be generated)\n")
