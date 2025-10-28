#!/usr/bin/env python3
"""
Convert a markdown resume to a professional PDF with color design

Usage:
    python3 markdown_to_resume_pdf.py input.md [output.pdf]

Requirements:
    pip install reportlab python-dateutil

Customization:
    Edit modules/config.py to customize colors, fonts, spacing, and more.
    See README.md for detailed customization instructions.

Examples:
    python3 markdown_to_resume_pdf.py resume.md
    python3 markdown_to_resume_pdf.py resume.md my_resume.pdf
"""

import sys

# Import modular components
from modules import (
    check_dependencies,
    warn_if_dateutil_unavailable,
    validate_input_file,
    validate_file_extension,
    check_output_file_overwrite,
    read_markdown_file,
    validate_output_path,
    generate_output_filename,
    parse_markdown_resume,
    validate_parsed_data,
    generate_pdf_from_data,
)

# Check for required and optional dependencies
has_required, missing_deps, has_optional = check_dependencies()
if not has_required:
    sys.exit(1)

# Warn about optional dependencies
if not has_optional:
    warn_if_dateutil_unavailable()


def create_resume_from_markdown(md_file, output_file):
    """
    Generate PDF resume from markdown file.

    This is a simplified wrapper that uses the modular components.

    Args:
        md_file (str): Path to input markdown file (may be updated to resolved path)
        output_file (str): Path to output PDF file

    Returns:
        tuple: (resolved_input_path, final_output_path) if successful
    """
    # Validate input file (may resolve to alternate location)
    is_valid, result = validate_input_file(md_file)
    if not is_valid:
        print(result)  # result contains error message
        sys.exit(1)

    # Update md_file to the resolved path
    md_file = result

    # Read markdown file
    success, result = read_markdown_file(md_file)
    if not success:
        print(result)  # result contains error message
        sys.exit(1)

    md_content = result

    # Parse markdown
    try:
        data = parse_markdown_resume(md_content)
    except Exception as e:
        print(f"\n❌ Error parsing markdown: {e}")
        print(f"💡 Make sure your markdown file follows the expected resume format")
        sys.exit(1)

    # Validate parsed data
    is_valid, error_msg = validate_parsed_data(data)
    if not is_valid:
        print(f"\n❌ Error: {error_msg}")
        sys.exit(1)

    # Generate PDF
    success = generate_pdf_from_data(data, output_file)
    if success:
        print(f"\n✅ Resume PDF created successfully!")
        print(f"📄 Output: {output_file}")
        return md_file, output_file
    else:
        sys.exit(1)


def main():
    """Main entry point for the resume generator."""
    from modules.config import Config

    if len(sys.argv) < 2:
        print("\n📄 Markdown to PDF Resume Converter")
        print("=" * 50)
        print("\n❌ Error: No input file specified")
        print("\n💡 Usage:")
        print("   python3 markdown_to_resume_pdf.py <input.md> [output.pdf]")
        print("\n📝 Examples:")
        print("   python3 markdown_to_resume_pdf.py resume.md")
        print("   python3 markdown_to_resume_pdf.py resume.md my_resume.pdf")
        print("\n🎨 Customization:")
        print("   Edit modules/config.py to customize colors, fonts, and spacing")

        # Show configured folders if they exist
        if Config.INPUTS_FOLDER:
            print(f"\n📁 Configured inputs folder: {Config.INPUTS_FOLDER}")
        if Config.OUTPUTS_FOLDER:
            print(f"📁 Configured exports folder: {Config.OUTPUTS_FOLDER}")
            print("   (PDFs will be saved here by default)")

        sys.exit(1)

    input_file = sys.argv[1]

    # Validate input file extension
    if not validate_file_extension(input_file):
        sys.exit(0)

    # Determine output file
    user_specified_output = len(sys.argv) > 2

    if user_specified_output:
        # User specified output path - don't use exports folder
        output_file = sys.argv[2]
        # Validate and normalize output file path
        output_file = validate_output_path(output_file)
    else:
        # No output specified - use exports folder from config if configured
        # Note: input_file might not exist yet, so we use the original filename
        output_file = generate_output_filename(input_file, use_exports_folder=True)

    # Check if output file will be overwritten
    if not check_output_file_overwrite(output_file):
        sys.exit(0)

    print(f"\n🔄 Converting '{input_file}' to PDF...")

    try:
        create_resume_from_markdown(input_file, output_file)
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print(f"💡 Please check your markdown file format and try again")
        sys.exit(1)


if __name__ == "__main__":
    main()
