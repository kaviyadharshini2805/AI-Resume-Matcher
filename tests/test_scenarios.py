import pytest
import os
import io
from backend.parser.resume_parser import (
    parse_resume_text,
    parse_resume_file,
    extract_experience,
    extract_education,
    extract_skills
)
from backend.matching.matcher import (
    match_resume_to_job,
    rank_candidates,
    extract_jd_experience_requirement
)

RESUMES_DIR = os.path.join(os.path.dirname(__file__), "..", "sample_data", "resumes")
JDS_DIR = os.path.join(os.path.dirname(__file__), "..", "sample_data", "job_descriptions")

def load_file(folder, filename):
    with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
        return f.read()

def test_scenario_a_strong_match():
    """Scenario A: Strong match candidate has most mandatory skills, relevant experience, relevant degree."""
    resume = load_file(RESUMES_DIR, "02_alex_johnson_senior_backend.txt")
    jd = load_file(JDS_DIR, "jd_senior_python_backend.txt")
    result = match_resume_to_job(resume, jd)
    
    assert result["overall_score"] >= 80.0
    assert result["recommendation"] == "Strong Match"
    assert "fastapi" in result["matched_skills"]
    assert "docker" in result["matched_skills"]
    assert "postgresql" in result["matched_skills"]

def test_scenario_b_partial_match():
    """Scenario B: Partial match candidate has some skills but lacks several critical requirements."""
    resume = load_file(RESUMES_DIR, "04_rahul_verma_partial_backend.txt")
    jd = load_file(JDS_DIR, "jd_senior_python_backend.txt")
    result = match_resume_to_job(resume, jd)
    
    assert 40.0 <= result["overall_score"] < 80.0
    assert result["recommendation"] in ["Moderate Match", "Potential Match"]
    assert "fastapi" in result["missing_skills"]
    assert "docker" in result["missing_skills"]

def test_scenario_c_weak_match():
    """Scenario C: Weak match candidate has unrelated experience and skills."""
    resume = load_file(RESUMES_DIR, "05_emily_clark_weak_frontend.txt")
    jd = load_file(JDS_DIR, "jd_lead_nlp_scientist.txt")
    result = match_resume_to_job(resume, jd)
    
    assert result["overall_score"] < 50.0
    assert result["recommendation"] in ["Low Match", "Potential Match"]
    assert "pytorch" in result["missing_skills"]
    assert "deep learning" in result["missing_skills"]

def test_scenario_d_experience_mismatch():
    """Scenario D: Fresher applying for a lead/senior position requiring 5+ years."""
    resume = load_file(RESUMES_DIR, "06_david_kim_fresher_mismatch.txt")
    jd = load_file(JDS_DIR, "jd_lead_nlp_scientist.txt")
    result = match_resume_to_job(resume, jd)
    
    exp_status = result["experience_comparison"]["status"]
    assert "Below" in exp_status or "Mismatch" in exp_status
    assert result["experience_score"] < 60.0

def test_scenario_e_education_mismatch():
    """Scenario E: Candidate does not meet required educational qualification (bootcamp vs Ph.D.)."""
    resume = load_file(RESUMES_DIR, "07_sarah_connor_education_mismatch.txt")
    jd = load_file(JDS_DIR, "jd_lead_nlp_scientist.txt")
    result = match_resume_to_job(resume, jd)
    
    edu_analysis = result["education_analysis"]
    assert edu_analysis["has_phd"] is False
    assert edu_analysis["has_masters"] is False
    assert edu_analysis["score"] <= 50.0

def test_scenario_f_semantic_related_matching():
    """Scenario F: Alternative terminology / related skills identified separately without converting to exact matches."""
    resume = load_file(RESUMES_DIR, "08_vikram_singh_semantic_related.txt")
    jd = load_file(JDS_DIR, "jd_senior_python_backend.txt")
    result = match_resume_to_job(resume, jd)
    
    # Candidate has Flask, JD requires FastAPI
    assert "fastapi" in result["missing_skills"]
    assert "fastapi" not in result["matched_skills"]
    # Check related skills dictionary captures the connection
    assert "related_skills" in result
    assert "fastapi" in result["related_skills"]
    assert "flask" in result["related_skills"]["fastapi"]

