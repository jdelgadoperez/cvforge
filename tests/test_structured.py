import pytest

from cvforge.parser import parse_markdown_resume
from cvforge.structured import (
    SCHEMA_VERSION,
    parse_dates,
    split_list,
    strip_markdown,
    to_structured,
)

TOP_LEVEL_KEYS = {
    "schema_version",
    "name",
    "title",
    "contact",
    "summary",
    "skills",
    "experience",
    "education",
    "certifications",
    "other_sections",
    "all_skills",
}
JOB_KEYS = {"company", "role", "dates", "bullets", "technologies", "condensed"}
DATE_KEYS = {"raw", "start", "end", "current"}


def structured(md):
    return to_structured(parse_markdown_resume(md))


def structured_with_diagnostics(md):
    """``(structured_result, diagnostic_messages)`` -- diagnostics collected, not printed."""
    messages = []
    return to_structured(parse_markdown_resume(md), warn=messages.append), messages


def condensed_resume(*experience_lines):
    body = "\n".join(experience_lines)
    return f"# Jane\n**Engineer**\n## EXPERIENCE\n### Earlier Experience\n{body}\n"


@pytest.fixture
def sample(sample_md):
    return structured(sample_md)


def test_shape_is_stable(sample):
    assert set(sample) == TOP_LEVEL_KEYS
    assert sample["schema_version"] == SCHEMA_VERSION == 1
    assert set(sample["contact"]) == {"items", "email", "links"}
    for group in sample["skills"]:
        assert set(group) == {"category", "items"}
    for job in sample["experience"]:
        assert set(job) == JOB_KEYS
        assert set(job["dates"]) == DATE_KEYS
    for edu in sample["education"]:
        assert set(edu) == {"degree", "institution", "year", "details"}
    for cert in sample["certifications"]:
        assert set(cert) == {"name", "issuer", "year", "details"}


def test_sample_header_and_contact(sample):
    assert sample["name"] == "John Doe"
    assert sample["title"] == "Senior Software Engineer"
    assert sample["contact"] == {
        "items": ["john.doe@email.com", "San Francisco, CA", "LinkedIn"],
        "email": "john.doe@email.com",
        "links": [{"label": "LinkedIn", "url": "https://linkedin.com/in/johndoe"}],
    }
    assert sample["summary"].startswith("Experienced software engineer with 8+ years")


def test_sample_skills_are_split_and_grouped(sample):
    assert sample["skills"] == [
        {"category": "Languages", "items": ["Python", "JavaScript", "TypeScript", "Go", "SQL"]},
        {
            "category": "Frameworks & Tools",
            "items": ["React", "Django", "Flask", "Node.js", "Docker", "Kubernetes", "AWS"],
        },
        {
            "category": "Practices",
            "items": ["Agile/Scrum", "TDD", "CI/CD", "Microservices Architecture"],
        },
    ]


def test_sample_experience(sample):
    jobs = sample["experience"]
    assert [(j["company"], j["role"], j["condensed"]) for j in jobs] == [
        ("Tech Company Inc.", "Senior Software Engineer", False),
        ("Startup Co.", "Software Engineer", False),
        ("Digital Agency", "Web Developer", True),
        ("Small Business Solutions", "Junior Developer", True),
    ]
    first = jobs[0]
    assert first["dates"] == {
        "raw": "January 2020 - Present",
        "start": "January 2020",
        "end": "Present",
        "current": True,
    }
    assert len(first["bullets"]) == 3
    assert first["bullets"][0].startswith("Led development of microservices")
    assert not first["bullets"][0].startswith("•")
    assert first["technologies"] == ["Python", "Django", "React", "AWS", "Docker", "Kubernetes"]
    assert jobs[1]["dates"]["current"] is False
    assert jobs[2]["dates"] == {
        "raw": "2016 - 2018",
        "start": "2016",
        "end": "2018",
        "current": False,
    }


def test_sample_education_and_certifications(sample):
    assert sample["education"] == [
        {
            "degree": "Bachelor of Science in Computer Science",
            "institution": "University of California, Berkeley",
            "year": "2015",
            "details": [],
        }
    ]
    assert [(c["name"], c["issuer"], c["year"]) for c in sample["certifications"]] == [
        ("AWS Certified Solutions Architect - Associate", "Amazon Web Services", "2021"),
        ("Certified Kubernetes Administrator (CKA)", "Cloud Native Computing Foundation", "2022"),
    ]


def test_all_skills_dedupes_across_skills_and_technologies(sample):
    assert sample["all_skills"][:5] == ["Python", "JavaScript", "TypeScript", "Go", "SQL"]
    assert sample["all_skills"][-3:] == ["PostgreSQL", "Redis", "MongoDB"]
    lowered = [s.lower() for s in sample["all_skills"]]
    assert len(lowered) == len(set(lowered))


def test_inline_categories_and_uncategorized_skills():
    md = """# Jane
**Engineer**
## SKILLS
Bash, Make
**Languages:** Python,  Go , rust.
Cloud: AWS (EC2, S3); GCP
- **Databases**: Postgres, python
**Languages**
Python, Kotlin
"""
    skills = structured(md)["skills"]
    assert skills == [
        {"category": None, "items": ["Bash", "Make"]},
        {"category": "Languages", "items": ["Python", "Go", "rust", "Kotlin"]},
        {"category": "Cloud", "items": ["AWS (EC2, S3)", "GCP"]},
        {"category": "Databases", "items": ["Postgres", "python"]},
    ]


