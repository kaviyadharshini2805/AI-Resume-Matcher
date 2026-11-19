from backend.matching.matcher import match_resume_to_job, calculate_similarity

def test_calculate_similarity():
    text1 = "Senior Python engineer building FastAPI microservices and Docker containers."
    text2 = "Looking for a Python developer with FastAPI and Docker experience."
    score = calculate_similarity(text1, text2)
    assert score > 0.2

def test_match_resume_to_job():
    resume = "Expert in Python, Docker, PostgreSQL, and AWS with 5 years experience."
    job = "We need a Python engineer with Docker and AWS skills."
    result = match_resume_to_job(resume, job)
    
    assert result["overall_score"] > 50
    assert "python" in result["matched_skills"]
    assert "docker" in result["matched_skills"]
    assert "aws" in result["matched_skills"]
    assert len(result["missing_skills"]) == 0
