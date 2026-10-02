"""Generic renderer smoke tests; no personal resume data."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

from docx import Document
from pypdf import PdfReader


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "render_resume.py"
SPEC = importlib.util.spec_from_file_location("render_resume", SCRIPT)
renderer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(renderer)


class RendererTest(unittest.TestCase):
    def test_four_formats_and_narrative_guards(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = root / "data"
            data.mkdir()
            (data / "previous-resume.txt").write_text(
                "The source had a long distinctive sentence about a fictional service and its release checks.\n",
                encoding="utf-8",
            )
            (data / "~$lock.docx").write_bytes(b"office lock file, not a document")
            source = root / "resume.md"
            source.write_text(
                "# Sample Candidate\nCity, ST | sample@example.invalid\n"
                "## Summary\nSoftware test engineer focused on reliable releases.\n"
                "## Experience\n### Test Engineer | Example Company | 2020 to 2024\n"
                "- Built regression checks for a service. Improved release confidence for the team.\n"
                "## Skills\nPython, API testing, automation\n",
                encoding="utf-8",
            )
            blocks = renderer.parse_markdown(source.read_text(encoding="utf-8"))
            renderer.validate(blocks, data)
            renderer.write_docx(blocks, root / "resume.docx")
            renderer.write_pdf(blocks, root / "resume.pdf")
            renderer.write_txt(blocks, root / "resume.txt")
            phrase = "Improved release confidence for the team"
            self.assertIn(phrase, " ".join(p.text for p in Document(root / "resume.docx").paragraphs))
            self.assertIn(phrase, PdfReader(root / "resume.pdf").pages[0].extract_text())
            self.assertIn("• Built regression checks", (root / "resume.txt").read_text(encoding="utf-8"))
            headings = [p for p in Document(root / "resume.docx").paragraphs if p.text in {"SUMMARY", "EXPERIENCE", "SKILLS"}]
            self.assertEqual(len(headings), 3)
            self.assertTrue(all(p.alignment == 1 for p in headings))
            self.assertTrue(source.is_file())
            bad_first_person = renderer.parse_markdown("# Sample Candidate\n## Experience\n- I built a framework.\n")
            with self.assertRaises(ValueError):
                renderer.validate(bad_first_person, data)
            for dashed in ("- Built end-to-end checks.", "- Built checks — quickly."):
                with self.assertRaises(ValueError):
                    renderer.validate(renderer.parse_markdown(f"# Sample Candidate\n## Experience\n{dashed}\n"), data)
            (data / "vocabulary.md").write_text(
                "| Write | Meaning | Avoid |\n|---|---|---|\n| test environment | Shared test setup | sandbox, Sandbox |\n",
                encoding="utf-8",
            )
            renderer.validate(blocks, data)
            with self.assertRaises(ValueError):
                renderer.validate(renderer.parse_markdown("# Sample Candidate\n## Experience\n- Built a sandbox.\n"), data)
            bad_copy = renderer.parse_markdown(
                "# Sample Candidate\n## Experience\n"
                "- The source had a long distinctive sentence about a fictional service and its release checks.\n"
            )
            with self.assertRaises(ValueError):
                renderer.validate(bad_copy, data)


if __name__ == "__main__":
    unittest.main()
