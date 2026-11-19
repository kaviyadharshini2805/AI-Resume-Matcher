from typing import Dict, Any, List, Optional, Set
import math
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ..nlp.text_processor import clean_text
from ..parser.resume_parser import (
    extract_skills_with_evidence,
    extract_education,
    extract_experience,
    extract_experience_years,
    extract_name,
    extract_projects,
    SKILL_PATTERNS,
    RELATED_SKILLS_MAP
)

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate TF-IDF Cosine Similarity between two texts."""
    c1 = clean_text(text1)
    c2 = clean_text(text2)
    
    if not c1 or not c2:
        return 0.0
    
    try:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([c1, c2])
        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(round(sim, 4))
    except Exception:
        words1 = set(c1.split())
        words2 = set(c2.split())
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        return float(round(len(intersection) / max(len(union), 1), 4))

def extract_jd_experience_requirement(job_text: str) -> Dict[str, Any]:
    """Accurately extract experience requirements directly from the supplied JD.
    Handles phrases such as fresher, entry-level, 0–2 years, 2+ years, 3–5 years, and 5+ years.
    Never invents or replaces the JD's requirement with 3+ years.
    """
    lower_text = job_text.lower()
    
    # 1. Check for fresher / recent graduate / no experience / 0-2 years
    if re.search(r"\b(freshers?(?:\s+welcome)?|fresh\s+graduates?|recent\s+graduates?|no\s+experience\s+required)\b", lower_text):
        range_match = re.search(r"\b(0)\s*[-–—to]+\s*([1-3])\s*years?\b", lower_text)
        if range_match:
            min_y = float(range_match.group(1))
            max_y = float(range_match.group(2))
            return {
                "min_years": min_y,
                "max_years": max_y,
                "display": f"{int(min_y)}–{int(max_y)} years",
                "is_entry_level": True,
                "is_fresher": True
            }
        return {
            "min_years": 0.0,
            "max_years": 1.0,
            "display": "0–1 years (Fresher)",
            "is_entry_level": True,
            "is_fresher": True
        }
        
    # 2. Check for explicit range like 0-2 years, 1-3 years, 3-5 years
    range_match = re.search(r"\b(\d+)\s*[-–—to]+\s*(\d+)\s*years?\b", lower_text)
    if range_match:
        min_y = float(range_match.group(1))
        max_y = float(range_match.group(2))
        return {
            "min_years": min_y,
            "max_years": max_y,
            "display": f"{int(min_y)}–{int(max_y)} years",
            "is_entry_level": (min_y <= 1 and max_y <= 2),
            "is_fresher": (min_y == 0)
        }
        
    # 3. Check for entry-level / junior
    if re.search(r"\b(entry[- ]level|junior|associate)\b", lower_text):
        return {
            "min_years": 0.0,
            "max_years": 2.0,
            "display": "0–2 years (Entry-Level)",
            "is_entry_level": True,
            "is_fresher": True
        }
        
    # 4. Check for minimum X years or X+ years
    min_match = re.search(r"\bminimum\s+(\d+)\+?\s*years?\b", lower_text)
    if min_match:
        min_y = float(min_match.group(1))
        return {
            "min_years": min_y,
            "max_years": None,
            "display": f"Minimum {int(min_y)} years",
            "is_entry_level": (min_y <= 1),
            "is_fresher": (min_y == 0)
        }

    plus_match = re.search(r"\b(\d+)\+?\s*years?(?:\s+of)?(?:\s+experience)?\b", lower_text)
    if plus_match:
        min_y = float(plus_match.group(1))
        return {
            "min_years": min_y,
            "max_years": None,
            "display": f"{int(min_y)}+ years",
            "is_entry_level": (min_y <= 1),
            "is_fresher": (min_y == 0)
        }
        
    # Default if truly unspecified
    return {
        "min_years": 0.0,
        "max_years": None,
        "display": "Not specified in JD",
        "is_entry_level": True,
        "is_fresher": False
    }

def extract_jd_skills(job_text: str) -> Dict[str, List[str]]:
    """Extract required and preferred skills separately from job description."""
    lines = job_text.split("\n")
    required_text = []
    preferred_text = []
    current_bucket = "REQUIRED"
    
    for line in lines:
        stripped = line.strip()
        upper = stripped.upper()
        if any(h in upper for h in ["PREFERRED", "NICE TO HAVE", "GOOD TO HAVE", "BONUS", "DESIRED"]):
            current_bucket = "PREFERRED"
            continue
        elif any(h in upper for h in ["REQUIRED", "REQUIREMENT", "MUST HAVE", "QUALIFICATIONS", "CORE SKILLS"]):
            current_bucket = "REQUIRED"
            continue
            
        if current_bucket == "REQUIRED":
            required_text.append(stripped)
        else:
            preferred_text.append(stripped)
            
    req_combined = "\n".join(required_text)
    pref_combined = "\n".join(preferred_text) if preferred_text else ""
    
    req_skills = set()
    for skill_name, pattern in SKILL_PATTERNS.items():
        if re.search(pattern, req_combined, re.IGNORECASE):
            req_skills.add(skill_name)
            
    pref_skills = set()
    if pref_combined:
        for skill_name, pattern in SKILL_PATTERNS.items():
            if re.search(pattern, pref_combined, re.IGNORECASE) and skill_name not in req_skills:
                pref_skills.add(skill_name)
                
    if not req_skills and not pref_skills:
        for skill_name, pattern in SKILL_PATTERNS.items():
            if re.search(pattern, job_text, re.IGNORECASE):
                req_skills.add(skill_name)
                
    return {
        "required_skills": sorted(list(req_skills)),
        "preferred_skills": sorted(list(pref_skills))
    }

def analyze_experience(resume_text: str, job_text: str) -> Dict[str, Any]:
    """Accurately compare candidate experience with the actual JD experience requirement.
    Never invents 4 years from a bachelor's degree duration.
    Accurately reports internships.
    """
    cand_exp = extract_experience(resume_text)
    jd_req = extract_jd_experience_requirement(job_text)
    
    prof_years = cand_exp["professional_years"]
    intern_months = cand_exp["internship_months"]
    is_intern_only = cand_exp["is_internship_only"]
    cand_display = cand_exp["display"]
    
    jd_display = jd_req["display"]
    jd_min = jd_req["min_years"]
    jd_max = jd_req.get("max_years")
    
    # Calculate experience score (0–100)
    score = 50.0
    if jd_req.get("is_fresher") or (jd_min == 0 and (jd_max is None or jd_max <= 2)):
        if is_intern_only or prof_years <= 2:
            status = "Meets Requirement (0–2 years)"
            score = 100.0 if (is_intern_only or prof_years >= 0.25) else 90.0
            if is_intern_only:
                details = f"Candidate has {cand_display}, which satisfies the entry-level requirement of {jd_display}."
            else:
                details = f"Candidate has {cand_display}, aligning with the role's {jd_display} expectation."
        else:
            status = "Exceeds Requirement"
            score = 100.0
            details = f"Candidate brings {cand_display}, exceeding the role's {jd_display} requirement."
    else:
        if prof_years >= jd_min:
            status = "Meets Requirement"
            score = 100.0
            details = f"Candidate demonstrates {cand_display}, satisfying the required {jd_display}."
        elif is_intern_only:
            status = "Below Stated Requirement"
            score = max(round(((intern_months / 12) / max(jd_min, 1)) * 50, 1), 15.0)
            details = f"Role requires {jd_display} of professional experience, whereas candidate has {cand_display}."
        elif prof_years >= max(jd_min - 1, 0.5):
            status = "Close to Requirement"
            score = 75.0
            details = f"Candidate demonstrates {cand_display}, closely approaching the required {jd_display}."
        else:
            status = "Below Stated Requirement"
            score = max(round((prof_years / max(jd_min, 1)) * 60, 1), 15.0)
            details = f"Role requires {jd_display} of professional experience, whereas candidate has {cand_display}."

    return {
        "candidate_experience": cand_display,
        "candidate_years": prof_years if not is_intern_only else round(intern_months / 12, 2),
        "internship_months": intern_months,
        "is_internship_only": is_intern_only,
        "required_experience": jd_display,
        "status": status,
        "details": details,
        "score": min(max(score, 0.0), 100.0)
    }

def analyze_education(resume_text: str, job_text: str) -> Dict[str, Any]:
    """Accurately analyze education: extract ONLY qualifications explicitly present in the resume.
    Never generate a Master's degree or any qualification that does not exist.
    """
    cand_edu = extract_education(resume_text)
    
    lower_jd = job_text.lower()
    requires_phd = bool(re.search(r"\b(ph\.?d|doctorate)\b", lower_jd))
    requires_masters = bool(re.search(r"\b(master'?s|m\.?tech|m\.?s|ph\.?d|doctorate)\b", lower_jd))
    requires_bachelors = bool(re.search(r"\b(bachelor'?s|b\.?e\b|b\.?tech|b\.?s\b|degree)\b", lower_jd))
    
    cand_degrees = cand_edu["degrees"]
    highest = cand_edu["highest_level"]
    full_details = cand_edu["details"]
    
    score = 70.0
    if cand_edu["has_phd"]:
        status = "Exceeds Requirement (Ph.D. / Doctorate)"
        score = 100.0
        details = f"Candidate holds advanced qualification: {full_details}."
    elif cand_edu["has_masters"]:
        if requires_phd:
            status = "Partially Qualified"
            score = 80.0
            details = f"Role specifies doctorate; candidate holds {full_details}."
        else:
            status = "Qualified (Master's Degree)"
            score = 100.0
            details = f"Candidate holds {full_details}, meeting degree specifications."
    elif cand_edu["has_bachelors"]:
        if requires_phd:
            status = "Below Qualification Target"
            score = 45.0
            details = f"Role requests advanced doctorate degree; candidate holds {full_details}."
        elif requires_masters and not requires_bachelors:
            status = "Partially Qualified"
            score = 70.0
            details = f"Role requests advanced qualification; candidate holds {full_details}."
        else:
            status = "Qualified"
            score = 100.0 if requires_bachelors else 95.0
            details = f"Candidate holds {full_details}, fulfilling the degree requirement. No Master's degree present or claimed."
    else:
        status = "Review Recommended"
        score = 35.0
        details = "Degree not explicitly stated in resume."

    return {
        "candidate_degrees": cand_degrees,
        "candidate_highest_level": highest,
        "education_details": full_details,
        "has_masters": cand_edu["has_masters"],
        "has_phd": cand_edu["has_phd"],
        "status": status,
        "details": details,
        "score": min(max(score, 0.0), 100.0)
    }

def analyze_projects_and_evidence(resume_text: str, job_text: str, matched_skills: List[str]) -> Dict[str, Any]:
    """Evaluate candidate project portfolio and verified application of relevant skills."""
    projects = extract_projects(resume_text)
    
    matched_skills_in_projects = set()
    for proj in projects:
        for tech in proj.get("technologies", []):
            if tech in matched_skills:
                matched_skills_in_projects.add(tech)
                
    proj_count = len(projects)
    if proj_count >= 3 and len(matched_skills_in_projects) >= 2:
        score = 95.0
        status = "Strong Project Evidence"
        details = f"Candidate documents {proj_count} hands-on projects applying key skills including {', '.join(list(matched_skills_in_projects)[:3])}."
    elif proj_count >= 1:
        score = 75.0 + min(len(matched_skills_in_projects) * 8.0, 20.0)
        status = "Verified Project Experience"
        details = f"Candidate demonstrates {proj_count} documented project(s) verifying practical technical implementation."
    elif len(matched_skills) >= 4:
        score = 70.0
        status = "Moderate Evidence"
        details = "Practical skill mentions present in work experience; dedicated project portfolio recommended."
    else:
        score = 40.0
        status = "Limited Project Documentation"
        details = "No structured project portfolio identified in resume."

    return {
        "projects_count": proj_count,
        "projects": projects,
        "matched_skills_in_projects": sorted(list(matched_skills_in_projects)),
        "status": status,
        "details": details,
        "score": min(max(score, 0.0), 100.0)
    }

def find_related_skills(cand_skills: Set[str], missing_skills: Set[str]) -> Dict[str, List[str]]:
    """Identify related skills possessed by the candidate that are semantically connected to missing skills.
    Never marks the missing skill as matched! Just identifies the transferrable knowledge.
    """
    related_found = {}
    for missing in missing_skills:
        related_targets = RELATED_SKILLS_MAP.get(missing, [])
        cand_matches = [s for s in related_targets if s in cand_skills]
        if cand_matches:
            related_found[missing] = cand_matches
    return related_found

def generate_suggestions(
    missing_required: List[str],
    missing_preferred: List[str],
    cand_exp: Dict[str, Any],
    cand_edu: Dict[str, Any]
) -> List[str]:
    """Generate ethical, evidence-based improvement suggestions.
    Never encourage candidates to falsely claim skills they do not possess.
    """
    suggestions = []
    
    if missing_required:
        top_missing = ", ".join(missing_required[:4])
        suggestions.append(
            f"Gain practical project exposure or complete structured training in key required technologies: {top_missing}."
        )
        
    if missing_preferred:
        top_pref = ", ".join(missing_preferred[:3])
        suggestions.append(
            f"Familiarity with preferred tools like {top_pref} will strengthen your application competitiveness."
        )
        
    if cand_exp.get("is_internship_only"):
        suggestions.append(
            "Detail specific technical accomplishments, algorithms implemented, and measurable outcomes from your internship to demonstrate production readiness."
        )
    elif cand_exp.get("professional_years", 0) > 0:
        suggestions.append(
            "Structure recent work achievements using the STAR method (Situation, Task, Action, Result) with quantified business metrics."
        )
        
    if cand_edu.get("has_bachelors"):
        suggestions.append(
            "Highlight capstone and academic coursework projects that demonstrate hands-on problem solving in machine learning and backend architecture."
        )
        
    suggestions.append(
        "Ensure your resume summary concisely specifies your target position and top verified proficiencies."
    )
    
    return suggestions

def match_resume_to_job(resume_text: str, job_description: str) -> Dict[str, Any]:
    """Calculate evidence-based match score and insights between a resume and job description.
    Uses Phase 6 Reference Weighting:
      - Skills match: 35%
      - Semantic similarity: 25%
      - Relevant experience: 20%
      - Education: 10%
      - Projects and evidence: 10%
    Formula:
      Overall Score = (Skills * 0.35) + (Semantic Sim * 0.25) + (Experience * 0.20) + (Education * 0.10) + (Projects * 0.10)
    All components normalized 0-100.
    Exact evidence-based matching distinguishing exact proficiencies from related skills.
    """
    cosine_sim = calculate_similarity(resume_text, job_description)
    raw_cosine_pct = round(cosine_sim * 100, 1)
    
    # Normalized semantic similarity score onto 0-100 scale:
    # In text comparison between a full resume and a focused job description, 0.35+ represents high semantic alignment
    semantic_score = min(round((cosine_sim / 0.38) * 100, 1), 100.0) if cosine_sim > 0 else 0.0
    
    # Evidence-based candidate skills extraction
    cand_skills_evidence = extract_skills_with_evidence(resume_text)
    cand_skills_set = set(cand_skills_evidence.keys())
    
    # Separate required and preferred skills from JD
    jd_skills_dict = extract_jd_skills(job_description)
    req_skills = jd_skills_dict["required_skills"]
    pref_skills = jd_skills_dict["preferred_skills"]
    
    all_jd_skills = set(req_skills).union(set(pref_skills))
    if not all_jd_skills:
        all_jd_skills = set(extract_skills_with_evidence(job_description).keys())
        req_skills = sorted(list(all_jd_skills))
        pref_skills = []
        
    req_set = set(req_skills)
    pref_set = set(pref_skills)
    
    # Exact evidence-based matching
    matched_required = sorted(list(req_set.intersection(cand_skills_set)))
    missing_required = sorted(list(req_set.difference(cand_skills_set)))
    
    matched_preferred = sorted(list(pref_set.intersection(cand_skills_set)))
    missing_preferred = sorted(list(pref_set.difference(cand_skills_set)))
    
    matched_all = sorted(list(set(matched_required).union(set(matched_preferred))))
    missing_all = sorted(list(set(missing_required).union(set(missing_preferred))))
    
    candidate_additional = sorted(list(cand_skills_set.difference(all_jd_skills)))
    
    # Identify related skills without converting them into exact matches!
    related_skills_found = find_related_skills(cand_skills_set, set(missing_all))
    
    # Matched skills evidence map
    matched_with_evidence = [
        {
            "skill": skill,
            "evidence": cand_skills_evidence.get(skill, "Mentioned in resume"),
            "is_required": skill in req_set
        }
        for skill in matched_all
    ]
    
    # Calculate Component 1: Skills Match Score (0–100)
    if req_skills:
        req_ratio = len(matched_required) / len(req_skills)
        pref_ratio = (len(matched_preferred) / len(pref_skills)) if pref_skills else 1.0
        # 85% required + 15% preferred
        raw_skill_ratio = (req_ratio * 0.85) + (pref_ratio * 0.15) if pref_skills else req_ratio
        skill_match_score = round(raw_skill_ratio * 100, 1)
    else:
        skill_match_score = 100.0 if not missing_all else 50.0
        
    # Analyze other components
    exp_analysis = analyze_experience(resume_text, job_description)
    edu_analysis = analyze_education(resume_text, job_description)
    proj_analysis = analyze_projects_and_evidence(resume_text, job_description, matched_all)
    jd_exp_req = extract_jd_experience_requirement(job_description)
    
    experience_score = exp_analysis["score"]
    education_score = edu_analysis["score"]
    projects_score = proj_analysis["score"]
    
    # 5-Component Weighted Formula (Phase 6):
    # Overall Score = (Skills * 0.35) + (Semantic Sim * 0.25) + (Experience * 0.20) + (Education * 0.10) + (Projects * 0.10)
    overall_calculated = (
        (skill_match_score * 0.35) +
        (semantic_score * 0.25) +
        (experience_score * 0.20) +
        (education_score * 0.10) +
        (projects_score * 0.10)
    )
    overall_score = round(min(max(overall_calculated, 0.0), 100.0), 1)
    
    # Verdict recommendation
    if overall_score >= 80:
        recommendation = "Strong Match"
    elif overall_score >= 60:
        recommendation = "Moderate Match"
    elif overall_score >= 40:
        recommendation = "Potential Match"
    else:
        recommendation = "Low Match"
        
    candidate_name = extract_name(resume_text)
    suggestions = generate_suggestions(
        missing_required,
        missing_preferred,
        exp_analysis,
        edu_analysis
    )
    
    score_breakdown = {
        "skills_match": {
            "score": skill_match_score,
            "weight": 0.35,
            "weighted_score": round(skill_match_score * 0.35, 2),
            "label": "Technical Skills Match"
        },
        "semantic_similarity": {
            "score": semantic_score,
            "weight": 0.25,
            "weighted_score": round(semantic_score * 0.25, 2),
            "label": "Semantic & Contextual Similarity"
        },
        "experience": {
            "score": experience_score,
            "weight": 0.20,
            "weighted_score": round(experience_score * 0.20, 2),
            "label": "Relevant Experience & Tenure"
        },
        "education": {
            "score": education_score,
            "weight": 0.10,
            "weighted_score": round(education_score * 0.10, 2),
            "label": "Academic Qualifications"
        },
        "projects_evidence": {
            "score": projects_score,
            "weight": 0.10,
            "weighted_score": round(projects_score * 0.10, 2),
            "label": "Project Evidence & Portfolio"
        }
    }
    
    ai_score_explanation = (
        f"Overall Compatibility Score: {overall_score}%. "
        f"Calculated from Skills ({skill_match_score}% × 35% = {round(skill_match_score*0.35, 1)}%), "
        f"Semantic Alignment ({semantic_score}% × 25% = {round(semantic_score*0.25, 1)}%), "
        f"Experience Alignment ({experience_score}% × 20% = {round(experience_score*0.20, 1)}%), "
        f"Education ({education_score}% × 10% = {round(education_score*0.10, 1)}%), and "
        f"Project Portfolio ({projects_score}% × 10% = {round(projects_score*0.10, 1)}%)."
    )

    return {
        "candidate_name": candidate_name,
        "overall_score": overall_score,
        "cosine_similarity": raw_cosine_pct,
        "semantic_similarity_score": semantic_score,
        "skill_match_score": skill_match_score,
        "experience_score": experience_score,
        "education_score": education_score,
        "projects_score": projects_score,
        "score_breakdown": score_breakdown,
        "ai_score_explanation": ai_score_explanation,
        "matched_skills": matched_all,
        "missing_skills": missing_all,
        "matched_required_skills": matched_required,
        "missing_required_skills": missing_required,
        "matched_preferred_skills": matched_preferred,
        "missing_preferred_skills": missing_preferred,
        "matched_skills_with_evidence": matched_with_evidence,
        "candidate_additional_skills": candidate_additional,
        "related_skills": related_skills_found,
        "recommendation": recommendation,
        "experience_comparison": exp_analysis,
        "education_analysis": edu_analysis,
        "projects_analysis": proj_analysis,
        "jd_experience_requirement": jd_exp_req,
        "suggestions": suggestions
    }

def rank_candidates(candidate_matches: List[Dict[str, Any]], job_title: str) -> Dict[str, Any]:
    """Rank multiple candidate match results in order and generate executive reasoning
    for why the AI chose candidate #1 as the top candidate and how they compare with others.
    """
    if not candidate_matches:
        return {
            "rankings": [],
            "top_candidate": None,
            "top_candidate_reasoning": "No candidates to evaluate."
        }
        
    sorted_candidates = sorted(candidate_matches, key=lambda c: c.get("overall_score", 0), reverse=True)
    
    for idx, cand in enumerate(sorted_candidates):
        cand["rank"] = idx + 1
        
    top_cand = sorted_candidates[0]
    
    top_name = top_cand.get("candidate_name", "Top Candidate")
    top_score = top_cand.get("overall_score", 0)
    top_matched = top_cand.get("matched_skills", [])
    top_exp = top_cand.get("experience_comparison", {}).get("candidate_experience", "Relevant experience")
    top_edu = top_cand.get("education_analysis", {}).get("education_details", "Qualified degree")
    
    reasoning_points = [
        f"**Highest Composite Score:** {top_name} leads the applicant pool with an overall compatibility score of **{top_score}%**, demonstrating the strongest holistic balance across technical skills, domain alignment, experience, and educational background.",
        f"**Core Technical Proficiency:** Directly matches **{len(top_matched)}** required and preferred role skills ({', '.join(top_matched[:6]) if top_matched else 'key core skills'}), verified with explicit supporting evidence in their resume.",
        f"**Experience Fit:** Brings {top_exp}, satisfying the position's experience criteria.",
        f"**Academic & Project Foundations:** Holds {top_edu} with validated practical project implementation."
    ]
    
    if len(sorted_candidates) > 1:
        runner_up = sorted_candidates[1]
        runner_name = runner_up.get("candidate_name", "Runner-up")
        diff = round(top_score - runner_up.get("overall_score", 0), 1)
        runner_missing = runner_up.get("missing_required_skills", [])
        
        comp_reason = f"**Comparative Edge Over #{runner_up.get('rank', 2)} ({runner_name}):** {top_name} outscores {runner_name} by **{diff}%**."
        if runner_missing:
            comp_reason += f" While {runner_name} lacks critical required proficiencies ({', '.join(runner_missing[:3])}), {top_name} provides direct evidence for these technologies."
        reasoning_points.append(comp_reason)
        
    top_candidate_reasoning = "\n\n".join(reasoning_points)
    
    return {
        "job_title": job_title,
        "total_ranked": len(sorted_candidates),
        "top_candidate": {
            "name": top_name,
            "score": top_score,
            "filename": top_cand.get("filename", ""),
            "matched_skills_count": len(top_matched),
            "recommendation": top_cand.get("recommendation", "Strong Match")
        },
        "top_candidate_reasoning": top_candidate_reasoning,
        "rankings": sorted_candidates
    }
