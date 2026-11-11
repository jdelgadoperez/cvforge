# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this is

cvforge turns a markdown resume into a styled PDF (ReportLab) or into versioned JSON. Python
3.11+, managed with uv, packaged with setuptools (`[project.scripts] cvforge = "cvforge.cli:main"`).

## Commands

```bash
uv sync                                   # deps + dev group (pytest, ruff) + editable cvforge
uv run cvforge build <in.md> [out.pdf] [--force]
uv run cvforge parse <in.md> [--compact]  # JSON on stdout, diagnostics on stderr
uv run pytest                             # all tests (offline)
uv run pytest tests/test_structured.py -k skills
uv run ruff check .                       # lint (E,F,I,UP,B,SIM; E501 ignored)
uv run ruff format .                      # format (100 cols, double quotes)
```

CI (`.github/workflows/ci.yml`): `uv sync --locked`, `ruff check`, `ruff format --check`, `pytest`
on Python 3.11 and 3.13. If you change dependencies, run `uv lock` and commit `uv.lock`.

## Architecture

Pipeline: markdown → `parser.parse_markdown_resume` (raw dict: name, title, contact lines,
sections → content lines + `###` subsections) → either `generator.generate_pdf_from_data` (PDF) or
`structured.to_structured` (the `parse` JSON).

- `cvforge/cli.py` — argparse CLI; `build` and `parse` subcommands. `markdown_to_resume_pdf.py`
  (repo root) is a backward-compatible wrapper that calls `main(["build", ...])`.
- `cvforge/parser.py` — line-based parsing; sections are routed later by name keywords.
- `cvforge/generator.py` — renderers per section kind (summary / skills / experience / generic),
  routed by keywords in the `##` heading.
- `cvforge/structured.py` — the `parse` contract. `SCHEMA_VERSION = 1`; the shape is documented in
  README.md ("parse JSON shape") and pinned by `tests/test_structured.py`.
- `cvforge/config.py` — the single `Config` class (colors, fonts, spacing, `INPUTS_FOLDER`,
  `OUTPUTS_FOLDER`, feature flags). `config.example.py` holds themes to copy from.
- `cvforge/duration.py` (dateutil-based durations), `formatter.py` (markdown → ReportLab markup),
  `styles.py`, `validators.py` (file checks, interactive prompts, output paths).

## Conventions

- The `parse` JSON is consumed by other tools (job-hunter builds a skill profile from it). Adding a
  key is fine; renaming/removing a key or changing a type requires bumping `SCHEMA_VERSION` and
  updating README.md and the tests. Keep strings plain text and skill lists split + trimmed.
- `cvforge parse` must write only JSON to stdout — send any diagnostics to stderr.
- Tests live in `tests/` and are offline; the sample resume `inputs/test_resume.md` is a fixture,
  so changing it means updating the assertions. Write PDFs to `tmp_path`, never the repo.
- `outputs/` is gitignored; don't commit generated PDFs.
- Conventional Commits.
