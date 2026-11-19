import io
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"]["connected"] is True

def test_db_status_api():
    response = client.get("/api/db-status")
    assert response.status_code == 200
    data = response.json()
    assert data["connected"] is True
    assert "SQLite" in data["engine"]

def test_parse_text_api():
    payload = {"text": "Developer proficient in Python and React. Contact: dev@code.com"}
    response = client.post("/api/parse-text", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "dev@code.com"
    assert "python" in data["skills"]
    assert "react" in data["skills"]

def test_match_api():
    payload = {
        "resume_text": "Experienced Python, FastAPI, and Docker developer. 4 years experience.",
        "job_description": "Seeking Python engineer with Docker experience. 3+ years required."
    }
    response = client.post("/api/match", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "overall_score" in data
    assert "matched_skills" in data
    assert "score_breakdown" in data
    assert data["overall_score"] > 0

def test_upload_resume_api():
    file_content = b"Candidate Name: Jane Doe\nEmail: jane@test.com\nSkills: Python, FastAPI\nExperience: 2021-2024 (3 years)"
    files = {"file": ("jane_resume.txt", io.BytesIO(file_content), "text/plain")}
    response = client.post("/api/upload-resume", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "jane@test.com"
    assert "python" in data["skills"]

def test_upload_batch_api():
    files = [
        ("files", ("c1.txt", io.BytesIO(b"Candidate 1\nEmail: c1@test.com\nSkills: Python"), "text/plain")),
        ("files", ("c2.txt", io.BytesIO(b"Candidate 2\nEmail: c2@test.com\nSkills: React"), "text/plain")),
    ]
    response = client.post("/api/upload-batch", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["total_uploaded"] == 2
    assert data["successful_count"] == 2

def test_match_batch_api():
    payload = {
        "candidates": [
            {"name": "Alice Strong", "filename": "alice.pdf", "text": "Alice Strong\nSkills: Python, FastAPI, Docker, SQL\nExperience: 5 years (2021-Present)"},
            {"name": "Bob Junior", "filename": "bob.pdf", "text": "Bob Junior\nSkills: Python\nExperience: 3 months internship"},
            {"name": "Charlie Weak", "filename": "charlie.pdf", "text": "Charlie Weak\nSkills: HTML, CSS"}
        ],
        "job_description": "Seeking Senior Python Backend Engineer with FastAPI, Docker, and SQL experience. 4+ years required.",
        "job_title": "Senior Python Backend Engineer"
    }
    response = client.post("/api/match-batch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total_ranked"] == 3
    assert len(data["rankings"]) == 3
    # Alice should be ranked #1
    assert data["rankings"][0]["rank"] == 1
    assert data["rankings"][0]["candidate_name"] == "Alice Strong"
    assert data["top_candidate"]["name"] == "Alice Strong"
    assert len(data["top_candidate_reasoning"]) > 50

def test_stats_and_history_api():
    stats_res = client.get("/api/stats")
    assert stats_res.status_code == 200
    stats = stats_res.json()
    assert "total_analyzed" in stats
    assert "avg_score" in stats

    hist_res = client.get("/api/history")
    assert hist_res.status_code == 200
    history = hist_res.json()
    assert isinstance(history, list)
    if history:
        item_id = history[0]["id"]
        single_res = client.get(f"/api/history/{item_id}")
        assert single_res.status_code == 200
        assert single_res.json()["id"] == item_id
