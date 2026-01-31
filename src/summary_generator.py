# src/summary_generator.py

from typing import List, Dict


def infer_role(jd_text: str) -> str:
    t = jd_text.lower()

    backend_keys = ["backend", "api", "rest", "microservices", "server", "django", "flask"]
    data_keys = ["data analyst", "dashboard", "excel", "reporting", "power bi", "tableau"]
    ml_keys = ["machine learning", "ml", "nlp", "model", "deep learning", "pytorch", "transformers"]
    frontend_keys = ["frontend", "react", "ui", "javascript", "html", "css"]

    if any(k in t for k in backend_keys):
        return "Backend Developer"
    if any(k in t for k in data_keys):
        return "Data Analyst"
    if any(k in t for k in ml_keys):
        return "AI/ML Engineer"
    if any(k in t for k in frontend_keys):
        return "Frontend Developer"
    return "Software Engineer"


def generate_summary(role: str, matched_skills: List[str], missing_by_category: Dict) -> List[str]:
    # pick a few strong matched skills for the summary
    strong = [s for s in matched_skills if s not in {"ms word", "ms excel", "powerpoint"}]
    top = strong[:5] if len(strong) >= 3 else matched_skills[:3]

    if len(top) == 0:
        top = ["problem solving", "programming fundamentals"]

    skills_text = ", ".join(top[:3]) if len(top) >= 3 else ", ".join(top)

    line1 = f"Entry-level {role} with strong fundamentals and hands-on projects using {skills_text}."
    line2 = "Built practical applications involving data processing, automation, and structured skill-matching workflows."
    line3 = "Seeking an entry-level opportunity to contribute, learn fast, and grow in a collaborative engineering team."

    return [line1, line2, line3]


def suggest_keywords(missing_by_category: Dict) -> List[str]:
    core = missing_by_category.get("core", [])
    important = missing_by_category.get("important", [])

    suggestions = core + important
    # remove duplicates but keep order
    seen = set()
    unique = []
    for s in suggestions:
        if s not in seen:
            seen.add(s)
            unique.append(s)

    return unique[:8]