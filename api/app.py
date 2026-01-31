# api/app.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.pdf_reader import extract_text_from_pdf_bytes
from src.text_cleaner import clean_text
from src.skills import SKILLS
from src.matcher import match_resume_to_jd
from src.config import MIN_TEXT_LENGTH
from src.summary_generator import infer_role, generate_summary, suggest_keywords

MAX_FILE_MB = 8
MAX_FILE_BYTES = MAX_FILE_MB * 1024 * 1024

app = FastAPI(title="JobFit API", version="1.0.0")

# Allow frontend to call API (safe for MVP; tighten later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later: replace with your frontend domain
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


def _validate_pdf(upload: UploadFile, label: str):
    # Content type check (LinkedIn PDFs etc usually set correctly)
    if upload.content_type not in ("application/pdf", "application/x-pdf"):
        raise HTTPException(status_code=400, detail=f"{label} must be a PDF file.")

def _read_limited(upload: UploadFile, label: str) -> bytes:
    data = upload.file.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
        raise HTTPException(status_code=413, detail=f"{label} is too large. Max {MAX_FILE_MB}MB.")
    if len(data) == 0:
        raise HTTPException(status_code=400, detail=f"{label} is empty.")
    return data


@app.post("/analyze")
def analyze(
    resume: UploadFile = File(...),
    jd: UploadFile = File(...),
):
    _validate_pdf(resume, "Resume")
    _validate_pdf(jd, "Job description")

    resume_bytes = _read_limited(resume, "Resume")
    jd_bytes = _read_limited(jd, "Job description")

    # Extract + clean
    try:
        resume_text = extract_text_from_pdf_bytes(resume_bytes)
        jd_text = extract_text_from_pdf_bytes(jd_bytes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PDF parsing failed: {str(e)}")

    resume_text = clean_text(resume_text)
    jd_text = clean_text(jd_text)

    warnings = []
    if len(resume_text) < MIN_TEXT_LENGTH:
        warnings.append("Resume text seems very short. PDF may be scanned or empty.")
    if len(jd_text) < MIN_TEXT_LENGTH:
        warnings.append("Job description text seems very short.")

    # Match
    result = match_resume_to_jd(resume_text, jd_text, SKILLS)

    if result.get("jd_skill_count", 0) == 0:
        raise HTTPException(
            status_code=400,
            detail="No skills detected in job description. Try a clearer JD or paste-text mode (coming soon)."
        )

    # Step 9 extras
    role = infer_role(jd_text)
    summary_lines = generate_summary(role, result["matched_skills"], result["missing_by_category"])
    keywords = suggest_keywords(result["missing_by_category"])

    result["role"] = role
    result["tailored_summary"] = summary_lines
    result["keyword_suggestions"] = keywords
    result["warnings"] = warnings

    return result