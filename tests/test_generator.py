from reportlab.platypus import Paragraph

from cvforge.config import Config
from cvforge.generator import render_earlier_experience
from cvforge.styles import create_custom_styles


def paragraph_texts(story):
    return [item.text for item in story if isinstance(item, Paragraph)]


def test_condensed_entry_descriptions_are_rendered(monkeypatch):
    monkeypatch.setattr(Config, "KEEP_SECTIONS_TOGETHER", False)
    entry = "**Web Developer** | Acme | 2013 - 2014"
    prose = "Led migration of Classic ASP sites to a custom WordPress stack."
    bullet = "\u2022 Trained two junior developers."
    story = []

    render_earlier_experience(
        story,
        {"name": "Earlier Experience", "lines": [entry, prose, bullet]},
        create_custom_styles(),
    )

    texts = paragraph_texts(story)
    assert any("Acme" in text for text in texts)
    assert any(prose in text for text in texts)
    assert any(bullet in text for text in texts)


def test_condensed_entry_descriptions_are_indented_under_the_entry(monkeypatch):
    monkeypatch.setattr(Config, "KEEP_SECTIONS_TOGETHER", False)
    styles = create_custom_styles()
    story = []

    render_earlier_experience(
        story,
        {
            "name": "Earlier Experience",
            "lines": ["**Web Developer** | Acme | 2013 - 2014", "Led the migration."],
        },
        styles,
    )

    indents = {
        paragraph.text: paragraph.style.leftIndent
        for paragraph in story
        if isinstance(paragraph, Paragraph)
    }
    entry_indent = next(indent for text, indent in indents.items() if "Acme" in text)
    detail_indent = next(indent for text, indent in indents.items() if "migration" in text)
    assert detail_indent > entry_indent
