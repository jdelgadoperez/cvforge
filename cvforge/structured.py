"""
Structured (JSON-ready) view of a parsed resume.

``parse_markdown_resume`` returns a loose, rendering-oriented structure (sections of raw
markdown lines). ``to_structured`` turns that into a stable, documented shape that other
tools can consume -- it is what ``cvforge parse`` prints. Everything here is plain text:
markdown emphasis and links are stripped, comma lists are split and trimmed.

The shape is versioned with ``SCHEMA_VERSION``. Additive changes (new keys) keep the
version; removing or renaming a key, or changing a value's type, bumps it.
"""

import re

SCHEMA_VERSION = 1

# Bullet markers accepted at the start of a line.
_BULLET_RE = re.compile(r"^(?:[•▪◦‣]|[-*+](?=\s))\s*")
# Separators between a start and end date ("Jan 2020 - Present", "2016 – 2018").
_DATE_SPLIT_RE = re.compile(r"\s+[-–—]+\s+|\s*[–—]\s*|(?<=\d)\s*-\s*(?=\d)")
# A trailing "(1 year 2 months)" style duration someone typed by hand.
_TRAILING_PARENS_RE = re.compile(r"\s*\([^)]*\)\s*$")
_TECH_RE = re.compile(r"^(?:technologies|tech(?:nolog(?:y|ies))?\s*(?:used|stack)?)\s*:\s*", re.I)
_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_URL_RE = re.compile(r"(?:https?://|www\.)\S+|\b[\w-]+\.(?:com|io|dev|me|org|net)/\S*", re.I)
_EMOJI_RE = re.compile(r"[📧🔗📄💼🎓🏆📍📱☎✉🌐]")
_YEAR_RE = re.compile(r"\b(?:19|20)\d{2}\b")
_PRESENT_RE = re.compile(r"\b(?:present|current|now|today)\b", re.I)


