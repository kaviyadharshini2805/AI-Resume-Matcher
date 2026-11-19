import sqlite3
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from .models import ResumeRecord, MatchResultRecord

DB_PATH = os.path.join(os.path.dirname(__file__), "resume_matcher.db")

class SQLiteDatabase:
    """Persistent local SQLite database for candidate profiles, job descriptions, and evaluation history."""
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_tables()
        self._seed_sample_history()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_tables(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Resumes Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS resumes (
                    id TEXT PRIMARY KEY,
                    candidate_name TEXT NOT NULL,
                    filename TEXT NOT NULL,
                    parsed_skills TEXT,
                    categorized_skills TEXT,
                    email TEXT,
                    phone TEXT,
                    location TEXT,
                    education TEXT,
                    education_details TEXT,
                    experience_display TEXT,
                    experience_years REAL,
                    projects TEXT,
                    certifications TEXT,
                    raw_text TEXT,
                    needs_manual_review INTEGER,
                    missing_fields TEXT,
                    created_at TEXT
                )
            """)

            # Matches History Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS matches (
                    id TEXT PRIMARY KEY,
                    candidate_name TEXT NOT NULL,
                    job_title TEXT NOT NULL,
                    filename TEXT,
                    overall_score REAL NOT NULL,
                    cosine_similarity REAL NOT NULL,
                    skill_match_score REAL NOT NULL,
                    experience_score REAL,
                    education_score REAL,
                    projects_score REAL,
                    score_breakdown TEXT,
                    ai_score_explanation TEXT,
                    matched_skills TEXT,
                    missing_skills TEXT,
                    matched_required_skills TEXT,
                    missing_required_skills TEXT,
                    matched_preferred_skills TEXT,
                    missing_preferred_skills TEXT,
                    matched_skills_with_evidence TEXT,
                    candidate_additional_skills TEXT,
                    related_skills TEXT,
                    recommendation TEXT NOT NULL,
                    experience_comparison TEXT,
                    education_analysis TEXT,
                    projects_analysis TEXT,
                    suggestions TEXT,
                    rank INTEGER,
                    created_at TEXT
                )
            """)
            
            # Job Descriptions Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS job_descriptions (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    required_skills TEXT,
                    preferred_skills TEXT,
                    experience_requirement TEXT,
                    created_at TEXT
                )
            """)
            conn.commit()

    def _seed_sample_history(self):
        """Seed baseline demonstration candidate evaluations if table is newly initialized."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as cnt FROM matches")
            row = cursor.fetchone()
            if row and row["cnt"] > 0:
                return  # Already seeded or has data
                
            samples = [
                MatchResultRecord(
                    id="rec-1",
                    candidate_name="Alex Johnson",
                    job_title="Senior Python Backend Engineer",
                    filename="02_alex_johnson_senior_backend.pdf",
                    overall_score=92.5,
                    cosine_similarity=38.4,
                    skill_match_score=100.0,
                    experience_score=100.0,
                    education_score=100.0,
                    projects_score=85.0,
                    score_breakdown={
                        "skills_match": {"score": 100.0, "weight": 0.35, "weighted_score": 35.0, "label": "Technical Skills Match"},
                        "semantic_similarity": {"score": 90.0, "weight": 0.25, "weighted_score": 22.5, "label": "Semantic Similarity"},
                        "experience": {"score": 100.0, "weight": 0.20, "weighted_score": 20.0, "label": "Relevant Experience"},
                        "education": {"score": 100.0, "weight": 0.10, "weighted_score": 10.0, "label": "Academic Qualifications"},
                        "projects_evidence": {"score": 85.0, "weight": 0.10, "weighted_score": 8.5, "label": "Project Portfolio"}
                    },
                    ai_score_explanation="Strong match with 5+ years of verified backend microservices experience on AWS and Docker.",
                    matched_skills=["python", "fastapi", "docker", "kubernetes", "postgresql", "redis", "aws", "git"],
                    missing_skills=[],
                    matched_required_skills=["python", "fastapi", "docker", "kubernetes", "postgresql", "redis", "git"],
                    missing_required_skills=[],
                    matched_preferred_skills=["aws", "ci/cd", "linux"],
                    missing_preferred_skills=[],
                    candidate_additional_skills=["golang", "django"],
                    recommendation="Strong Match",
                    experience_comparison={
                        "candidate_experience": "5.8 years professional experience",
                        "candidate_years": 5.8,
                        "required_experience": "4+ years",
                        "status": "Meets or Exceeds Requirement",
                        "details": "Candidate brings 5+ years of production experience exceeding role requirement."
                    },
                    education_analysis={
                        "candidate_degrees": ["B.S. in Computer Science"],
                        "candidate_highest_level": "Bachelor's Degree",
                        "education_details": "B.S. in Computer Science (2015–2019) UC Berkeley",
                        "status": "Qualified",
                        "details": "Holds Bachelor's in CS fulfilling requirement."
                    },
                    projects_analysis={"status": "Verified", "projects_count": 2},
                    suggestions=[
                        "Highlight distributed caching architectures implemented with Redis.",
                        "Structure recent work achievements with quantified latency reduction metrics."
                    ],
                    rank=1,
                    created_at="May 14, 2026"
                ),
                MatchResultRecord(
                    id="rec-2",
                    candidate_name="Dr. Priya Sharma",
                    job_title="Lead AI & NLP Scientist",
                    filename="03_priya_sharma_nlp_scientist.docx",
                    overall_score=94.0,
                    cosine_similarity=42.1,
                    skill_match_score=95.0,
                    experience_score=100.0,
                    education_score=100.0,
                    projects_score=90.0,
                    score_breakdown={
                        "skills_match": {"score": 95.0, "weight": 0.35, "weighted_score": 33.25, "label": "Technical Skills Match"},
                        "semantic_similarity": {"score": 95.0, "weight": 0.25, "weighted_score": 23.75, "label": "Semantic Similarity"},
                        "experience": {"score": 100.0, "weight": 0.20, "weighted_score": 20.0, "label": "Relevant Experience"},
                        "education": {"score": 100.0, "weight": 0.10, "weighted_score": 10.0, "label": "Academic Qualifications"},
                        "projects_evidence": {"score": 90.0, "weight": 0.10, "weighted_score": 9.0, "label": "Project Portfolio"}
                    },
                    ai_score_explanation="Candidate holds Ph.D. from MIT with 6+ years of specialized AI/NLP research and transformer model fine-tuning.",
                    matched_skills=["python", "nlp", "pytorch", "transformers", "deep learning", "machine learning", "aws"],
                    missing_skills=["sql"],
                    matched_required_skills=["python", "nlp", "pytorch", "transformers", "deep learning", "machine learning"],
                    missing_required_skills=[],
                    matched_preferred_skills=["aws", "docker"],
                    missing_preferred_skills=["sql"],
                    candidate_additional_skills=["pandas", "numpy", "c++"],
                    recommendation="Strong Match",
                    experience_comparison={
                        "candidate_experience": "6 years professional experience",
                        "candidate_years": 6.0,
                        "required_experience": "Minimum 5 years",
                        "status": "Meets or Exceeds Requirement",
                        "details": "Candidate brings 6 years of specialized AI research and engineering."
                    },
                    education_analysis={
                        "candidate_degrees": ["Ph.D. in Computer Science"],
                        "candidate_highest_level": "Ph.D. / Doctorate",
                        "education_details": "Ph.D. in Computer Science (AI & NLP) MIT (2014–2018)",
                        "status": "Qualified (Advanced Degree)",
                        "details": "Holds Ph.D. in NLP from MIT."
                    },
                    projects_analysis={"status": "Strong Evidence", "projects_count": 3},
                    suggestions=[
                        "Mention database querying experience (SQL) in large-scale model inference pipelines."
                    ],
                    rank=1,
                    created_at="May 12, 2026"
                ),
                MatchResultRecord(
                    id="rec-3",
                    candidate_name="Arjun Kumar",
                    job_title="AI/ML Engineer",
                    filename="01_arjun_kumar_ai_ml_intern.pdf",
                    overall_score=85.9,
                    cosine_similarity=34.2,
                    skill_match_score=92.0,
                    experience_score=100.0,
                    education_score=100.0,
                    projects_score=95.0,
                    score_breakdown={
                        "skills_match": {"score": 92.0, "weight": 0.35, "weighted_score": 32.2, "label": "Technical Skills Match"},
                        "semantic_similarity": {"score": 85.0, "weight": 0.25, "weighted_score": 21.25, "label": "Semantic Similarity"},
                        "experience": {"score": 100.0, "weight": 0.20, "weighted_score": 20.0, "label": "Relevant Experience"},
                        "education": {"score": 100.0, "weight": 0.10, "weighted_score": 10.0, "label": "Academic Qualifications"},
                        "projects_evidence": {"score": 95.0, "weight": 0.10, "weighted_score": 9.5, "label": "Project Portfolio"}
                    },
                    ai_score_explanation="Strong entry-level match: B.E. CS (CGPA 8.2), 3-month ML internship satisfying 0–2 years requirement, and 3 verified projects.",
                    matched_skills=["python", "machine learning", "pandas", "numpy", "scikit-learn", "eda", "data preprocessing", "model evaluation", "sql", "flask", "tensorflow", "nlp", "llm", "git"],
                    missing_skills=["fastapi", "rag", "pytorch", "aws", "azure"],
                    matched_required_skills=["python", "machine learning", "pandas", "numpy", "scikit-learn", "eda", "data preprocessing", "model evaluation", "sql"],
                    missing_required_skills=[],
                    matched_preferred_skills=["flask", "tensorflow", "nlp", "llm", "git"],
                    missing_preferred_skills=["fastapi", "rag", "pytorch", "aws", "azure"],
                    candidate_additional_skills=["java", "postgresql"],
                    recommendation="Strong Match",
                    experience_comparison={
                        "candidate_experience": "3 months internship (January 2026 – March 2026)",
                        "candidate_years": 0.25,
                        "required_experience": "0–2 years",
                        "status": "Meets Requirement (0–2 years)",
                        "details": "Candidate has 3 months internship, satisfying the 0–2 years entry-level requirement."
                    },
                    education_analysis={
                        "candidate_degrees": ["B.E. in Computer Science"],
                        "candidate_highest_level": "Bachelor's Degree",
                        "education_details": "B.E. in Computer Science (2022–2026) CGPA 8.2",
                        "status": "Qualified",
                        "details": "Holds B.E. in Computer Science (CGPA 8.2)."
                    },
                    projects_analysis={"status": "Strong Project Evidence", "projects_count": 3},
                    suggestions=[
                        "Gain practical project exposure in cloud platforms (AWS or Azure).",
                        "Explore Retrieval-Augmented Generation (RAG) frameworks like LangChain."
                    ],
                    rank=1,
                    created_at="May 10, 2026"
                )
            ]
            for s in samples:
                self.save_match(s)

    def check_connection(self) -> Dict[str, Any]:
        """Verify database connectivity with a live test query."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                row = cursor.fetchone()
                
                cursor.execute("SELECT COUNT(*) as total FROM matches")
                total_m = cursor.fetchone()["total"]
                
                cursor.execute("SELECT COUNT(*) as total FROM resumes")
                total_r = cursor.fetchone()["total"]
                
                return {
                    "connected": True,
                    "engine": "SQLite (Local Persistent Storage)",
                    "database_path": self.db_path,
                    "tables": ["resumes", "matches", "job_descriptions"],
                    "total_evaluations_stored": total_m,
                    "total_resumes_stored": total_r,
                    "status": "healthy"
                }
        except Exception as e:
            return {
                "connected": False,
                "engine": "SQLite",
                "error": str(e),
                "status": "unhealthy"
            }

    def save_resume(self, resume: ResumeRecord) -> ResumeRecord:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO resumes (
                    id, candidate_name, filename, parsed_skills, categorized_skills,
                    email, phone, location, education, education_details,
                    experience_display, experience_years, projects, certifications,
                    raw_text, needs_manual_review, missing_fields, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                resume.id,
                resume.candidate_name,
                resume.filename,
                json.dumps(resume.parsed_skills),
                json.dumps(resume.categorized_skills),
                resume.email,
                resume.phone,
                resume.location,
                json.dumps(resume.education),
                json.dumps(resume.education_details),
                resume.experience_display,
                resume.experience_years,
                json.dumps(resume.projects),
                json.dumps(resume.certifications),
                resume.raw_text,
                1 if resume.needs_manual_review else 0,
                json.dumps(resume.missing_fields),
                resume.created_at.isoformat() if isinstance(resume.created_at, datetime) else str(resume.created_at)
            ))
            conn.commit()
        return resume

    def get_resume(self, resume_id: str) -> Optional[ResumeRecord]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM resumes WHERE id = ?", (resume_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return ResumeRecord(
                id=row["id"],
                candidate_name=row["candidate_name"],
                filename=row["filename"],
                parsed_skills=json.loads(row["parsed_skills"] or "[]"),
                categorized_skills=json.loads(row["categorized_skills"] or "{}"),
                email=row["email"],
                phone=row["phone"],
                location=row["location"],
                education=json.loads(row["education"] or "[]"),
                education_details=json.loads(row["education_details"] or "{}"),
                experience_display=row["experience_display"],
                experience_years=row["experience_years"] or 0.0,
                projects=json.loads(row["projects"] or "[]"),
                certifications=json.loads(row["certifications"] or "[]"),
                raw_text=row["raw_text"] or "",
                needs_manual_review=bool(row["needs_manual_review"]),
                missing_fields=json.loads(row["missing_fields"] or "[]")
            )

    def list_resumes(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, candidate_name, filename, email, phone, location, experience_display, created_at FROM resumes ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def save_match(self, match: MatchResultRecord) -> MatchResultRecord:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO matches (
                    id, candidate_name, job_title, filename, overall_score,
                    cosine_similarity, skill_match_score, experience_score,
                    education_score, projects_score, score_breakdown,
                    ai_score_explanation, matched_skills, missing_skills,
                    matched_required_skills, missing_required_skills,
                    matched_preferred_skills, missing_preferred_skills,
                    matched_skills_with_evidence, candidate_additional_skills,
                    related_skills, recommendation, experience_comparison,
                    education_analysis, projects_analysis, suggestions,
                    rank, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                match.id,
                match.candidate_name,
                match.job_title,
                match.filename,
                match.overall_score,
                match.cosine_similarity,
                match.skill_match_score,
                match.experience_score,
                match.education_score,
                match.projects_score,
                json.dumps(match.score_breakdown),
                match.ai_score_explanation,
                json.dumps(match.matched_skills),
                json.dumps(match.missing_skills),
                json.dumps(match.matched_required_skills),
                json.dumps(match.missing_required_skills),
                json.dumps(match.matched_preferred_skills),
                json.dumps(match.missing_preferred_skills),
                json.dumps(match.matched_skills_with_evidence),
                json.dumps(match.candidate_additional_skills),
                json.dumps(match.related_skills),
                match.recommendation,
                json.dumps(match.experience_comparison),
                json.dumps(match.education_analysis),
                json.dumps(match.projects_analysis),
                json.dumps(match.suggestions),
                match.rank,
                match.created_at
            ))
            conn.commit()
        return match

    def list_matches(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM matches ORDER BY ROWID DESC")
            rows = cursor.fetchall()
            results = []
            for r in rows:
                item = dict(r)
                # Parse JSON fields
                for f in [
                    "score_breakdown", "matched_skills", "missing_skills",
                    "matched_required_skills", "missing_required_skills",
                    "matched_preferred_skills", "missing_preferred_skills",
                    "matched_skills_with_evidence", "candidate_additional_skills",
                    "related_skills", "experience_comparison", "education_analysis",
                    "projects_analysis", "suggestions"
                ]:
                    if item.get(f):
                        try:
                            item[f] = json.loads(item[f])
                        except Exception:
                            pass
                results.append(item)
            return results

    def get_match(self, match_id: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM matches WHERE id = ?", (match_id,))
            row = cursor.fetchone()
            if not row:
                return None
            item = dict(row)
            for f in [
                "score_breakdown", "matched_skills", "missing_skills",
                "matched_required_skills", "missing_required_skills",
                "matched_preferred_skills", "missing_preferred_skills",
                "matched_skills_with_evidence", "candidate_additional_skills",
                "related_skills", "experience_comparison", "education_analysis",
                "projects_analysis", "suggestions"
            ]:
                if item.get(f):
                    try:
                        item[f] = json.loads(item[f])
                    except Exception:
                        pass
            return item

    def delete_match(self, match_id: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM matches WHERE id = ?", (match_id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_stats(self) -> Dict[str, Any]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as total, AVG(overall_score) as avg_score FROM matches")
            row = cursor.fetchone()
            total = row["total"] if row else 0
            avg_score = round(row["avg_score"], 1) if (row and row["avg_score"] is not None) else 0.0
            
            cursor.execute("SELECT COUNT(*) as strong FROM matches WHERE overall_score >= 80")
            strong = cursor.fetchone()["strong"]
            
            return {
                "total_analyzed": total,
                "avg_score": avg_score,
                "strong_matches": strong,
                "completed": total,
                "db_engine": "SQLite"
            }

# Global database instance
db_instance = SQLiteDatabase()
db_store = db_instance

def get_db() -> SQLiteDatabase:
    return db_instance
