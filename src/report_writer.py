import os
import json


def save_report_txt(result:dict,out_path:str)->None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("JOBFIT REPORT\n")
        f.write("=================\n")
        f.write(f"Match Score: {result['score']}%\n")

        # optional weight info (safe even if not present)
        matched_weight = result.get("matched_weight")
        total_weight = result.get("total_weight")
        if matched_weight is not None and total_weight is not None:
            f.write(f"Matched Weight: {matched_weight} / {total_weight}\n")

        role = result.get("role")
        if role:
            f.write(f"\nRole: {role}\n")
            
        summary_lines = result.get("tailored_summary", [])
        if summary_lines:
            f.write("\nTailored Summary:\n")
            for line in summary_lines:
                f.write(f"- {line}\n")
        
        keywords= result.get("keyword_suggestions, []")
        f.write("\nKeyword Suggestions:\n")
        if keywords:
            for kw in keywords:
                f.write(f"- {kw}\n")
        else:
            f.write("- (No core/important keywords missing)\n")
            
        matched = result.get("matched_skills",[])
        missing = result.get("missing_skills", [])
        
        f.write("\nMatched Skills ({}):\n".format(len(result["matched_skills"])))
        for skill in result["matched_skills"]:
            f.write(f"- {skill}\n")

        f.write("\nMissing Skills ({}):\n".format(len(result["missing_skills"])))
        for skill in result["missing_skills"]:
            f.write(f"- {skill}\n")
    
def save_report_json(result:dict,out_path:str)->None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)