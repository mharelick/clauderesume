# Windows setup

Extract this package directly into the root of your checked-out GitHub repository. It does not include a `.git` directory or `README.md`. Open that repository folder in Claude Desktop on Windows.

Install Python 3 and the local document dependencies once, from a terminal in the repository root:

```powershell
python -m pip install -r requirements.txt
```

Put at least one existing resume in the root `data\` directory. You may also put supporting notes and job-description files there. Claude creates the concise, editable `data\history.md` on the first run. You can paste a job description into Claude instead of saving it as a file. Invoke `/resume-customizer` with the target description, a path, or a platform profile purpose; ordinary career narrative can be shared for history capture without a target posting.

Each requested version gets its own `output\YYYY-MM-DD_company_role\` or `output\YYYY-MM-DD_profile_platform\` directory. It contains `resume.docx`, `resume.pdf`, `resume.txt`, `resume.md`, and `notes.md`. Claude generates all four resume formats in the same run.

`data\` and `output\` are ignored by Git even though they are inside the repository folder. Before committing, check `git status --short` and the staged diff. Git ignore rules do not remove files that were already tracked. The included instructions and renderer are generic; do not put personal career information into public tracked files.
