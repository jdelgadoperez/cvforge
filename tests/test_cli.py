import json
import shutil
import subprocess
import sys

import pytest

from cvforge import cli
from cvforge.structured import SCHEMA_VERSION


def test_parse_prints_json(sample_path, capsys):
    assert cli.main(["parse", str(sample_path)]) == 0
    out, _ = capsys.readouterr()
    payload = json.loads(out)
    assert payload["schema_version"] == SCHEMA_VERSION
    assert payload["name"] == "John Doe"
    assert "Kubernetes" in payload["all_skills"]


def test_parse_compact(sample_path, capsys):
    assert cli.main(["parse", "--compact", str(sample_path)]) == 0
    out, _ = capsys.readouterr()
    assert out.count("\n") == 1
    json.loads(out)


def test_parse_missing_file_writes_only_to_stderr(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert cli.main(["parse", "missing.md"]) == 1
    out, err = capsys.readouterr()
    assert out == ""
    assert "not found" in err


def test_parse_rejects_resume_without_title(tmp_path, capsys):
    md = tmp_path / "bad.md"
    md.write_text("# Jane\n## SKILLS\nGo\n", encoding="utf-8")
    assert cli.main(["parse", str(md)]) == 1
    out, err = capsys.readouterr()
    assert out == ""
    assert "title" in err


def test_build_writes_pdf(sample_path, tmp_path, capsys):
    out_pdf = tmp_path / "resume.pdf"
    assert cli.main(["build", str(sample_path), str(out_pdf)]) == 0
    assert out_pdf.read_bytes().startswith(b"%PDF")
    assert "created successfully" in capsys.readouterr().out


def test_build_adds_pdf_extension_and_default_output_folder(sample_path, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert cli.main(["build", str(sample_path), "named"]) == 0
    assert (tmp_path / "named.pdf").read_bytes().startswith(b"%PDF")

    # No output argument: written to the configured outputs folder under the cwd.
    assert cli.main(["build", str(sample_path)]) == 0
    assert (tmp_path / "outputs" / "test_resume.pdf").read_bytes().startswith(b"%PDF")


def test_build_overwrite_prompt_and_force(sample_path, tmp_path, monkeypatch):
    out_pdf = tmp_path / "resume.pdf"
    out_pdf.write_bytes(b"old")
    monkeypatch.setattr("builtins.input", lambda _prompt: "n")
    assert cli.main(["build", str(sample_path), str(out_pdf)]) == 0
    assert out_pdf.read_bytes() == b"old"

    def no_prompt(_prompt):
        raise AssertionError("--force must not prompt")

    monkeypatch.setattr("builtins.input", no_prompt)
    assert cli.main(["build", str(sample_path), str(out_pdf), "--force"]) == 0
    assert out_pdf.read_bytes().startswith(b"%PDF")


def test_build_invalid_resume_fails(tmp_path, capsys):
    md = tmp_path / "empty.md"
    md.write_text("\n", encoding="utf-8")
    assert cli.main(["build", str(md), str(tmp_path / "x.pdf")]) == 1
    assert "empty" in capsys.readouterr().out
    assert not (tmp_path / "x.pdf").exists()


def test_no_command_prints_help(capsys):
    assert cli.main([]) == 2
    assert "usage: cvforge" in capsys.readouterr().err


def test_version(capsys):
    with pytest.raises(SystemExit) as exc:
        cli.main(["--version"])
    assert exc.value.code == 0
    assert capsys.readouterr().out.startswith("cvforge ")


def test_legacy_wrapper_script(sample_path, tmp_path):
    script = sample_path.parent.parent / "markdown_to_resume_pdf.py"
    out_pdf = tmp_path / "legacy.pdf"
    result = subprocess.run(
        [sys.executable, str(script), str(sample_path), str(out_pdf)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert out_pdf.read_bytes().startswith(b"%PDF")


@pytest.mark.skipif(shutil.which("cvforge") is None, reason="console script not installed")
def test_console_script_parse(sample_path):
    result = subprocess.run(
        ["cvforge", "parse", str(sample_path)], capture_output=True, text=True, check=True
    )
    assert json.loads(result.stdout)["schema_version"] == SCHEMA_VERSION


def test_parse_exits_quietly_when_the_reader_closes_early(tmp_path):
    import subprocess
    import sys
    from pathlib import Path

    sample = Path(__file__).resolve().parent.parent / "inputs" / "test_resume.md"
    proc = subprocess.run(
        f'"{sys.executable}" -m cvforge parse "{sample}" | head -c 10',
        shell=True,
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )
    assert proc.stdout.startswith("{")
    assert "Traceback" not in proc.stderr
