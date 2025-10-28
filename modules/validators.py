"""
Validators module for resume PDF generation.

Handles file validation, error checking, and helpful error messages.
"""

import os
import sys


def validate_input_file(md_file):
    """
    Validate that the input markdown file exists and is readable.

    If file is not found locally, also checks Config.INPUTS_FOLDER.

    Args:
        md_file (str): Path to markdown file

    Returns:
        tuple: (is_valid: bool, resolved_path: str or error_message: str)
            If valid, returns (True, full_path_to_file)
            If invalid, returns (False, error_message)

    Side effects:
        Prints helpful suggestions if file not found
    """
    from .config import Config

    # Check if input file exists at the given path
    if os.path.exists(md_file):
        return True, os.path.abspath(md_file)

    # If not found and path is relative, try INPUTS_FOLDER from config
    if not os.path.isabs(md_file) and Config.INPUTS_FOLDER:
        inputs_folder = os.path.expanduser(Config.INPUTS_FOLDER)
        alternate_path = os.path.join(inputs_folder, md_file)

        if os.path.exists(alternate_path):
            print(f"\n💡 Found file in inputs folder: {alternate_path}")
            return True, os.path.abspath(alternate_path)

    # File not found - generate helpful error message
    error_msg = f"\n❌ Error: Input file not found: '{md_file}'"

    # Try to find similar files
    dir_path = os.path.dirname(md_file) or "."
    filename = os.path.basename(md_file)

    search_dirs = [dir_path]

    # Also search in inputs folder if configured
    if Config.INPUTS_FOLDER:
        inputs_folder = os.path.expanduser(Config.INPUTS_FOLDER)
        if os.path.exists(inputs_folder):
            search_dirs.append(inputs_folder)

    for search_dir in search_dirs:
        try:
            md_files = [f for f in os.listdir(search_dir) if f.endswith(".md")]
            if md_files:
                error_msg += f"\n\n💡 Found .md files in '{search_dir}':"
                for f in md_files[:5]:  # Show up to 5 suggestions
                    error_msg += f"\n   - {f}"
        except Exception:
            pass

    error_msg += (
        f"\n\n💡 Usage: python3 markdown_to_resume_pdf.py <input.md> [output.pdf]"
    )

    return False, error_msg


def validate_file_extension(input_file, expected_ext=".md"):
    """
    Validate that input file has the expected extension.

    Args:
        input_file (str): Path to input file
        expected_ext (str): Expected file extension (default: ".md")

    Returns:
        bool: True if extension matches or user confirms to continue, False otherwise
    """
    if not input_file.endswith(expected_ext):
        print(
            f"\n⚠️  Warning: Input file '{input_file}' doesn't have {expected_ext} extension"
        )
        print(f"💡 Expected a markdown file ({expected_ext})")
        response = input("Continue anyway? (y/n): ").lower()
        if response != "y":
            print("Cancelled.")
            return False

    return True


def check_output_file_overwrite(output_file):
    """
    Check if output file exists and prompt user for overwrite confirmation.

    Args:
        output_file (str): Path to output PDF file

    Returns:
        bool: True if user confirms overwrite or file doesn't exist, False otherwise
    """
    if os.path.exists(output_file):
        print(f"\n⚠️  Warning: Output file '{output_file}' already exists")
        response = input("Overwrite? (y/n): ").lower()
        if response != "y":
            print("Cancelled.")
            return False

    return True


def read_markdown_file(md_file):
    """
    Read and validate markdown file content.

    Args:
        md_file (str): Path to markdown file

    Returns:
        tuple: (success: bool, content: str or error_message: str)

    Examples:
        >>> success, content = read_markdown_file("resume.md")
        >>> if success:
        ...     print(f"Read {len(content)} characters")
    """
    try:
        with open(md_file, "r", encoding="utf-8") as f:
            md_content = f.read()
    except PermissionError:
        return (
            False,
            f"\n❌ Error: Permission denied reading '{md_file}'\n💡 Check file permissions and try again",
        )
    except Exception as e:
        return False, f"\n❌ Error reading file '{md_file}': {e}"

    if not md_content.strip():
        return False, f"\n❌ Error: Input file '{md_file}' is empty"

    return True, md_content


def validate_output_path(output_file):
    """
    Validate that output file path is writable and has correct extension.

    Args:
        output_file (str): Path to output file

    Returns:
        str: Validated output path (adds .pdf extension if missing)
    """
    # Add .pdf extension if missing
    if not output_file.endswith(".pdf"):
        output_file += ".pdf"

    # Check if directory is writable (if directory specified)
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        print(f"\n⚠️  Warning: Output directory '{output_dir}' does not exist")
        print("💡 The directory will be created if possible")

    return output_file


def check_dependencies():
    """
    Check for required and optional dependencies.

    Returns:
        tuple: (has_required: bool, missing_required: list, has_optional: bool)

    Side effects:
        Prints error messages for missing required dependencies
        Prints warnings for missing optional dependencies
    """
    missing_required = []

    # Check for reportlab (required)
    try:
        import reportlab
    except ImportError:
        missing_required.append("reportlab")

    # Handle missing required dependencies
    if missing_required:
        print("\n❌ Error: Required dependencies not installed\n")
        print("Missing packages:")
        for dep in missing_required:
            print(f"  - {dep}")
        print("\n💡 Install with:")
        print(f"   pip install {' '.join(missing_required)}")
        print("\nOr install all dependencies at once:")
        print("   pip install reportlab python-dateutil")
        return False, missing_required, False

    # Check for dateutil (optional)
    try:
        import dateutil

        has_dateutil = True
    except ImportError:
        has_dateutil = False

    return True, [], has_dateutil


def generate_output_filename(input_file, use_exports_folder=True):
    """
    Generate output PDF filename from input markdown filename.

    Args:
        input_file (str): Path to input markdown file
        use_exports_folder (bool): If True, uses Config.EXPORTS_FOLDER for output path

    Returns:
        str: Output PDF filename (same name as input, with .pdf extension)
             If use_exports_folder=True and EXPORTS_FOLDER is set, places file there

    Examples:
        >>> generate_output_filename("resume.md", use_exports_folder=False)
        'resume.pdf'

        >>> generate_output_filename("/path/to/my_resume.md", use_exports_folder=False)
        '/path/to/my_resume.pdf'
    """
    import os
    from .config import Config

    # Get base filename without extension
    base_name = os.path.basename(input_file).rsplit(".", 1)[0]
    pdf_name = base_name + ".pdf"

    # Check if we should use exports folder from config
    if use_exports_folder and Config.OUTPUTS_FOLDER:
        exports_folder = os.path.expanduser(Config.OUTPUTS_FOLDER)

        # Create exports folder if it doesn't exist
        if not os.path.exists(exports_folder):
            try:
                os.makedirs(exports_folder, exist_ok=True)
            except Exception as e:
                print(
                    f"\n⚠️  Warning: Could not create exports folder '{exports_folder}': {e}"
                )
                print(f"💡 Saving to current directory instead")
                return pdf_name

        return os.path.join(exports_folder, pdf_name)

    # Default: save in same directory as input file
    input_dir = os.path.dirname(input_file)
    if input_dir:
        return os.path.join(input_dir, pdf_name)

    return pdf_name
