from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_RESUME = REPO_ROOT / "inputs" / "test_resume.md"


@pytest.fixture
def sample_path():
    return SAMPLE_RESUME


@pytest.fixture
def sample_md():
    return SAMPLE_RESUME.read_text(encoding="utf-8")
