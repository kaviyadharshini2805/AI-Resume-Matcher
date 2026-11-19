import re
import io
from typing import Dict, Any, List, Optional, Tuple, Set
from datetime import datetime

CURRENT_YEAR = 2026
CURRENT_MONTH = 11

# Canonical categorized skills
SKILL_CATEGORIES = {
    "programming_languages": [
        "python", "javascript", "typescript", "java", "c++", "c#", "golang", "ruby", 
        "rust", "php", "swift", "kotlin", "sql", "html", "css", "r", "scala", "bash"
    ],
    "machine_learning": [
        "machine learning", "scikit-learn", "pandas", "numpy", "eda", "data preprocessing", 
        "model evaluation", "feature engineering", "predictive modeling"
    ],
    "deep_learning": [
        "deep learning", "pytorch", "tensorflow", "keras", "cnn", "rnn", "lstm", "computer vision"
    ],
    "nlp_generative_ai": [
        "nlp", "natural language processing", "llm", "llms", "rag", "retrieval-augmented generation", 
        "transformers", "prompt engineering", "langchain", "llama-index", "hugging face", 
        "bert", "semantic search", "embeddings"
    ],
    "backend_frameworks": [
        "fastapi", "flask", "django", "node.js", "express", "spring boot", "graphql", 
        "rest api", "microservices"
    ],
    "databases": [
        "postgresql", "mysql", "mongodb", "redis", "sqlite", "elasticsearch", "cassandra"
    ],
    "cloud_devops": [
        "docker", "kubernetes", "aws", "gcp", "azure", "ci/cd", "git", "github", 
        "linux", "terraform", "agile", "scrum"
    ]
}

# Skill patterns with word boundaries
SKILL_PATTERNS = {
    "python": r"\bpython\b",
    "javascript": r"\bjavascript\b|\bjs\b",
    "typescript": r"\btypescript\b|\bts\b",
    "java": r"\bjava\b",
    "c++": r"\bc\+\+\b",
    "c#": r"\bc\#\b",
    "golang": r"\bgolang\b|\bgo\b",
    "ruby": r"\bruby\b",
    "rust": r"\brust\b",
    "php": r"\bphp\b",
    "swift": r"\bswift\b",
    "kotlin": r"\bkotlin\b",
    "sql": r"\bsql\b",
    "r": r"\br\b(?=\s*(?:programming|scripting|studio|,))",
    "scala": r"\bscala\b",
    "bash": r"\bbash\b|\bshell\s+scripting\b",
    "react": r"\breact(?:\.js)?\b",
    "next.js": r"\bnext(?:\.js)?\b",
    "vue": r"\bvue(?:\.js)?\b",
    "angular": r"\bangular\b",
    "html": r"\bhtml(?:5)?\b",
    "css": r"\bcss(?:3)?\b",
    "tailwind": r"\btailwind(?:\s*css)?\b",
    "fastapi": r"\bfastapi\b",
    "django": r"\bdjango\b",
    "flask": r"\bflask\b",
    "node.js": r"\bnode(?:\.js)?\b",
    "express": r"\bexpress(?:\.js)?\b",
    "spring boot": r"\bspring\s*boot\b",
    "graphql": r"\bgraphql\b",
    "rest api": r"\brest(?:ful)?(?:\s*api)?s?\b",
    "microservices": r"\bmicroservices?\b",
    "postgresql": r"\bpostgres(?:ql)?\b",
    "mysql": r"\bmysql\b",
    "mongodb": r"\bmongo(?:db)?\b",
    "redis": r"\bredis\b",
    "sqlite": r"\bsqlite(?:3)?\b",
    "docker": r"\bdocker\b",
    "kubernetes": r"\bkubernetes\b|\bk8s\b",
    "aws": r"\baws\b|\bamazon\s+web\s+services\b",
    "gcp": r"\bgcp\b|\bgoogle\s+cloud(?:\s+platform)?\b",
    "azure": r"\bazure\b|\bmicrosoft\s+azure\b",
    "ci/cd": r"\bci\s*/\s*cd\b|\bcontinuous\s+integration\b",
    "git": r"\bgit\b",
    "github": r"\bgithub\b",
    "linux": r"\blinux\b",
    "terraform": r"\bterraform\b",
    "machine learning": r"\bmachine\s+learning\b|\bml\b",
    "deep learning": r"\bdeep\s+learning\b|\bdl\b",
    "nlp": r"\bnlp\b|\bnatural\s+language\s+processing\b",
    "pytorch": r"\bpytorch\b|\btorch\b",
    "tensorflow": r"\btensorflow\b|\btf\b",
    "keras": r"\bkeras\b",
    "cnn": r"\bcnn\b|\bconvolutional\s+neural\s+networks?\b",
    "rnn": r"\brnn\b|\brecurrent\s+neural\s+networks?\b",
    "lstm": r"\blstm\b",
    "scikit-learn": r"\bscikit[- ]learn\b|\bsklearn\b",
    "pandas": r"\bpandas\b",
    "numpy": r"\bnumpy\b",
    "eda": r"\beda\b|\bexploratory\s+data\s+analysis\b",
    "data preprocessing": r"\bdata\s+preprocessing\b|\bdata\s+cleaning\b",
    "model evaluation": r"\bmodel\s+evaluation\b|\bvalidation\s+metrics\b",
    "rag": r"\brag\b|\bretrieval[- ]augmented\s+generation\b",
    "transformers": r"\btransformers?\b|\bhugging\s*face\b",
    "llm": r"\bllms?\b|\blarge\s+language\s+models?\b",
    "prompt engineering": r"\bprompt\s+engineering\b",
    "computer vision": r"\bcomputer\s+vision\b|\bcv\b",
    "agile": r"\bagile\b",
    "scrum": r"\bscrum\b",
    "tdd": r"\btdd\b|\btest[- ]driven\b",
    "system design": r"\bsystem\s+design\b"
}

