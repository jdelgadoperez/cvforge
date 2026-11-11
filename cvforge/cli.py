"""
Command-line interface for cvforge.

    cvforge build <input.md> [output.pdf] [--force]   render a markdown resume to PDF
    cvforge parse <input.md>                          print the parsed resume as JSON

Installed as the ``cvforge`` console script (see pyproject.toml); ``python -m cvforge``
and the legacy ``markdown_to_resume_pdf.py`` wrapper route here too.
"""

import argparse
import contextlib
import json
import sys

from . import __version__
from .config import Config
from .duration import warn_if_dateutil_unavailable
from .generator import generate_pdf_from_data
from .parser import parse_markdown_resume, validate_parsed_data
from .structured import to_structured
from .validators import (
    check_dependencies,
    check_output_file_overwrite,
    generate_output_filename,
    read_markdown_file,
    validate_file_extension,
    validate_input_file,
    validate_output_path,
)

KOFI_URL = "https://ko-fi.com/jessdp"


def _load_resume(input_file):
    """Resolve, read and parse ``input_file``. Returns (data, None) or (None, error message)."""
    is_valid, result = validate_input_file(input_file)
    if not is_valid:
        return None, result
    success, content = read_markdown_file(result)
    if not success:
        return None, content
    try:
        data = parse_markdown_resume(content)
    except Exception as e:  # parser is plain string handling; guard anyway
        return None, f"\n❌ Error parsing markdown: {e}"
    is_valid, error_msg = validate_parsed_data(data)
    if not is_valid:
        return None, f"\n❌ Error: {error_msg}"
    return data, None


def cmd_build(args):
    has_required, _, has_optional = check_dependencies()
    if not has_required:
        return 1
    if not has_optional:
        warn_if_dateutil_unavailable()

    input_file = args.input
    if not args.force and not validate_file_extension(input_file):
        return 0

    if args.output:
        # Explicit output path: don't use the configured outputs folder.
        output_file = validate_output_path(args.output)
    else:
        output_file = generate_output_filename(input_file, use_exports_folder=True)

    if not args.force and not check_output_file_overwrite(output_file):
        return 0

    print(f"\n🔄 Converting '{input_file}' to PDF...")
    try:
        data, error = _load_resume(input_file)
        if error:
            print(error)
            print("💡 Make sure your markdown file follows the expected resume format")
            return 1
        if not generate_pdf_from_data(data, output_file):
            return 1
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user")
        return 130
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("💡 Please check your markdown file format and try again")
        return 1

    print("\n✅ Resume PDF created successfully!")
    print(f"📄 Output: {output_file}")
    # Last line on screen, and only after a run that actually produced a PDF.
    print(f"\nIf this helped: {KOFI_URL}")
    return 0


def cmd_parse(args):
    # stdout carries only the JSON document; route any diagnostics to stderr.
    with contextlib.redirect_stdout(sys.stderr):
        data, error = _load_resume(args.input)
    if error:
        print(error.strip(), file=sys.stderr)
        return 1
    indent = None if args.compact else 2
    json.dump(to_structured(data), sys.stdout, indent=indent, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        prog="cvforge",
        description="Convert a markdown resume to a styled PDF, or to structured JSON.",
        epilog=f"Customize colors, fonts and spacing in cvforge/config.py. "
        f"Inputs are also looked up in '{Config.INPUTS_FOLDER}/'.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", metavar="<command>")

    build = sub.add_parser(
        "build",
        help="render a markdown resume to PDF",
        description="Render a markdown resume to PDF. Without an output path the PDF is "
        f"written to the configured outputs folder ('{Config.OUTPUTS_FOLDER}/').",
    )
    build.add_argument("input", help="markdown resume (.md)")
    build.add_argument("output", nargs="?", help="output PDF path ('.pdf' added if missing)")
    build.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="overwrite an existing PDF and accept a non-.md input without prompting",
    )
    build.set_defaults(func=cmd_build)

    parse = sub.add_parser(
        "parse",
        help="print the parsed resume as JSON (schema_version 1)",
        description="Print the parsed resume structure as JSON on stdout. "
        "Diagnostics go to stderr; exit status is non-zero on failure.",
    )
    parse.add_argument("input", help="markdown resume (.md)")
    parse.add_argument("--compact", action="store_true", help="emit single-line JSON")
    parse.set_defaults(func=cmd_parse)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help(sys.stderr)
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
