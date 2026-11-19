from backend.parser.resume_parser import parse_resume_text, extract_skills, extract_email

def test_extract_email():
    text = "Candidate Name. Reach me at john.doe@techcorp.com or call me."
    assert extract_email(text) == "john.doe@techcorp.com"

def test_extract_skills():
    text = "Experienced in Python, FastAPI, Docker, and PostgreSQL databases."
    skills = extract_skills(text)
    assert "python" in skills
    assert "fastapi" in skills
    assert "docker" in skills
    assert "postgresql" in skills

def test_parse_resume_text():
    sample = """
    Jane Doe
    jane.doe@example.org
    (555) 321-4567
    Skilled in React, TypeScript, and AWS.
    """
    parsed = parse_resume_text(sample)
    assert parsed["email"] == "jane.doe@example.org"
    assert "react" in parsed["skills"]
    assert "typescript" in parsed["skills"]
    assert "aws" in parsed["skills"]