# Related skills taxonomy for semantic relation (never substitutes exact match!)
RELATED_SKILLS_MAP = {
    "fastapi": ["flask", "django", "rest api", "microservices"],
    "flask": ["fastapi", "django", "rest api"],
    "django": ["flask", "fastapi", "rest api"],
    "pytorch": ["tensorflow", "keras", "deep learning"],
    "tensorflow": ["pytorch", "keras", "deep learning"],
    "rag": ["nlp", "llm", "transformers", "semantic search"],
    "llm": ["nlp", "transformers", "rag", "prompt engineering"],
    "nlp": ["llm", "transformers", "text processing"],
    "aws": ["gcp", "azure", "cloud computing"],
    "azure": ["aws", "gcp", "cloud computing"],
    "gcp": ["aws", "azure", "cloud computing"],
    "docker": ["kubernetes", "containerization"],
    "kubernetes": ["docker", "containerization"],
    "postgresql": ["mysql", "sqlite", "sql"],
    "mysql": ["postgresql", "sqlite", "sql"],
    "pandas": ["numpy", "eda", "data preprocessing"],
    "numpy": ["pandas", "scikit-learn"],
    "scikit-learn": ["machine learning", "pandas", "numpy"]
}

MONTH_MAP = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12
}

def extract_name(text: str) -> str:
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    for line in lines[:5]:
        if not re.search(r"(@|https?://|phone|email|resume|curriculum|education|skills|experience|summary)", line, re.IGNORECASE) and len(line) < 40:
            clean = re.sub(r"[^a-zA-Z\s\.\-]", "", line).strip()
            if len(clean.split()) in [2, 3, 4]:
                return clean
    return "Candidate"

def extract_email(text: str) -> str:
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    return match.group(0) if match else "Not specified in resume"

