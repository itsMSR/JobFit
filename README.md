# JobFit (Resume ↔ Job Description Matcher)

JobFit is a Python CLI tool that compares a resume PDF with a job description PDF and produces:
- Skill match score (weighted)
- Matched vs missing skills
- Missing skills grouped by priority (core / important / nice-to-have)
- Tailored 3-line summary based on the job description
- Keyword suggestions to improve alignment
- TXT + JSON reports

## Features
- PDF text extraction
- Text cleaning + normalization
- Skill detection with safer matching (reduces false positives)
- Alias normalization (e.g., mysql → sql, ml → machine learning)
- Weighted scoring (core skills contribute more)
- Report export (TXT + JSON)

## Project Structure
JOB_FIT/
    src/
        main.py
        pdf_reader.py
        text_cleaner.py
        skills.py
        matcher.py
        summary_generator.py
        report_writer.py
        config.py
    data/
        resume.pdf
        jd.pdf
    reports/
        jobfit_report.txt
        jobfit_report.json


## Setup
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows

pip install -r requirements.txt

python -m src.main --resume data/resume.pdf --jd data/jd.pdf --out reports

## Without saving reports:
python -m src.main --resume data/resume.pdf --jd data/jd.pdf --no-save