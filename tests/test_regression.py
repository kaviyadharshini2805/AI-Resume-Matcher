import pytest
import os
from backend.parser.resume_parser import (
    parse_resume_text,
    extract_experience,
    extract_education,
    extract_skills
)
from backend.matching.matcher import (
    match_resume_to_job,
    extract_jd_experience_requirement,
    extract_jd_skills
)

@pytest.fixture
def arjun_resume():
    path = os.path.join(os.path.dirname(__file__), "..", "sample_data", "resumes", "01_arjun_kumar_ai_ml_intern.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@pytest.fixture
def aiml_jd():
    path = os.path.join(os.path.dirname(__file__), "..", "sample_data", "job_descriptions", "jd_ai_ml_engineer.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def test_phase11_arjun_kumar_regression(arjun_resume, aiml_jd):
    """PHASE 11 REGRESSION TEST:
    Verify exact extraction and matching behavior for Arjun Kumar against AI/ML Engineer JD.
    """
    parsed = parse_resume_text(arjun_resume)
    exp = parsed["experience"]
    edu = parsed["education_details"]
    
    # 1. Candidate Name: Arjun Kumar
    assert parsed["candidate_name"] == "Arjun Kumar"
    
    # 2. Education: B.E. in Computer Science, CGPA 8.2
    assert edu["has_bachelors"] is True
    assert edu["has_masters"] is False
    assert any("B.E." in d for d in edu["degrees"])
    assert edu["cgpa"] == "8.2"
    
    # 3. Internship: January–March 2026, approx 3 months
    assert exp["is_internship_only"] is True
    assert exp["internship_months"] == 3
    assert exp["professional_years"] == 0.0
    assert "3 months" in exp["display"]
    
    # 4. JD Experience Requirement: 0–2 years
    jd_req = extract_jd_experience_requirement(aiml_jd)
    assert jd_req["min_years"] == 0.0
    assert jd_req["max_years"] == 2.0
    assert "0–2 years" in jd_req["display"] or "0-2 years" in jd_req["display"]
    
    # 5. Matching Assertions
    match = match_resume_to_job(arjun_resume, aiml_jd)
    matched_skills = match["matched_skills"]
    missing_req = match["missing_required_skills"]
    missing_pref = match["missing_preferred_skills"]
    missing_all = match["missing_skills"]
    additional = match["candidate_additional_skills"]
    
    # Flask: Matched
    assert "flask" in matched_skills
    
    # FastAPI: Missing (not marked matched just because Flask is present!)
    assert "fastapi" in missing_all
    assert "fastapi" not in matched_skills
    
    # TensorFlow: Matched
    assert "tensorflow" in matched_skills
    
    # PyTorch: Missing (not marked matched just because TensorFlow is present!)
    assert "pytorch" in missing_all
    assert "pytorch" not in matched_skills
    
    # NLP: Matched
    assert "nlp" in matched_skills
    
    # RAG: Missing
    assert "rag" in missing_all
    assert "rag" not in matched_skills
    
    # AWS: Missing
    assert "aws" in missing_all
    assert "aws" not in matched_skills
    
    # Azure: Missing
    assert "azure" in missing_all
    assert "azure" not in matched_skills
    
    # Java and PostgreSQL: Additional skills
    assert "java" in additional
    assert "postgresql" in additional
    
    # Component breakdown present and normalized
    assert "score_breakdown" in match
    breakdown = match["score_breakdown"]
    assert "skills_match" in breakdown
    assert "semantic_similarity" in breakdown
    assert "experience" in breakdown
    assert "education" in breakdown
    assert "projects_evidence" in breakdown
    
    # Verify overall score calculation matches formula
    calc_score = round(
        (breakdown["skills_match"]["score"] * 0.35) +
        (breakdown["semantic_similarity"]["score"] * 0.25) +
        (breakdown["experience"]["score"] * 0.20) +
        (breakdown["education"]["score"] * 0.10) +
        (breakdown["projects_evidence"]["score"] * 0.10),
        1
    )
    assert abs(match["overall_score"] - calc_score) <= 0.2