def extract_phone(text: str) -> str:
    match = re.search(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
    return match.group(0) if match else "Not specified in resume"

def extract_location(text: str) -> str:
    match = re.search(r"(?:location|address|city)\s*[:\-]?\s*([a-zA-Z\s,]+(?:,\s*[a-zA-Z\s]+)?)", text, re.IGNORECASE)
    if match:
        loc = match.group(1).strip()
        if len(loc) < 50:
            return loc
    city_match = re.search(r"\b(Bangalore|Bengaluru|San Francisco|New York|Seattle|Austin|Boston|London|Toronto|Chicago|Mumbai|Delhi|Hyderabad|Pune|Chennai)\b(?:,\s*[A-Za-z\s]+)?", text, re.IGNORECASE)
    if city_match:
        return city_match.group(0).strip()
    return "Not specified in resume"

def extract_skills_with_evidence(text: str) -> Dict[str, str]:
    """Extract skills from text and retain the exact supporting line/sentence as evidence."""
    lines = text.split("\n")
    found_skills = {}
    
    for skill_name, pattern in SKILL_PATTERNS.items():
        regex = re.compile(pattern, re.IGNORECASE)
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if regex.search(stripped):
                found_skills[skill_name] = stripped
                break
                
    return found_skills

def extract_skills(text: str) -> List[str]:
    """Return sorted list of detected canonical skill names."""
    return sorted(list(extract_skills_with_evidence(text).keys()))

def categorize_skills(skills_list: List[str]) -> Dict[str, List[str]]:
    """Group extracted skills into clear domains for UI and scoring."""
    categorized = {
        "programming_languages": [],
        "machine_learning": [],
        "deep_learning": [],
        "nlp_generative_ai": [],
        "backend_frameworks": [],
        "databases": [],
        "cloud_devops": [],
        "other": []
    }
    for skill in skills_list:
        placed = False
        for cat, skills in SKILL_CATEGORIES.items():
            if skill in skills:
                categorized[cat].append(skill)
                placed = True
                break
        if not placed:
            categorized["other"].append(skill)
    return categorized

def extract_education(text: str) -> Dict[str, Any]:
    """Extract ONLY qualifications explicitly present in the resume.
    Avoid generating Master's degrees from unrelated keywords like 'systems' or 'algorithms'.
    """
    lines = text.split("\n")
    found_degrees = []
    highest_level = "Not specified in resume"
    has_masters = False
    has_phd = False
    has_bachelors = False
    details_list = []
    
    # 1. Ph.D. detection
    phd_match = re.search(r"\b(ph\.?d\.?|doctorate|doctor\s+of\s+philosophy)\b", text, re.IGNORECASE)
    if phd_match:
        has_phd = True
        highest_level = "Ph.D. / Doctorate"
        found_degrees.append("Ph.D. / Doctorate")

    # 2. Master's degree detection (strict: must NOT match general words)
    masters_match = re.search(
        r"\b(m\.?tech\b|m\.?e\b|m\.?sc\b|mba\b|master(?:'s)?\s+(?:degree|in|of)\s+[a-zA-Z\s]+)",
        text,
        re.IGNORECASE
    )
    if masters_match:
        has_masters = True
        if not has_phd:
            highest_level = "Master's Degree"
        found_degrees.append("Master's Degree")

    # 3. Bachelor's degree detection
    bachelor_match = re.search(
        r"\b(b\.?e\.?\s+(?:in|of)\s+[a-zA-Z\s]+|b\.?e\.?\b|b\.?tech\b|b\.?s\.?\b|b\.?sc\b|bachelor(?:'s)?\s+(?:degree|in|of)\s+[a-zA-Z\s]+|bachelor(?:'s)?\b)",
        text,
        re.IGNORECASE
    )
    if bachelor_match:
        has_bachelors = True
        if not has_phd and not has_masters:
            highest_level = "Bachelor's Degree"
            
        for line in lines:
            if re.search(r"\b(b\.?e\.?|b\.?tech|b\.?s\.?|bachelor)\b", line, re.IGNORECASE):
                details_list.append(line.strip())
                deg_name_match = re.search(r"(b\.?e\.?\s+(?:in\s+)?[a-zA-Z\s]+|b\.?tech\s+(?:in\s+)?[a-zA-Z\s]+|bachelor(?:'s)?(?:\s+of|\s+in|\s+degree)?\s+[a-zA-Z\s]+)", line, re.IGNORECASE)
                deg_label = deg_name_match.group(0).strip() if deg_name_match else "Bachelor's Degree"
                if deg_label not in found_degrees:
                    found_degrees.append(deg_label)
                break
        if not found_degrees:
            found_degrees.append("Bachelor's Degree")

    cgpa_match = re.search(r"\b(?:cgpa|gpa)\s*[:=]?\s*([0-9]+(?:\.[0-9]+)?)\b", text, re.IGNORECASE)
    cgpa_val = cgpa_match.group(1) if cgpa_match else None
    
    edu_years_match = re.search(r"\b(20\d\d)\s*[-–—to]+\s*(20\d\d)\b", " ".join(details_list) if details_list else text)
    edu_years = f"{edu_years_match.group(1)}–{edu_years_match.group(2)}" if edu_years_match else None

    summary_parts = []
    if found_degrees:
        summary_parts.append(", ".join(found_degrees))
    if edu_years:
        summary_parts.append(f"({edu_years})")
    if cgpa_val:
        summary_parts.append(f"CGPA {cgpa_val}")
        
    full_details = " ".join(summary_parts) if summary_parts else "Not specified in resume"

    return {
        "degrees": found_degrees if found_degrees else ["Degree not explicitly identified"],
        "highest_level": highest_level,
        "cgpa": cgpa_val,
        "education_years": edu_years,
        "details": full_details,
        "has_masters": has_masters,
        "has_phd": has_phd,
        "has_bachelors": has_bachelors
    }

def merge_date_intervals(intervals: List[Tuple[int, int]]) -> int:
    """Merge overlapping (start_month_index, end_month_index) to avoid double counting."""
    if not intervals:
        return 0
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = []
    for cur_s, cur_e in sorted_intervals:
        if not merged:
            merged.append([cur_s, cur_e])
        else:
            prev_s, prev_e = merged[-1]
            if cur_s <= prev_e:
                merged[-1][1] = max(prev_e, cur_e)
            else:
                merged.append([cur_s, cur_e])
    total_months = sum((e - s + 1) for s, e in merged)
    return total_months

def extract_experience(text: str) -> Dict[str, Any]:
    """Accurately extract experience while strictly distinguishing professional employment
    from internships, academic projects, and education.
    Never infer experience years from education duration (e.g. 2022-2026).
    Handles current employment (Present / Current / Ongoing).
    Avoids double-counting overlapping employment intervals.
    """
    lines = text.split("\n")
    internships = []
    professional_jobs = []
    current_section = None
    
    month_regex = r"(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember))"
    
    # Pattern 1: Month Year - Month Year
    p1 = re.compile(rf"{month_regex}\s+(\d{{4}})\s*[-–—to]+\s*{month_regex}\s+(\d{{4}})", re.IGNORECASE)
    # Pattern 2: Month Year - Present / Current / Ongoing / Now
    p2 = re.compile(rf"{month_regex}\s+(\d{{4}})\s*[-–—to]+\s*(present|current|ongoing|now)", re.IGNORECASE)
    # Pattern 3: Year - Present (e.g. 2021 - Present)
    p3 = re.compile(r"\b(\d{4})\s*[-–—to]+\s*(present|current|ongoing|now)\b", re.IGNORECASE)
    # Pattern 4: Year - Year (e.g. 2019 - 2021 or 2021 - 2024)
    p4 = re.compile(r"\b(\d{4})\s*[-–—to]+\s*(\d{4})\b", re.IGNORECASE)
    # Direct months (e.g. 3-month internship)
    direct_months_regex = re.compile(r"(\d+)\s*months?\s*(?:internship)?", re.IGNORECASE)
    
    intern_intervals = []
    prof_intervals = []
    
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            continue
            
        upper_line = line_clean.upper()
        if upper_line in ["EDUCATION", "ACADEMICS", "ACADEMIC BACKGROUND"]:
            current_section = "EDUCATION"
            continue
        elif upper_line in ["EXPERIENCE", "WORK EXPERIENCE", "EMPLOYMENT HISTORY", "PROFESSIONAL EXPERIENCE"]:
            current_section = "EXPERIENCE"
            continue
        elif upper_line in ["INTERNSHIP", "INTERNSHIPS", "INTERNSHIP EXPERIENCE"]:
            current_section = "INTERNSHIP"
            continue
        elif upper_line in ["PROJECTS", "ACADEMIC PROJECTS", "PERSONAL PROJECTS"]:
            current_section = "PROJECTS"
            continue
        elif upper_line in ["SKILLS", "TECHNICAL SKILLS", "CERTIFICATIONS"]:
            current_section = "OTHER"
            continue
            
        if current_section == "EDUCATION" or current_section == "PROJECTS":
            continue
            
        is_intern_line = bool(re.search(r"\b(intern|internship|trainee)\b", line_clean, re.IGNORECASE))
        surrounding_text = line_clean
        if i > 0: surrounding_text += " " + lines[i-1]
        if i < len(lines) - 1: surrounding_text += " " + lines[i+1]
        is_intern = is_intern_line or current_section == "INTERNSHIP" or bool(re.search(r"\b(intern|internship|trainee)\b", surrounding_text, re.IGNORECASE))

        # Check Pattern 1: Month Year - Month Year
        m1 = p1.search(line_clean)
        # Check Pattern 2: Month Year - Present
        m2 = p2.search(line_clean)
        # Check Pattern 3: Year - Present
        m3 = p3.search(line_clean)
        # Check Pattern 4: Year - Year (only if in experience section or has job keywords)
        m4 = p4.search(line_clean) if (current_section in ["EXPERIENCE", "INTERNSHIP"] or re.search(r"engineer|developer|scientist|specialist|lead|analyst", line_clean, re.IGNORECASE)) else None
        
        start_idx = None
        end_idx = None
        date_str = None
        
        if m1:
            sm, sy, em, ey = m1.groups()
            s_month = MONTH_MAP.get(sm.lower(), 1)
            s_year = int(sy)
            e_month = MONTH_MAP.get(em.lower(), 1)
            e_year = int(ey)
            start_idx = s_year * 12 + s_month
            end_idx = e_year * 12 + e_month
            date_str = f"{sm.capitalize()} {s_year} – {em.capitalize()} {e_year}"
        elif m2:
            sm, sy, _ = m2.groups()
            s_month = MONTH_MAP.get(sm.lower(), 1)
            s_year = int(sy)
            start_idx = s_year * 12 + s_month
            end_idx = CURRENT_YEAR * 12 + CURRENT_MONTH
            date_str = f"{sm.capitalize()} {s_year} – Present"
        elif m3:
            sy, _ = m3.groups()
            s_year = int(sy)
            start_idx = s_year * 12 + 1
            end_idx = CURRENT_YEAR * 12 + CURRENT_MONTH
            date_str = f"{s_year} – Present"
        elif m4:
            sy, ey = m4.groups()
            s_year, e_year = int(sy), int(ey)
            if 2000 <= s_year <= CURRENT_YEAR and s_year <= e_year <= CURRENT_YEAR + 1:
                start_idx = s_year * 12 + 1
                end_idx = e_year * 12 + 12
                date_str = f"{s_year} – {e_year}"
                
        if start_idx is not None and end_idx is not None and end_idx >= start_idx:
            duration = end_idx - start_idx + 1
            if is_intern:
                intern_intervals.append((start_idx, end_idx))
                internships.append({
                    "title": line_clean,
                    "months": duration,
                    "date_str": date_str,
                    "is_internship": True
                })
            else:
                prof_intervals.append((start_idx, end_idx))
                professional_jobs.append({
                    "title": line_clean,
                    "months": duration,
                    "date_str": date_str,
                    "is_internship": False
                })
        else:
            direct_match = direct_months_regex.search(line_clean)
            if direct_match and is_intern:
                months_val = int(direct_match.group(1))
                internships.append({
                    "title": line_clean,
                    "months": months_val,
                    "date_str": f"{months_val} months",
                    "is_internship": True
                })
                # Synthesize interval if not present
                intern_intervals.append((CURRENT_YEAR * 12, CURRENT_YEAR * 12 + months_val - 1))

    # Merge intervals to prevent double-counting overlapping jobs
    total_internship_months = merge_date_intervals(intern_intervals)
    total_prof_months = merge_date_intervals(prof_intervals)
    prof_years = round(total_prof_months / 12, 1) if total_prof_months > 0 else 0.0

    if total_prof_months == 0 and total_internship_months > 0:
        intern_dates = internships[0].get("date_str", "") if internships else ""
        date_suffix = f" ({intern_dates})" if intern_dates else ""
        display_exp = f"{total_internship_months} months internship{date_suffix}"
        summary_exp = f"Candidate has {total_internship_months} months of internship experience{date_suffix} and 0 years of full-time professional employment."
        is_intern_only = True
    elif total_prof_months > 0 and total_internship_months > 0:
        display_exp = f"{prof_years} years professional experience + {total_internship_months} months internship"
        summary_exp = f"Candidate has {prof_years} years of professional employment plus {total_internship_months} months of internship experience."
        is_intern_only = False
    elif total_prof_months > 0:
        display_exp = f"{prof_years} years professional experience"
        summary_exp = f"Candidate has {prof_years} years of professional experience."
        is_intern_only = False
    else:
        display_exp = "Not specified in resume (Fresh graduate / Entry-level)"
        summary_exp = "No professional employment or internship tenure specified in resume."
        is_intern_only = False

    return {
        "professional_years": prof_years,
        "professional_months": total_prof_months,
        "internship_months": total_internship_months,
        "internships": internships,
        "professional_jobs": professional_jobs,
        "is_internship_only": is_intern_only,
        "display": display_exp,
        "summary": summary_exp
    }

def extract_experience_years(text: str) -> float:
    exp = extract_experience(text)
    if exp["professional_years"] > 0:
        return exp["professional_years"]
    if exp["internship_months"] > 0:
        return round(exp["internship_months"] / 12, 2)
    return 0.0

def extract_projects(text: str) -> List[Dict[str, str]]:
    projects = []
    lines = text.split("\n")
    in_projects_section = False
    current_project = None
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        upper = stripped.upper()
        if any(h in upper for h in ["PROJECTS", "ACADEMIC PROJECTS", "KEY PROJECTS", "PERSONAL PROJECTS"]):
            in_projects_section = True
            continue
        elif in_projects_section and upper in ["SKILLS", "EDUCATION", "EXPERIENCE", "CERTIFICATIONS", "ACHIEVEMENTS"]:
            in_projects_section = False
            break
            
        if in_projects_section:
            if re.search(r"^[•\-\*]?\s*([A-Z][a-zA-Z0-9\s\-_]+(?:\([^\)]+\))?)$", stripped) and len(stripped) < 70 and not stripped.startswith("- Developed") and not stripped.startswith("- Built"):
                if current_project:
                    projects.append(current_project)
                title = re.sub(r"^[•\-\*]\s*", "", stripped)
                is_academic = bool(re.search(r"academic|coursework|university", title, re.IGNORECASE))
                current_project = {
                    "title": title,
                    "description": "",
                    "is_academic": is_academic,
                    "technologies": []
                }
            elif current_project:
                current_project["description"] += " " + stripped
                for skill_name, pattern in SKILL_PATTERNS.items():
                    if re.search(pattern, stripped, re.IGNORECASE) and skill_name not in current_project["technologies"]:
                        current_project["technologies"].append(skill_name)
                        
    if current_project:
        projects.append(current_project)
        
    return projects

def extract_certifications(text: str) -> List[str]:
    certs = []
    lines = text.split("\n")
    in_certs = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        upper = stripped.upper()
        if "CERTIFICATION" in upper or "CERTIFICATES" in upper:
            in_certs = True
            continue
        elif in_certs and upper in ["SKILLS", "EDUCATION", "EXPERIENCE", "PROJECTS"]:
            in_certs = False
            break
        if in_certs:
            clean = re.sub(r"^[•\-\*]\s*", "", stripped)
            if clean:
                certs.append(clean)
    return certs

def parse_resume_text(text: str) -> Dict[str, Any]:
    exp_info = extract_experience(text)
    edu_info = extract_education(text)
    skills_with_evidence = extract_skills_with_evidence(text)
    skills_list = sorted(list(skills_with_evidence.keys()))
    categorized = categorize_skills(skills_list)
    projects = extract_projects(text)
    certs = extract_certifications(text)
    email = extract_email(text)
    phone = extract_phone(text)
    location = extract_location(text)
    name = extract_name(text)
    
    missing_fields = []
    if email == "Not specified in resume":
        missing_fields.append("Email")
    if phone == "Not specified in resume":
        missing_fields.append("Phone")
    if not skills_list:
        missing_fields.append("Technical Skills")
    if edu_info["highest_level"] == "Not specified in resume":
        missing_fields.append("Education Qualifications")
    if exp_info["display"].startswith("Not specified"):
        missing_fields.append("Employment Tenure")
        
    needs_manual_review = len(missing_fields) >= 2 or not skills_list
    
    return {
        "candidate_name": name,
        "email": email,
        "phone": phone,
        "location": location,
        "skills": skills_list,
        "skills_evidence": skills_with_evidence,
        "categorized_skills": categorized,
        "education": edu_info["degrees"],
        "education_details": edu_info,
        "experience": exp_info,
        "experience_years": exp_info["professional_years"],
        "experience_display": exp_info["display"],
        "projects": projects,
        "certifications": certs,
        "missing_fields": missing_fields,
        "needs_manual_review": needs_manual_review,
        "raw_text_length": len(text),
        "summary": text[:350].strip() + ("..." if len(text) > 350 else "")
    }

def parse_resume_file(file_bytes: bytes, filename: str) -> Dict[str, Any]:
    text = ""
    lower_fn = filename.lower()
    
    if lower_fn.endswith(".pdf"):
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            text = "\n".join([page.extract_text() or "" for page in reader.pages])
        except Exception:
            text = file_bytes.decode("utf-8", errors="ignore")
    elif lower_fn.endswith(".docx"):
        try:
            import docx
            doc = docx.Document(io.BytesIO(file_bytes))
            text = "\n".join([para.text for para in doc.paragraphs if para.text])
        except Exception:
            text = file_bytes.decode("utf-8", errors="ignore")
    else:
        text = file_bytes.decode("utf-8", errors="ignore")
        
    parsed = parse_resume_text(text)
    parsed["filename"] = filename
    parsed["raw_text"] = text
    return parsed
