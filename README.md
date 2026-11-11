# cvforge

Turn a markdown resume into a clean, customizable PDF — or into structured JSON that other
tools can consume.

## Quick Start

```bash
uv sync                                            # install dependencies + the cvforge CLI
uv run cvforge build inputs/test_resume.md         # -> outputs/test_resume.pdf
uv run cvforge parse inputs/test_resume.md         # -> JSON on stdout
```

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

## Usage

### `cvforge build` — markdown to PDF

```bash
uv run cvforge build <input.md> [output.pdf] [--force]
```

- With no output path, the PDF is written to the configured outputs folder
  (`Config.OUTPUTS_FOLDER`, default `outputs/` under the current directory) with the input's name.
- With an output path, the PDF goes exactly there (`.pdf` is appended if missing).
- If the input isn't found at the given path, it is also looked up in `Config.INPUTS_FOLDER`
  (default `inputs/`), so `uv run cvforge build test_resume.md` works too.
- Existing output files trigger an overwrite prompt; `--force` (`-f`) skips it (and the prompt for
  a non-`.md` input).

The legacy entry point still works and is equivalent:

```bash
uv run python markdown_to_resume_pdf.py <input.md> [output.pdf]
```

### `cvforge parse` — markdown to JSON

```bash
uv run cvforge parse <input.md> [--compact]
```

Prints the parsed resume as JSON on stdout (pretty-printed; `--compact` for one line).
Diagnostics go to stderr, and the exit status is non-zero if the file is missing or isn't a valid
resume (it needs a `# Name`, a `**Title**` and at least one `## SECTION`).

`uv run cvforge --help` / `uv run cvforge <command> --help` list all options; `python -m cvforge`
works as well.

## `parse` JSON shape (schema_version 1)

This output is a contract consumed by other tools (e.g. to build a skill profile). Adding keys
keeps `schema_version`; removing/renaming a key or changing a value's type bumps it. All strings are
plain text: markdown emphasis, links and contact emoji are stripped.

| Key              | Type                                                      | Notes                                                                                                                       |
| ---------------- | --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `schema_version` | `1`                                                       |                                                                                                                             |
| `name`           | string                                                    | the `# Name` heading                                                                                                        |
| `title`          | string                                                    | the first `**Title**` line                                                                                                  |
| `contact`        | `{items: string[], email: string\|null, links: {label, url}[]}` | `items` are the `\|`-separated pieces of the contact lines                                                         |
| `summary`        | string                                                    | `SUMMARY` / `PROFILE` / `OBJECTIVE` / `ABOUT` sections joined; `""` if none                                                 |
| `skills`         | `{category: string\|null, items: string[]}[]`             | `SKILL*` sections; comma/semicolon lists split and trimmed (commas inside parentheses kept), de-duplicated per category     |
| `experience`     | `Job[]`                                                   | `EXPERIENCE` / `EMPLOYMENT` / `WORK HISTORY` sections                                                                       |
| `education`      | `{degree, institution, year, details: string[]}[]`        | `institution` / `year` may be `null`                                                                                        |
| `certifications` | `{name, issuer, year, details: string[]}[]`               | `CERTIF*` sections; `issuer` / `year` may be `null`                                                                         |
| `other_sections` | `{name: string, lines: string[]}[]`                       | any other `##` section, lines as plain text                                                                                 |
| `all_skills`     | string[]                                                  | every skill item then every job technology, de-duplicated case-insensitively, first spelling wins                          |

`Job` is:

| Key            | Type                                                                | Notes                                                                                     |
| -------------- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `company`      | string \| null                                                      | the `### Company` heading (for condensed entries, the second `\|` field)                  |
| `role`         | string \| null                                                      | the `**Role**` line                                                                       |
| `dates`        | `{raw: string, start: string\|null, end: string\|null, current: bool}` | as written, not normalized; a hand-typed trailing `(2 years)` is dropped; `current` is true when the end is Present/Current/Now |
| `bullets`      | string[]                                                            | `•` / `-` / `*` bullets (and any free text under the role), markers removed               |
| `technologies` | string[]                                                            | from a `Technologies:` / `Tech used:` / `Tech Stack:` line, split and trimmed             |
| `condensed`    | bool                                                                | true for one-line entries under `### Earlier Experience`                                  |

Example (`uv run cvforge parse inputs/test_resume.md`, abridged):

```json
{
  "schema_version": 1,
  "name": "John Doe",
  "title": "Senior Software Engineer",
  "contact": {
    "items": ["john.doe@email.com", "San Francisco, CA", "LinkedIn"],
    "email": "john.doe@email.com",
    "links": [{ "label": "LinkedIn", "url": "https://linkedin.com/in/johndoe" }]
  },
  "summary": "Experienced software engineer with 8+ years building scalable web applications. ...",
  "skills": [
    { "category": "Languages", "items": ["Python", "JavaScript", "TypeScript", "Go", "SQL"] },
    { "category": "Frameworks & Tools", "items": ["React", "Django", "Flask", "Node.js", "Docker", "Kubernetes", "AWS"] },
    { "category": "Practices", "items": ["Agile/Scrum", "TDD", "CI/CD", "Microservices Architecture"] }
  ],
  "experience": [
    {
      "company": "Tech Company Inc.",
      "role": "Senior Software Engineer",
      "dates": { "raw": "January 2020 - Present", "start": "January 2020", "end": "Present", "current": true },
      "bullets": ["Led development of microservices architecture serving 10M+ users, improving response time by 40%", "..."],
      "technologies": ["Python", "Django", "React", "AWS", "Docker", "Kubernetes"],
      "condensed": false
    },
    {
      "company": "Digital Agency",
      "role": "Web Developer",
      "dates": { "raw": "2016 - 2018", "start": "2016", "end": "2018", "current": false },
      "bullets": [],
      "technologies": [],
      "condensed": true
    }
  ],
  "education": [
    { "degree": "Bachelor of Science in Computer Science", "institution": "University of California, Berkeley", "year": "2015", "details": [] }
  ],
  "certifications": [
    { "name": "AWS Certified Solutions Architect - Associate", "issuer": "Amazon Web Services", "year": "2021", "details": [] }
  ],
  "other_sections": [],
  "all_skills": ["Python", "JavaScript", "TypeScript", "Go", "SQL", "React", "...", "PostgreSQL", "Redis", "MongoDB"]
}
```

