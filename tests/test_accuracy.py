import pytest
import os
from backend.parser.resume_parser import (
    parse_resume_text,
    extract_experience,
    extract_education,
    extract_skills_with_evidence
)
from backend.matching.matcher import (
    match_resume_to_job,
    extract_jd_experience_requirement,
    extract_jd_skills
)

@pytest.fixture
def synthetic_resume():
    path = os.path.join(os.path.dirname(__file__), "..", "sample_data", "resumes", "synthetic_candidate.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@pytest.fixture
def synthetic_jd():
    path = os.path.join(os.path.dirname(__file__), "..", "sample_data", "synthetic_job_description.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def test_experience_extraction_accuracy(synthetic_resume):
    """Verify:
    - Experience = 3 months internship, not 4 years.
    - Does not claim 3+ years of professional experience.
    - Does not infer 4 years of experience from a bachelor's degree duration (2022-2026).
    """
    exp = extract_experience(synthetic_resume)
    
    assert exp["internship_months"] == 3
    assert exp["professional_years"] == 0.0
    assert exp["is_internship_only"] is True
    assert "3 months" in exp["display"]
    assert "4 years" not in exp["display"]
    assert "3+ years" not in exp["display"]

def test_job_description_experience_extraction(synthetic_jd):
    """Verify:
    - JD experience requirement = 0-2 years.
    - Handles entry-level / fresher phrasing.
    - Does not invent or replace the JD requirement with 3+ years.
    """
    jd_req = extract_jd_experience_requirement(synthetic_jd)
    
    assert jd_req["min_years"] == 0.0
    assert jd_req["max_years"] == 2.0
    assert "0–2 years" in jd_req["display"] or "0-2 years" in jd_req["display"]
    assert "3+" not in jd_req["display"]

def test_education_extraction_accuracy(synthetic_resume):
    """Verify:
    - Education = B.E. Computer Science only.
    - Candidate has CGPA 8.2 and years 2022-2026.
    - Does not generate a Master's degree or any other qualification that does not exist.
    """
    edu = extract_education(synthetic_resume)
    
    assert edu["has_masters"] is False
    assert edu["has_phd"] is False
    assert edu["has_bachelors"] is True
    assert any("B.E." in d for d in edu["degrees"])
    assert "Master" not in " ".join(edu["degrees"])
    assert edu["cgpa"] == "8.2"

def test_evidence_based_matching(synthetic_resume, synthetic_jd):
    """Verify:
    - Flask is matched.
    - FastAPI is missing (not marked matched just because Flask is present).
    - TensorFlow is matched.
    - PyTorch is missing (not marked matched just because TensorFlow is present).
    - AWS and Azure are missing.
    - RAG is missing.
    - Required and preferred skills are kept separate.
    """
    result = match_resume_to_job(synthetic_resume, synthetic_jd)
    
    matched = result["matched_skills"]
    missing_req = result["missing_required_skills"]
    
    # 1. Flask is matched
    assert "flask" in matched
    
    # 2. FastAPI is missing
    assert "fastapi" in missing_req
    assert "fastapi" not in matched
    
    # 3. TensorFlow is matched
    assert "tensorflow" in matched
    
    # 4. PyTorch is missing
    assert "pytorch" in missing_req
    assert "pytorch" not in matched
    
    # 5. AWS and Azure are missing
    assert "aws" in missing_req
    assert "azure" in missing_req
    assert "aws" not in matched
    assert "azure" not in matched
    
    # 6. RAG is missing
    assert "rag" in missing_req
    assert "rag" not in matched
    
    # 7. Check evidence support for matched skills
    for item in result["matched_skills_with_evidence"]:
        assert len(item["evidence"]) > 0
        assert item["skill"] in item["evidence"].lower()

def test_ai_explanations_grounded(synthetic_resume, synthetic_jd):
    """Verify:
    - No unsupported qualifications or experience appear in generated explanation.
    - Suggestions do not tell candidates to falsely claim skills.
    - Accurately references 3 months internship and 0-2 years JD expectation.
    """
    result = match_resume_to_job(synthetic_resume, synthetic_jd)
    
    exp_details = result["experience_comparison"]["details"]
    edu_details = result["education_analysis"]["details"]
    
    # Must mention 3 months internship
    assert "3 months" in exp_details or "internship" in exp_details
    assert "4 years" not in exp_details
    assert "3+ years" not in exp_details
    
    # Must NOT claim Master's degree
    assert "Master's" not in edu_details or "No Master's degree" in edu_details
    assert result["education_analysis"]["has_masters"] is False
    
    # Suggestions must be constructive (gain experience / project exposure)
    for sug in result["suggestions"]:
        assert "falsely" not in sug.lower()
        assert "claim skills you do not have" not in sug.lower()
