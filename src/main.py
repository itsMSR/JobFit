import argparse
import os

from src.pdf_reader import extract_text_from_pdf
from src.text_cleaner import clean_text
from src.skills import SKILLS
from src.matcher import match_resume_to_jd
from src.report_writer import save_report_txt,save_report_json
from src.config import MIN_TEXT_LENGTH,REPORT_DIR
from src.summary_generator import infer_role, generate_summary, suggest_keywords

def parse_args():
    parser = argparse.ArgumentParser(
        prog="jobfit",
        description="JobFit: Match a resume PDF against a job description PDF using skill extraction + weighted scoring."
    )
    
    parser.add_argument("--resume", required=True, help="Path to resume PDF(e.g., data/sample_resume.pdf)")
    parser.add_argument("--jd", required=True, help="Path to job description PDF (e.g., data/sample_jd.pdf)")
    parser.add_argument("--out", default="reports", help="Output directory for reports (default: reports)")
    parser.add_argument("--no-save", action="store_true", help="Do not save TXT/JSON reports")
    
    return parser.parse_args()

def main():
    args = parse_args()
    
    resume_path = args.resume
    jd_path = args.jd
    out_dir = args.out
    
    if not os.path.isfile(resume_path):
        print(f"Error: Resume file not found: {resume_path}")
        return
    if not os.path.isfile(jd_path):
        print(f"Error: JD file not found: {jd_path}")
        return
    
    try:
        resume_text = extract_text_from_pdf(resume_path)
        jd_text = extract_text_from_pdf(jd_path)
    except Exception as e:
        print(f"Error reading resume PDF: {e}")
        return
    
    # clean extracted text
    resume_text = clean_text(resume_text)
    jd_text = clean_text(jd_text)
    
    if len(resume_text)<MIN_TEXT_LENGTH:
        print("Warning: Resume text seems very short. PDF may be scanned or empty.")
    
    if len(jd_text)<MIN_TEXT_LENGTH:
        print("Warning: Job description text seems very short.")
        
    
    result= match_resume_to_jd(resume_text,jd_text,SKILLS)
    
    print("\n===== JOBFIT ANALYSIS =====")
    print(f"Resume skills detected: {result['resume_skill_count']}")
    print(f"JD skills detected: {result['jd_skill_count']}")
    
    
    if result["jd_skill_count"]==0:
        print("No skills detected in job description.Cannot compute a reliable match score.")
        print("Cannot compute a reliable match score.")
        return
    
    print(f"\nMatch Score: {result['score']}%")
    print(f"Matched Weight: {result['matched_weight']} / {result['total_weight']}")
    
    print(f"Matched skills({len(result['matched_skills'])})")
    for skill in result["matched_skills"]:
        print(f"- {skill}")
        
        
    print(f"Missing skills({len(result['missing_skills'])})")
    for skill in result["missing_skills"]:
        print(f"- {skill}")
        
    print("Missing Skills by Priority: ")
    core_missing = result["missing_by_category"]["core"]
    important_missing = result["missing_by_category"]["important"]
    nice_missing = result["missing_by_category"]["nice"]
    
    print(f"Core ({len(core_missing)}):")
    for s in core_missing:
        print(f"- {s}")
        
    print(f"\nImportant ({len(core_missing)}):")
    for s in important_missing:
        print(f"- {s}")
        
    print(f"\nNice-to-have ({len(core_missing)}):")
    for s in nice_missing:
        print(f"- {s}")    
        
    if len(core_missing)>0:
        print("Suggestion: Focus on adding/learning the core missing skills first.")
    elif len(important_missing)>0:
        print("\nSuggestion: Add the IMPORTANT skills if you’ve used them in projects.")
    else:
        print("\nSuggestion: Great match — only nice-to-have skills are missing.")
        
    role = infer_role(jd_text)
    summary_lines = generate_summary(role,result["matched_skills"],result["missing_by_category"])
    keywords = suggest_keywords(result["missing_by_category"])
    
    print("\nTailored Summary:")
    for line in summary_lines:
        print(f"- {line}")

    print("\nKeyword Suggestions:")
    if keywords:
        for kw in keywords:
            print(f"- {kw}")
    else:
        print("- (No core/important keywords missing)")

    # store in result for JSON report
    result["role"] = role
    result["tailored_summary"] = summary_lines
    result["keyword_suggestions"] = keywords
    
    if args.no_save:
        return

    os.makedirs(out_dir,exist_ok=True)
        
    txt_path = os.path.join(out_dir,"jobfit_report.txt")
    json_path = os.path.join(out_dir,"jobfit_report.json")
    
    save_report_txt(result, txt_path)
    save_report_json(result, json_path)

    print(f"\nSaved TXT report to: {txt_path}")
    print(f"Saved JSON report to: {json_path}")
    
if __name__=="__main__":
    main()    
