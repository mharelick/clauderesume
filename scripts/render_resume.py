"""Validate resume.md and write resume.docx, resume.pdf, and resume.txt beside it.

Run from the repository root: python scripts/render_resume.py output/<version>/resume.md
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from xml.sax.saxutils import escape

from docx import Document
from docx.shared import Inches, Pt
from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate


Block = tuple[str, str]
WORD_RE = re.compile(r"[a-z0-9]+(?:'[a-z]+)?", re.I)


def words(text: str) -> list[str]:
    return [match.lower() for match in WORD_RE.findall(text)]


def parse_markdown(text: str) -> list[Block]:
    blocks: list[Block] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        for prefix, kind in (("### ", "role"), ("## ", "section"), ("# ", "name"), ("- ", "bullet")):
            if line.startswith(prefix):
                value = line[len(prefix):].strip()
                break
        else:
            kind, value = "text", line
        if not value or any(token in value for token in ("**", "[", "](", "|---")):
            raise ValueError("Use nonempty plain text without inline Markdown or tables")
        blocks.append((kind, value))
    if not blocks or blocks[0][0] != "name":
        raise ValueError("Resume must begin with '# Candidate Name'")
    return blocks


def extract_source_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt"}:
        return path.read_text(encoding="utf-8", errors="replace")
    if suffix == ".docx":
        return "\n".join(p.text for p in Document(path).paragraphs)
    if suffix == ".pdf":
        return "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
    return ""


def copied_prose(blocks: list[Block], data_dir: Path, width: int = 10) -> str | None:
    """Detect long verbatim spans in prose; headings and names are excluded."""
    if not data_dir.is_dir():
        return None
    candidates = [words(value) for kind, value in blocks if kind in {"bullet", "text"}]
    if candidates and blocks[1:2] and blocks[1][0] == "text":
        candidates.pop(0)  # contact line
    candidate_grams = {
        tuple(tokens[i:i + width])
        for tokens in candidates
        for i in range(max(0, len(tokens) - width + 1))
    }
    if not candidate_grams:
        return None
    for path in sorted(data_dir.rglob("*")):
        if (not path.is_file() or path.name.startswith("~$")
                or path.suffix.lower() not in {".md", ".txt", ".docx", ".pdf"}):
            continue
        try:
            source = words(extract_source_text(path))
        except Exception as exc:
            raise ValueError(f"Could not read source file {path.name}: {exc}") from exc
        if any(tuple(source[i:i + width]) in candidate_grams for i in range(max(0, len(source) - width + 1))):
            return path.name
    return None


DASH_RE = re.compile(r"[-‐-―−]")


def validate(blocks: list[Block], data_dir: Path) -> None:
    for index, (kind, value) in enumerate(blocks):
        # The name and contact line may legitimately contain hyphens (emails, URLs).
        if kind != "name" and not (index == 1 and kind == "text") and DASH_RE.search(value):
            raise ValueError("Hyphen or dash found; write compounds as separate words or reword")
        if kind not in {"bullet", "text"} or (index == 1 and kind == "text"):
            continue
        if re.search(r"\b(?:I|me|my|we|our)\b", value, re.I):
            raise ValueError("First-person or conversational wording in resume prose")
        tokens = words(value)
        if len(tokens) > (45 if kind == "bullet" else 50):
            raise ValueError("Resume bullet or paragraph is too long; condense it")
        for sentence in re.split(r"(?<=[.!?])\s+", value):
            if len(words(sentence)) > 27:
                raise ValueError("Run-on sentence detected; use shorter sentences")
    copied_from = copied_prose(blocks, data_dir)
    if copied_from:
        raise ValueError(f"Resume repeats a long source phrase from {copied_from}; rewrite it")


def write_docx(blocks: list[Block], target: Path) -> None:
    doc = Document()
    page = doc.sections[0]
    page.top_margin = page.bottom_margin = Inches(0.65)
    page.left_margin = page.right_margin = Inches(0.7)
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(10)
    normal.paragraph_format.space_after = Pt(3)
    for index, (kind, value) in enumerate(blocks):
        if kind == "name":
            para = doc.add_paragraph()
            para.alignment = 1
            run = para.add_run(value)
            run.bold = True
            run.font.size = Pt(16)
        elif kind == "section":
            para = doc.add_paragraph()
            para.alignment = 1
            para.paragraph_format.space_before = Pt(9)
            para.paragraph_format.keep_with_next = True
            para.add_run(value.upper()).bold = True
        elif kind == "role":
            para = doc.add_paragraph()
            para.paragraph_format.space_before = Pt(5)
            para.paragraph_format.keep_with_next = True
            para.add_run(value).bold = True
        elif kind == "bullet":
            para = doc.add_paragraph(style="List Bullet")
            para.paragraph_format.left_indent = Inches(0.22)
            para.paragraph_format.first_line_indent = Inches(-0.12)
            para.add_run(value)
        else:
            para = doc.add_paragraph(value)
            if index == 1:
                para.alignment = 1
    doc.save(target)


def write_pdf(blocks: list[Block], target: Path) -> None:
    styles = {
        "name": ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=16, leading=19, alignment=TA_CENTER, spaceAfter=3),
        "contact": ParagraphStyle("contact", fontName="Helvetica", fontSize=9, leading=12, alignment=TA_CENTER, spaceAfter=7),
        "section": ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=10, leading=12, textColor=colors.HexColor("#18354D"), alignment=TA_CENTER, spaceBefore=9, spaceAfter=3, keepWithNext=True),
        "role": ParagraphStyle("role", fontName="Helvetica-Bold", fontSize=10, leading=12, spaceBefore=5, spaceAfter=2, keepWithNext=True),
        "text": ParagraphStyle("text", fontName="Helvetica", fontSize=9.5, leading=12.5, spaceAfter=3),
        "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.5, leading=12.5, leftIndent=15, firstLineIndent=-8, spaceAfter=3),
    }
    story = []
    for index, (kind, value) in enumerate(blocks):
        style = "contact" if kind == "text" and index == 1 else kind
        story.append(Paragraph(escape(value), styles[style], bulletText="•" if kind == "bullet" else None))
    document = SimpleDocTemplate(str(target), pagesize=letter, leftMargin=0.7 * inch,
                                 rightMargin=0.7 * inch, topMargin=0.65 * inch,
                                 bottomMargin=0.65 * inch, title=blocks[0][1] + " Resume")
    document.build(story)


def write_txt(blocks: list[Block], target: Path) -> None:
    lines: list[str] = []
    for kind, value in blocks:
        if kind == "section":
            lines.extend(("", value.upper()))
        elif kind == "role":
            lines.extend(("", value))
        elif kind == "bullet":
            lines.append("• " + value)
        else:
            lines.append(value)
    target.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Path to output/<version>/resume.md")
    args = parser.parse_args()
    source: Path = args.source
    if source.name != "resume.md" or not source.is_file():
        parser.error("source must be an existing resume.md")
    repo_root = Path(__file__).resolve().parent.parent
    blocks = parse_markdown(source.read_text(encoding="utf-8"))
    validate(blocks, repo_root / "data")
    write_docx(blocks, source.with_suffix(".docx"))
    write_pdf(blocks, source.with_suffix(".pdf"))
    write_txt(blocks, source.with_suffix(".txt"))
    print("Rendered DOCX, PDF, TXT, and Markdown in", source.parent)


if __name__ == "__main__":
    main()
