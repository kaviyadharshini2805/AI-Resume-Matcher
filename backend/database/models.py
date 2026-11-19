from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

class ResumeRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    candidate_name: str = "Candidate"
    filename: str
    parsed_skills: List[str] = []
    categorized_skills: Dict[str, List[str]] = {}
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    education: List[str] = []
    education_details: Dict[str, Any] = {}
    experience_display: Optional[str] = None
    experience_years: float = 0.0
    projects: List[Dict[str, Any]] = []
    certifications: List[str] = []
    raw_text: str
    needs_manual_review: bool = False
    missing_fields: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

class JobDescriptionRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    experience_requirement: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MatchResultRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    candidate_name: str = "Candidate"
    job_title: str = "Target Position"
    filename: Optional[str] = None
    overall_score: float
    cosine_similarity: float
    skill_match_score: float
    experience_score: float = 0.0
    education_score: float = 0.0
    projects_score: float = 0.0
    score_breakdown: Dict[str, Any] = {}
    ai_score_explanation: Optional[str] = None
    matched_skills: List[str] = []
    missing_skills: List[str] = []
    matched_required_skills: List[str] = []
    missing_required_skills: List[str] = []
    matched_preferred_skills: List[str] = []
    missing_preferred_skills: List[str] = []
    matched_skills_with_evidence: List[Dict[str, Any]] = []
    candidate_additional_skills: List[str] = []
    related_skills: Dict[str, List[str]] = {}
    recommendation: str
    experience_comparison: Dict[str, Any] = {}
    education_analysis: Dict[str, Any] = {}
    projects_analysis: Dict[str, Any] = {}
    suggestions: List[str] = []
    rank: Optional[int] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().strftime("%b %d, %Y"))
