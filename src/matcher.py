import re
from src.skills import SKILL_ALIASES,SKILL_WEIGHTS,SKILL_CATEGORIES

def extract_skills(text:str, skills_list: list[str])-> set[str]:
    skill_set = set()
    text_lower = text.lower()
    
    for skill in skills_list:
        skill_lower = skill.lower()
        
        is_special = any(ch in skill_lower for ch in ["+", "#", ".", "-"])
        found = False
        
        if is_special:
            if skill_lower in text_lower:
                found = True
        else:
            escaped_skill = re.escape(skill_lower)
            pattern = rf"\b{escaped_skill}\b"
            if re.search(pattern,text_lower):
                found = True
                
        if found:
            canonical = SKILL_ALIASES.get(skill_lower,skill_lower)
            skill_set.add(canonical)
                
    return skill_set

def match_resume_to_jd(resume_text:str,jd_text:str,skill_list:list[str])-> dict:
    
    resume_skills = extract_skills(resume_text,skill_list)
    jd_skills = extract_skills(jd_text,skill_list)
    
    matched_skills = resume_skills.intersection(jd_skills)
    missing_skills = jd_skills.difference(resume_skills)
    missing_by_category={"core":[],
                         "important":[],
                         "nice":[]}
    
    missing_by_category={"core":[], "important":[], "nice":[]}
    
    for skill in missing_skills:
        category = SKILL_CATEGORIES.get(skill,"nice")
        missing_by_category[category].append(skill)
        
    for cat in missing_by_category:
        missing_by_category[cat] = sorted(missing_by_category[cat])
    
    total_weight = 0
    matched_weight = 0
    
    for skill in jd_skills:
        weight = SKILL_WEIGHTS.get(skill,1)
        total_weight+=weight
        if skill in matched_skills:
            matched_weight += weight
        
    score = matched_weight/total_weight*100 if total_weight>0 else 0.0
        
    result={"score":round(score,1),
            "resume_skills":sorted(resume_skills),
            "jd_skills":sorted(jd_skills),
            "matched_skills":sorted(matched_skills),
            "missing_skills":sorted(missing_skills),
            "total_weight": total_weight,
            "matched_weight": matched_weight,
            "jd_skill_count": len(jd_skills),
            "resume_skill_count": len(resume_skills),
            "missing_by_category":missing_by_category
            }
    
    return result
    