def test_condensed_entry_keeps_a_following_prose_line_as_a_bullet():
    entry = "**Web Developer** | Pensacola State College | 2013 - 2014"
    description = "Led migration of Classic ASP sites to a custom WordPress stack."
    result, messages = structured_with_diagnostics(condensed_resume(entry, description))

    jobs = result["experience"]
    assert len(jobs) == 1
    assert jobs[0]["company"] == "Pensacola State College"
    assert jobs[0]["role"] == "Web Developer"
    assert jobs[0]["bullets"] == [description]
    assert messages == []


def test_condensed_entry_keeps_a_following_bullet_line_as_a_bullet():
    entry = "**Web Developer** | Pensacola State College | 2013 - 2014"
    description = "Led migration of Classic ASP sites to a custom WordPress stack."
    result, messages = structured_with_diagnostics(condensed_resume(entry, f"\u2022 {description}"))

    jobs = result["experience"]
    assert len(jobs) == 1
    assert jobs[0]["bullets"] == [description]
    assert messages == []


def test_condensed_entries_never_have_a_null_company():
    entries = [
        "**Web Developer** | Pensacola State College | 2013 - 2014",
        "Led migration of Classic ASP sites to a custom WordPress stack.",
        "\u2022 Trained two junior developers.",
        "**Support Engineer** | Helpdesk Co | 2012 - 2013",
        "- Handled escalations.",
    ]
    result, messages = structured_with_diagnostics(condensed_resume(*entries))

    jobs = result["experience"]
    assert [job["company"] for job in jobs] == ["Pensacola State College", "Helpdesk Co"]
    assert all(job["company"] is not None for job in jobs)
    assert jobs[0]["bullets"] == [entries[1], "Trained two junior developers."]
    assert jobs[1]["bullets"] == ["Handled escalations."]
    assert messages == []


def test_condensed_description_with_no_entry_above_it_is_reported_and_skipped():
    orphan = "Everything before 2012 was contract work."
    entry = "**Web Developer** | Pensacola State College | 2013 - 2014"
    result, messages = structured_with_diagnostics(condensed_resume(orphan, entry))

    jobs = result["experience"]
    assert [job["company"] for job in jobs] == ["Pensacola State College"]
    assert jobs[0]["bullets"] == []
    assert len(messages) == 1
    assert orphan in messages[0]
    assert "Earlier Experience" in messages[0]


def test_condensed_entry_without_a_company_field_is_reported():
    entry = "**Intern** | 2015"
    result, messages = structured_with_diagnostics(condensed_resume(entry))

    jobs = result["experience"]
    assert (jobs[0]["role"], jobs[0]["company"]) == ("Intern", None)
    assert len(messages) == 1
    assert "Intern | 2015" in messages[0]


def test_experience_variants():
    md = """# Jane
**Engineer**
## WORK EXPERIENCE
### Acme
**Staff Engineer** | March 2021 - Present (3 years)
Owned the platform.
- Shipped things
* Fixed **bugs** in [the API](https://acme.dev)
Tech Stack: Go, Kafka
### Beta
**Engineer**
### Earlier Experience
**Intern** | 2015
**Contractor** | Gamma LLC
"""
    # "**Intern** | 2015" has no company field, which is reported (see the test above).
    jobs = structured_with_diagnostics(md)[0]["experience"]
    acme = jobs[0]
    assert acme["role"] == "Staff Engineer"
    assert acme["dates"] == {
        "raw": "March 2021 - Present",
        "start": "March 2021",
        "end": "Present",
        "current": True,
    }
    assert acme["bullets"] == ["Owned the platform.", "Shipped things", "Fixed bugs in the API"]
    assert acme["technologies"] == ["Go", "Kafka"]
    beta = jobs[1]
    assert (beta["company"], beta["role"], beta["dates"]["raw"]) == ("Beta", "Engineer", "")
    assert (jobs[2]["role"], jobs[2]["company"], jobs[2]["dates"]["start"]) == (
        "Intern",
        None,
        "2015",
    )
    assert (jobs[3]["role"], jobs[3]["company"]) == ("Contractor", "Gamma LLC")


def test_other_sections_and_minimal_resume():
    md = "# Jane\n**Engineer**\n## PROJECTS\n### cvforge\n- Resume tool\n## AWARDS\nBest **demo**\n"
    result = structured(md)
    assert result["other_sections"] == [
        {"name": "PROJECTS", "lines": ["cvforge", "- Resume tool"]},
        {"name": "AWARDS", "lines": ["Best demo"]},
    ]
    assert result["skills"] == result["experience"] == result["all_skills"] == []
    assert result["contact"] == {"items": [], "email": None, "links": []}
    assert result["summary"] == ""


def test_bare_urls_in_contact_become_links():
    md = "# Jane\n**Engineer**\njane@x.io | github.com/jane | https://jane.dev\n## SKILLS\nGo\n"
    contact = structured(md)["contact"]
    assert contact["email"] == "jane@x.io"
    assert contact["links"] == [
        {"label": "github.com/jane", "url": "github.com/jane"},
        {"label": "https://jane.dev", "url": "https://jane.dev"},
    ]


@pytest.mark.parametrize(
    ("raw", "start", "end", "current"),
    [
        ("Jan 2020 – Present", "Jan 2020", "Present", True),
        ("2016-2018", "2016", "2018", False),
        ("May 2019 -- June 2020 (1 year 1 month)", "May 2019", "June 2020", False),
        ("2015", "2015", None, False),
    ],
)
def test_parse_dates(raw, start, end, current):
    parsed = parse_dates(raw)
    assert (parsed["start"], parsed["end"], parsed["current"]) == (start, end, current)


def test_strip_markdown_and_split_list():
    assert strip_markdown("📧 **Bold** *it* `code` [x](http://y)") == "Bold it code x"
    assert split_list("**A**, B;  , C.") == ["A", "B", "C"]
    assert split_list("Node.js, AWS (Lambda, S3)") == ["Node.js", "AWS (Lambda, S3)"]