## Markdown Format

The parser expects this structure (see `inputs/test_resume.md` for a full example):

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

**Role 1** | Company 1 | Dates
**Role 2** | Company 2 | Dates

## EDUCATION

**Degree Name**
University Name | Year
```

Notes:

- Contact lines are recognized before the first `##` section when they contain an email, a
  LinkedIn/GitHub/Website/Portfolio link, or one of a few location keywords (e.g. `Remote`, `USA`,
  `California`). Putting the email on the contact line is the safest way to get it detected.
- Durations such as `(4 years 10 months)` are calculated automatically from `Start - End` dates
  (`Present` counts to today) and shown in the PDF.

## Customization

Every renderer reads its settings from the `Config` class in `cvforge/config.py`:

```python
# cvforge/config.py
class Config:
    PRIMARY_COLOR = colors.HexColor("#1e40af")  # headers, dividers
    ACCENT_COLOR = colors.HexColor("#1e3a8a")  # subtitle
    FONT_SIZE_NAME = 24
    FONT_SIZE_SECTION_HEADER = 13
    MARGIN_TOP = 0.5 * inch
    MARGIN_LEFT = 0.75 * inch
    PAGE_SIZE = letter  # or A4
    INPUTS_FOLDER = "inputs"  # where `build`/`parse` also look for input files
    OUTPUTS_FOLDER = "outputs"  # default PDF destination
    CALCULATE_DURATIONS = True
    KEEP_SECTIONS_TOGETHER = True
```

`config.example.py` contains ready-made themes (green, compact, classic black & white): copy a
theme's values over the matching ones in `cvforge/config.py`. See `cvforge/config.py` for the full
list of options (colors, font families and sizes, margins, spacing, divider style, feature flags).

Color pickers: [HTML Color Codes](https://htmlcolorcodes.com/), [Coolors](https://coolors.co/),
[Color Hunt](https://colorhunt.co/).

## Using as a Library

```python
from cvforge import generate_pdf_from_data, parse_markdown_resume, to_structured

with open("resume.md", encoding="utf-8") as f:
    data = parse_markdown_resume(f.read())

generate_pdf_from_data(data, "output.pdf")  # PDF
structured = to_structured(data)  # the `cvforge parse` dict
```

## Project Structure

```
cvforge/                         # repository root
├── .github/
│   ├── FUNDING.yml              # Ko-fi sponsor link
│   └── workflows/ci.yml         # ruff + pytest on push / PR
├── cvforge/                     # the installable package
│   ├── __init__.py              # public API re-exports
│   ├── __main__.py              # `python -m cvforge`
│   ├── cli.py                   # argparse CLI: `build` and `parse`
│   ├── config.py                # colors, fonts, spacing, folders, feature flags
│   ├── styles.py                # ReportLab paragraph styles
│   ├── parser.py                # markdown -> raw sections
│   ├── structured.py            # raw sections -> versioned JSON shape (`parse`)
│   ├── formatter.py             # markdown emphasis/links -> ReportLab markup
│   ├── duration.py              # date-range duration calculation
│   ├── validators.py            # file checks, prompts, output paths
│   └── generator.py             # PDF rendering
├── tests/                       # pytest suite (offline)
├── inputs/test_resume.md        # sample resume
├── config.example.py            # example themes
├── markdown_to_resume_pdf.py    # legacy wrapper for `cvforge build`
├── pyproject.toml
└── uv.lock
```

## Development

```bash
uv sync                    # includes the dev group (pytest, ruff)
uv run pytest              # tests
uv run ruff check .        # lint
uv run ruff format .       # format
```

CI (`.github/workflows/ci.yml`) runs `uv sync --locked`, `ruff check`, `ruff format --check` and
`pytest` on Python 3.11 and 3.13.

## Troubleshooting

- **`ModuleNotFoundError` / `cvforge: command not found`** — run `uv sync`, then use
  `uv run cvforge ...`.
- **"Permission denied"** — the output PDF may be open in another application; close it and retry.
- **"Input file not found"** — check the path; cvforge lists `.md` files it found nearby and in the
  inputs folder.
- **No durations shown** — check `CALCULATE_DURATIONS` in `cvforge/config.py` and that dates are
  written as `Start - End`.

## Found this useful?

If you'd like to buy me a coffee or send a tip, it's much appreciated.

[![Say thanks on Ko-fi](https://img.shields.io/badge/Ko--fi-Say%20thanks-FF5E5B?logo=kofi&logoColor=white)](https://ko-fi.com/jessdp)

A star works just as well.

## License

MIT License - feel free to use and modify for your needs.
