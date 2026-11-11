"""
Parser module for resume PDF generation.

Parses markdown resume files into structured data.
Handles name, title, contact info, and section parsing.
"""


def parse_markdown_resume(md_content):
    """
    Parse markdown resume into structured data dictionary.

    Expected markdown structure:
        # Name
        **Job Title**
        Contact info lines (email, location, links)

        ## SECTION NAME
        Section content...

        ### Subsection (e.g., Company Name)
        Subsection content...

    Args:
        md_content (str): Raw markdown content from resume file

    Returns:
        dict: Structured resume data with keys:
            - name (str): Person's full name
            - title (str): Job title/tagline
            - contact (list): List of contact info strings
            - sections (list): List of section dictionaries, each with:
                - name (str): Section name
                - content (list): Lines of content
                - subsections (list): List of subsection dicts with name and lines

    Example structure:
        {
            "name": "John Doe",
            "title": "Senior Software Engineer",
            "contact": ["john@email.com", "San Francisco, CA"],
            "sections": [
                {
                    "name": "SUMMARY",
                    "content": ["Professional summary text..."],
                    "subsections": []
                },
                {
                    "name": "EXPERIENCE",
                    "content": [],
                    "subsections": [
                        {
                            "name": "Company Name",
                            "lines": ["**Senior Engineer**", "2020 - Present", "• Achievement 1"]
                        }
                    ]
                }
            ]
        }
    """
    lines = md_content.split("\n")
    data = {"name": "", "title": "", "contact": [], "sections": []}

    current_section = None
    current_subsection = None
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines and separators
        if not line or line == "---":
            i += 1
            continue

        # Name (first # heading)
        if line.startswith("# ") and not data["name"]:
            data["name"] = line[2:].strip()
            i += 1
            continue

        # Title/subtitle (first ** line after name)
        if line.startswith("**") and line.endswith("**") and not data["title"]:
            data["title"] = line[2:-2].strip()
            i += 1
            continue

        # Contact info (before any section starts)
        # Common patterns: email (@), location names, links (linkedin, github, website)
        if not current_section and (
            "@" in line
            or "linkedin.com" in line.lower()
            or "github.com" in line.lower()
            or "LinkedIn" in line
            or "GitHub" in line
            or "Website" in line
            or "Portfolio" in line
            or any(
                location in line
                for location in [
                    "Florida",
                    "California",
                    "New York",
                    "Texas",
                    "USA",
                    "Remote",
                ]
            )
        ):
            if line:  # Only add non-empty contact lines
                data["contact"].append(line)
            i += 1
            continue

        # Section headers (## SECTION NAME)
        if line.startswith("## "):
            section_name = line[3:].strip()
            current_section = {"name": section_name, "content": [], "subsections": []}
            data["sections"].append(current_section)
            current_subsection = None
            i += 1
            continue

        # Subsection headers (### Company Name, ### Degree, etc.)
        if line.startswith("### "):
            subsection_name = line[4:].strip()
            current_subsection = {"name": subsection_name, "lines": []}
            if current_section:
                current_section["subsections"].append(current_subsection)
            i += 1
            continue

        # Add content to current context (only if non-empty)
        if line and line.strip():
            if current_subsection:
                current_subsection["lines"].append(line)
            elif current_section:
                current_section["content"].append(line)

        i += 1

    return data


def validate_parsed_data(data):
    """
    Validate that parsed resume data contains required fields.

    Args:
        data (dict): Parsed resume data from parse_markdown_resume()

    Returns:
        tuple: (is_valid: bool, error_message: str)

    Examples:
        >>> validate_parsed_data({"name": "John", "title": "Engineer", "contact": [], "sections": []})
        (True, "")

        >>> validate_parsed_data({"name": "", "title": "", "contact": [], "sections": []})
        (False, "Resume must contain a name (# Name)")
    """
    if not data.get("name"):
        return False, "Resume must contain a name (# Name)"

    if not data.get("title"):
        return False, "Resume must contain a title (**Your Title**)"

    if not data.get("sections"):
        return False, "Resume must contain at least one section (## SECTION NAME)"

    return True, ""