def test_scenario_g_missing_information():
    """Scenario G: Resume missing email, phone, and employment dates."""
    resume = load_file(RESUMES_DIR, "09_anonymized_missing_info.txt")
    parsed = parse_resume_text(resume)
    
    assert parsed["email"] == "Not specified in resume"
    assert parsed["phone"] == "Not specified in resume"
    assert len(parsed["missing_fields"]) > 0
    assert parsed["needs_manual_review"] is True

def test_scenario_h_multiple_resumes_batch_ranking():
    """Scenario H: Upload & evaluate 10+ resumes simultaneously; verify ranking and selection reasoning."""
    jd = load_file(JDS_DIR, "jd_ai_ml_engineer.txt")
    txt_files = sorted([f for f in os.listdir(RESUMES_DIR) if f.startswith(("0", "1")) and f.endswith(".txt")])
    assert len(txt_files) >= 10
    
    candidate_matches = []
    for fn in txt_files:
        content = load_file(RESUMES_DIR, fn)
        res = match_resume_to_job(content, jd)
        res["filename"] = fn
        candidate_matches.append(res)
        
    ranking = rank_candidates(candidate_matches, "AI/ML Engineer")
    
    assert ranking["total_ranked"] >= 10
    assert len(ranking["rankings"]) >= 10
    assert ranking["top_candidate"] is not None
    assert "Arjun Kumar" in ranking["top_candidate"]["name"] or ranking["top_candidate"]["score"] >= 80.0
    assert len(ranking["top_candidate_reasoning"]) > 50
    # Check ranks are ordered 1 to N
    ranks = [c["rank"] for c in ranking["rankings"]]
    assert ranks == list(range(1, len(ranks) + 1))
    # Check scores are descending
    scores = [c["overall_score"] for c in ranking["rankings"]]
    assert scores == sorted(scores, reverse=True)

def test_scenario_i_duplicate_resume():
    """Scenario I: Uploading duplicate resume produces identical and consistent scoring."""
    resume = load_file(RESUMES_DIR, "01_arjun_kumar_ai_ml_intern.txt")
    jd = load_file(JDS_DIR, "jd_ai_ml_engineer.txt")
    
    run1 = match_resume_to_job(resume, jd)
    run2 = match_resume_to_job(resume, jd)
    
    assert run1["overall_score"] == run2["overall_score"]
    assert run1["matched_skills"] == run2["matched_skills"]
    assert run1["missing_skills"] == run2["missing_skills"]

def test_scenario_j_invalid_files():
    """Scenario J: Invalid, empty, or unsupported files handled gracefully without crashing."""
    # Empty bytes
    empty_parsed = parse_resume_file(b"", "empty.pdf")
    assert empty_parsed["candidate_name"] == "Candidate"
    
    # Non-text binary
    corrupted_parsed = parse_resume_file(b"\x00\x01\x02\x03\xff", "corrupted.docx")
    assert "candidate_name" in corrupted_parsed
    
    # Unsupported extension falls back gracefully
    txt_fallback = parse_resume_file(b"Python developer", "unknown.xyz")
    assert "python" in txt_fallback["skills"]

def test_scenario_k_no_false_experience():
    """Scenario K: 3-month internship with 4-year degree yields 3 months internship, NOT 4 years experience."""
    resume = load_file(RESUMES_DIR, "01_arjun_kumar_ai_ml_intern.txt")
    exp = extract_experience(resume)
    
    assert exp["is_internship_only"] is True
    assert exp["internship_months"] == 3
    assert exp["professional_years"] == 0.0
    assert "4 years" not in exp["display"]

def test_scenario_l_no_false_qualifications():
    """Scenario L: Resume with only a bachelor's degree must never display a master's degree."""
    resume = load_file(RESUMES_DIR, "01_arjun_kumar_ai_ml_intern.txt")
    edu = extract_education(resume)
    
    assert edu["has_bachelors"] is True
    assert edu["has_masters"] is False
    assert edu["has_phd"] is False
    assert "Master" not in " ".join(edu["degrees"])
