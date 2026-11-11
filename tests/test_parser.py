from cvforge.parser import parse_markdown_resume, validate_parsed_data


def test_sample_header(sample_md):
    data = parse_markdown_resume(sample_md)
    assert data["name"] == "John Doe"
    assert data["title"] == "Senior Software Engineer"
    assert data["contact"] == [
        "john.doe@email.com | San Francisco, CA | [LinkedIn](https://linkedin.com/in/johndoe)"
    ]


def test_sample_sections(sample_md):
    data = parse_markdown_resume(sample_md)
    assert [s["name"] for s in data["sections"]] == [
        "PROFESSIONAL SUMMARY",
        "TECHNICAL SKILLS",
        "EXPERIENCE",
        "EDUCATION",
        "CERTIFICATIONS",
    ]
    experience = data["sections"][2]
    assert [sub["name"] for sub in experience["subsections"]] == [
        "Tech Company Inc.",
        "Startup Co.",
        "Earlier Experience",
    ]
    first = experience["subsections"][0]["lines"]
    assert first[0] == "**Senior Software Engineer**"
    assert first[1] == "January 2020 - Present"
    assert first[-1].startswith("**Technologies:**")


def test_separators_and_blank_lines_are_skipped():
    md = "# Jane\n\n**Engineer**\n\n---\n\n## SUMMARY\n\n\nLine one\n\n---\nLine two\n"
    data = parse_markdown_resume(md)
    assert data["sections"][0]["content"] == ["Line one", "Line two"]


def test_only_first_heading_is_the_name():
    data = parse_markdown_resume("# Jane Roe\n**Engineer**\n## SKILLS\n# Not A Name\n")
    assert data["name"] == "Jane Roe"
    # A later "# " line is just content.
    assert data["sections"][0]["content"] == ["# Not A Name"]


def test_contact_lines_detected_before_first_section():
    md = "# Jane\n**Engineer**\njane@example.com\n[GitHub](https://github.com/jane)\nRemote\n## SKILLS\nGo\n"
    data = parse_markdown_resume(md)
    assert data["contact"] == ["jane@example.com", "[GitHub](https://github.com/jane)", "Remote"]


def test_subsection_without_section_is_dropped():
    data = parse_markdown_resume("# Jane\n**Engineer**\n### Orphan\nline\n")
    assert data["sections"] == []


def test_empty_input():
    assert parse_markdown_resume("") == {"name": "", "title": "", "contact": [], "sections": []}


def test_validate_parsed_data():
    ok = {"name": "J", "title": "E", "contact": [], "sections": [{"name": "S"}]}
    assert validate_parsed_data(ok) == (True, "")
    assert validate_parsed_data({**ok, "name": ""})[0] is False
    assert "title" in validate_parsed_data({**ok, "title": ""})[1]
    assert "section" in validate_parsed_data({**ok, "sections": []})[1]