def strip_markdown(text):
    """Return ``text`` with markdown links, emphasis and contact emoji removed."""
    text = _EMOJI_RE.sub("", text)
    text = _LINK_RE.sub(r"\1", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"__(.+?)__", r"\1", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\1", text)
    text = re.sub(r"(?<!\w)_(?!\s)(.+?)(?<!\s)_(?!\w)", r"\1", text)
    text = text.replace("`", "")
    return re.sub(r"\s+", " ", text).strip()


def split_list(text):
    """
    Split a comma/semicolon separated list, ignoring separators inside parentheses.

    >>> split_list("Python, AWS (EC2, S3), Go.")
    ['Python', 'AWS (EC2, S3)', 'Go']
    """
    items, depth, current = [], 0, []
    for ch in text:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth = max(depth - 1, 0)
        if ch in ",;" and depth == 0:
            items.append("".join(current))
            current = []
        else:
            current.append(ch)
    items.append("".join(current))
    cleaned = []
    for item in items:
        item = strip_markdown(item).strip().rstrip(".").strip()
        if item:
            cleaned.append(item)
    return cleaned


def _is_bold_line(line):
    return bool(re.fullmatch(r"\*\*[^*].*?\*\*:?", line))


def _strip_bullet(line):
    return _BULLET_RE.sub("", line, count=1).strip()


def _is_bullet(line):
    return bool(_BULLET_RE.match(line))


def parse_dates(raw):
    """
    Split a date range into its parts. Values are kept as written (no date parsing).

    Returns a dict ``{"raw", "start", "end", "current"}``; ``start``/``end`` are ``None``
    when the text is not a recognisable range (a single year keeps ``start``).
    """
    raw = _TRAILING_PARENS_RE.sub("", strip_markdown(raw)).strip()
    if not raw:
        return {"raw": "", "start": None, "end": None, "current": False}
    parts = [p.strip() for p in _DATE_SPLIT_RE.split(raw, maxsplit=1)]
    if len(parts) == 2 and all(parts):
        start, end = parts
    else:
        start, end = raw, None
    return {
        "raw": raw,
        "start": start,
        "end": end,
        "current": bool(end and _PRESENT_RE.search(end)),
    }


def _section_kind(name):
    upper = name.upper()
    if "SUMMARY" in upper or "PROFILE" in upper or "OBJECTIVE" in upper or "ABOUT" in upper:
        return "summary"
    if "SKILL" in upper:
        return "skills"
    if "EXPERIENCE" in upper or "EMPLOYMENT" in upper or "WORK HISTORY" in upper:
        return "experience"
    if "EDUCATION" in upper:
        return "education"
    if "CERTIF" in upper:
        return "certifications"
    return "other"


def _parse_contact(lines):
    items, links, email = [], [], None
    for line in lines:
        for label, url in _LINK_RE.findall(line):
            links.append({"label": strip_markdown(label), "url": url.strip()})
        for part in line.split("|"):
            text = strip_markdown(part)
            if text:
                items.append(text)
        if email is None:
            match = _EMAIL_RE.search(_LINK_RE.sub(r"\1", line))
            if match:
                email = match.group(0)
    linked = {link["url"] for link in links}
    for item in items:
        if "@" in item:
            continue
        for match in _URL_RE.findall(item):
            if match not in linked:
                links.append({"label": match, "url": match})
                linked.add(match)
    return {"items": items, "email": email, "links": links}


def _parse_skills(section):
    groups = []
    current = None

    def group_for(category):
        nonlocal current
        for group in groups:
            if group["category"] == category:
                current = group
                return group
        current = {"category": category, "items": []}
        groups.append(current)
        return current

    lines = list(section["content"])
    for sub in section["subsections"]:
        lines.append(f"**{sub['name']}**")
        lines.extend(sub["lines"])

    for raw_line in lines:
        line = _strip_bullet(raw_line.strip())
        if not line:
            continue
        # "**Languages**" on its own line opens a category.
        if _is_bold_line(line):
            group_for(strip_markdown(line).rstrip(":").strip())
            continue
        # "**Languages:** Python, Go" or "Languages: Python, Go" -- inline category.
        inline = re.match(r"^\*\*(.+?)\*\*\s*:?\s*(.+)$", line) or re.match(
            r"^([A-Za-z][\w &/+-]{0,40}):\s+(.+)$", line
        )
        if inline:
            group = group_for(strip_markdown(inline.group(1)).rstrip(":").strip())
            group["items"].extend(split_list(inline.group(2)))
            continue
        group = current if current is not None else group_for(None)
        group["items"].extend(split_list(line))

    for group in groups:
        group["items"] = _dedupe(group["items"])
    return [group for group in groups if group["items"]]


def _dedupe(items):
    seen, out = set(), []
    for item in items:
        key = item.casefold()
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out


def _empty_job(company, condensed=False):
    return {
        "company": company,
        "role": None,
        "dates": parse_dates(""),
        "bullets": [],
        "technologies": [],
        "condensed": condensed,
    }


def _parse_condensed_line(line):
    """``**Role** | Company | Dates`` -> experience entry (the format of "Earlier Experience")."""
    parts = [strip_markdown(p) for p in line.split("|")]
    job = _empty_job(None, condensed=True)
    job["role"] = parts[0] or None
    if len(parts) >= 3:
        job["company"] = parts[1] or None
        job["dates"] = parse_dates(parts[-1])
    elif len(parts) == 2:
        if _YEAR_RE.search(parts[1]) or _PRESENT_RE.search(parts[1]):
            job["dates"] = parse_dates(parts[1])
        else:
            job["company"] = parts[1] or None
    return job


def _parse_experience_entry(sub):
    name = strip_markdown(sub["name"])
    if "earlier" in name.lower() and "experience" in name.lower():
        return [_parse_condensed_line(line) for line in sub["lines"] if line.strip()]

    job = _empty_job(name)
    expect_dates = False
    for raw_line in sub["lines"]:
        line = raw_line.strip()
        if not line:
            continue
        plain = strip_markdown(line)
        tech = _TECH_RE.match(plain)
        if tech:
            job["technologies"].extend(split_list(plain[tech.end() :]))
            expect_dates = False
        elif _is_bullet(line):
            text = strip_markdown(_strip_bullet(line))
            if text:
                job["bullets"].append(text)
            expect_dates = False
        elif job["role"] is None and line.startswith("**"):
            # "**Senior Engineer**" (dates on the next line) or "**Senior Engineer** | 2020 - Now"
            role, _, rest = plain.partition("|") if "|" in line else (plain, "", "")
            job["role"] = role.strip() or None
            if rest.strip():
                job["dates"] = parse_dates(rest)
            else:
                expect_dates = True
        elif expect_dates:
            job["dates"] = parse_dates(line)
            expect_dates = False
        else:
            # Free text after the header: treat as a description bullet.
            job["bullets"].append(plain)
    job["technologies"] = _dedupe(job["technologies"])
    return [job]


def _parse_experience(section):
    jobs = []
    for sub in section["subsections"]:
        jobs.extend(_parse_experience_entry(sub))
    for line in section["content"]:
        if line.strip().startswith("**") and "|" in line:
            jobs.append(_parse_condensed_line(line))
    return jobs


def _entries(section):
    """Group a section's lines into ``{"title", "details"}`` entries keyed by bold headings."""
    entries = []
    lines = list(section["content"])
    for sub in section["subsections"]:
        lines.append(f"**{sub['name']}**")
        lines.extend(sub["lines"])
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_bold_line(line):
            entries.append({"title": strip_markdown(line), "details": []})
        elif entries:
            entries[-1]["details"].append(strip_markdown(_strip_bullet(line)))
        else:
            entries.append({"title": strip_markdown(_strip_bullet(line)), "details": []})
    return entries


def _split_meta(details):
    """First detail line "Org | 2015" -> ("Org", "2015"); either may be None."""
    if not details:
        return None, None
    parts = [p.strip() for p in details[0].split("|") if p.strip()]
    if not parts:
        return None, None
    date = None
    if len(parts) > 1 and (_YEAR_RE.search(parts[-1]) or _PRESENT_RE.search(parts[-1])):
        date = parts.pop()
    elif len(parts) == 1 and _YEAR_RE.fullmatch(parts[0]):
        return None, parts[0]
    return " | ".join(parts) or None, date


def _parse_education(section):
    out = []
    for entry in _entries(section):
        institution, year = _split_meta(entry["details"])
        out.append(
            {
                "degree": entry["title"],
                "institution": institution,
                "year": year,
                "details": entry["details"][1:] if entry["details"] else [],
            }
        )
    return out


def _parse_certifications(section):
    out = []
    for entry in _entries(section):
        issuer, year = _split_meta(entry["details"])
        out.append(
            {
                "name": entry["title"],
                "issuer": issuer,
                "year": year,
                "details": entry["details"][1:] if entry["details"] else [],
            }
        )
    return out


def _section_lines(section):
    lines = [strip_markdown(line) for line in section["content"] if line.strip()]
    for sub in section["subsections"]:
        lines.append(strip_markdown(sub["name"]))
        lines.extend(strip_markdown(line) for line in sub["lines"] if line.strip())
    return lines


def to_structured(data):
    """
    Convert ``parse_markdown_resume`` output to the stable ``cvforge parse`` shape.

    See README.md ("parse JSON shape") for the documented contract.
    """
    result = {
        "schema_version": SCHEMA_VERSION,
        "name": strip_markdown(data.get("name", "")),
        "title": strip_markdown(data.get("title", "")),
        "contact": _parse_contact(data.get("contact", [])),
        "summary": "",
        "skills": [],
        "experience": [],
        "education": [],
        "certifications": [],
        "other_sections": [],
        "all_skills": [],
    }
    summaries = []
    for section in data.get("sections", []):
        kind = _section_kind(section["name"])
        if kind == "summary":
            summaries.append(" ".join(_section_lines(section)))
        elif kind == "skills":
            result["skills"].extend(_parse_skills(section))
        elif kind == "experience":
            result["experience"].extend(_parse_experience(section))
        elif kind == "education":
            result["education"].extend(_parse_education(section))
        elif kind == "certifications":
            result["certifications"].extend(_parse_certifications(section))
        else:
            result["other_sections"].append(
                {"name": strip_markdown(section["name"]), "lines": _section_lines(section)}
            )
    result["summary"] = " ".join(s for s in summaries if s).strip()

    every = [item for group in result["skills"] for item in group["items"]]
    every += [tech for job in result["experience"] for tech in job["technologies"]]
    result["all_skills"] = _dedupe(every)
    return result
