from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json

from ..parser.resume_parser import parse_resume_file, parse_resume_text
from ..matching.matcher import match_resume_to_job, rank_candidates
from ..database.models import ResumeRecord, MatchResultRecord
from ..database.session import SQLiteDatabase, get_db

router = APIRouter()

class TextParseRequest(BaseModel):
    text: str

class MatchRequest(BaseModel):
    resume_text: Optional[str] = None
    resume_id: Optional[str] = None
    job_description: str
    job_title: Optional[str] = "Target Role"
    filename: Optional[str] = None

class CandidateBatchItem(BaseModel):
    name: Optional[str] = "Candidate"
    filename: Optional[str] = "Resume.pdf"
    text: str

class BatchMatchRequest(BaseModel):
    candidates: List[CandidateBatchItem]
    job_description: str
    job_title: Optional[str] = "Target Position"

@router.post("/parse-text")
def parse_text_endpoint(payload: TextParseRequest):
    """Parse raw text directly and extract candidate metadata & skills."""
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    return parse_resume_text(payload.text)

@router.post("/upload-resume")
async def upload_resume_endpoint(
    file: UploadFile = File(...),
    db: SQLiteDatabase = Depends(get_db)
):
    """Upload a single resume file (PDF, DOCX, or TXT), parse it, and return extracted data."""
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    
    parsed = parse_resume_file(content, file.filename or "uploaded_resume")
    
    record = ResumeRecord(
        candidate_name=parsed.get("candidate_name", "Candidate"),
        filename=parsed.get("filename", "uploaded_resume"),
        parsed_skills=parsed.get("skills", []),
        categorized_skills=parsed.get("categorized_skills", {}),
        email=parsed.get("email"),
        phone=parsed.get("phone"),
        location=parsed.get("location"),
        education=parsed.get("education", []),
        education_details=parsed.get("education_details", {}),
        experience_display=parsed.get("experience_display"),
        experience_years=parsed.get("experience_years", 0.0),
        projects=parsed.get("projects", []),
        certifications=parsed.get("certifications", []),
        raw_text=parsed.get("raw_text", ""),
        needs_manual_review=parsed.get("needs_manual_review", False),
        missing_fields=parsed.get("missing_fields", [])
    )
    db.save_resume(record)
    
    return {
        "id": record.id,
        "candidate_name": record.candidate_name,
        "filename": record.filename,
        "email": record.email,
        "phone": record.phone,
        "location": record.location,
        "skills": record.parsed_skills,
        "categorized_skills": record.categorized_skills,
        "education": record.education,
        "education_details": record.education_details,
        "experience_display": record.experience_display,
        "experience_years": record.experience_years,
        "projects": record.projects,
        "certifications": record.certifications,
        "raw_text": record.raw_text,
        "summary": parsed.get("summary"),
        "needs_manual_review": record.needs_manual_review,
        "missing_fields": record.missing_fields
    }

@router.post("/upload-batch")
async def upload_batch_endpoint(
    files: List[UploadFile] = File(...),
    db: SQLiteDatabase = Depends(get_db)
):
    """Upload a batch of multiple resumes (PDF, DOCX, TXT; at least 10 supported), parse all of them."""
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")
        
    parsed_resumes = []
    errors = []
    
    for file in files:
        try:
            content = await file.read()
            if not content:
                errors.append({"filename": file.filename, "error": "File is empty"})
                continue
                
            parsed = parse_resume_file(content, file.filename or "uploaded_resume")
            record = ResumeRecord(
                candidate_name=parsed.get("candidate_name", "Candidate"),
                filename=parsed.get("filename", "uploaded_resume"),
                parsed_skills=parsed.get("skills", []),
                categorized_skills=parsed.get("categorized_skills", {}),
                email=parsed.get("email"),
                phone=parsed.get("phone"),
                location=parsed.get("location"),
                education=parsed.get("education", []),
                education_details=parsed.get("education_details", {}),
                experience_display=parsed.get("experience_display"),
                experience_years=parsed.get("experience_years", 0.0),
                projects=parsed.get("projects", []),
                certifications=parsed.get("certifications", []),
                raw_text=parsed.get("raw_text", ""),
                needs_manual_review=parsed.get("needs_manual_review", False),
                missing_fields=parsed.get("missing_fields", [])
            )
            db.save_resume(record)
            
            parsed_resumes.append({
                "id": record.id,
                "candidate_name": record.candidate_name,
                "filename": record.filename,
                "email": record.email,
                "phone": record.phone,
                "location": record.location,
                "skills": record.parsed_skills,
                "experience_display": record.experience_display,
                "education": record.education,
                "raw_text": record.raw_text,
                "needs_manual_review": record.needs_manual_review
            })
        except Exception as e:
            errors.append({"filename": file.filename, "error": str(e)})
            
    return {
        "total_uploaded": len(files),
        "successful_count": len(parsed_resumes),
        "resumes": parsed_resumes,
        "errors": errors
    }

@router.post("/match")
def match_endpoint(
    payload: MatchRequest,
    db: SQLiteDatabase = Depends(get_db)
):
    """Match resume against job description using 5-component scoring formula and save to history."""
    resume_text = payload.resume_text
    filename = payload.filename
    
    if payload.resume_id:
        resume_record = db.get_resume(payload.resume_id)
        if not resume_record:
            raise HTTPException(status_code=404, detail="Resume record not found.")
        resume_text = resume_record.raw_text
        filename = resume_record.filename
        
    if not resume_text or not resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text or a valid resume_id must be provided.")
        
    if not payload.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")
        
    match_result = match_resume_to_job(resume_text, payload.job_description)
    
    record = MatchResultRecord(
        candidate_name=match_result.get("candidate_name", "Candidate"),
        job_title=payload.job_title or "Target Position",
        filename=filename or "Uploaded_Resume.pdf",
        overall_score=match_result["overall_score"],
        cosine_similarity=match_result["cosine_similarity"],
        skill_match_score=match_result["skill_match_score"],
        experience_score=match_result.get("experience_score", 0.0),
        education_score=match_result.get("education_score", 0.0),
        projects_score=match_result.get("projects_score", 0.0),
        score_breakdown=match_result.get("score_breakdown", {}),
        ai_score_explanation=match_result.get("ai_score_explanation"),
        matched_skills=match_result["matched_skills"],
        missing_skills=match_result["missing_skills"],
        matched_required_skills=match_result.get("matched_required_skills", []),
        missing_required_skills=match_result.get("missing_required_skills", []),
        matched_preferred_skills=match_result.get("matched_preferred_skills", []),
        missing_preferred_skills=match_result.get("missing_preferred_skills", []),
        matched_skills_with_evidence=match_result.get("matched_skills_with_evidence", []),
        candidate_additional_skills=match_result["candidate_additional_skills"],
        related_skills=match_result.get("related_skills", {}),
        recommendation=match_result["recommendation"],
        experience_comparison=match_result.get("experience_comparison", {}),
        education_analysis=match_result.get("education_analysis", {}),
        projects_analysis=match_result.get("projects_analysis", {}),
        suggestions=match_result.get("suggestions", [])
    )
    db.save_match(record)
    
    match_result["id"] = record.id
    match_result["created_at"] = record.created_at
    match_result["job_title"] = record.job_title
    match_result["filename"] = record.filename
    return match_result

@router.post("/match-batch")
def match_batch_endpoint(
    payload: BatchMatchRequest,
    db: SQLiteDatabase = Depends(get_db)
):
    """Match multiple candidate resumes against a job description, rank them in order,
    and provide executive AI reasoning for why the top candidate was chosen.
    """
    if not payload.candidates:
        raise HTTPException(status_code=400, detail="Candidate list cannot be empty.")
    if not payload.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")
        
    candidate_matches = []
    
    for cand in payload.candidates:
        if not cand.text.strip():
            continue
            
        result = match_resume_to_job(cand.text, payload.job_description)
        
        # Override name/filename if provided by candidate object
        if cand.name and cand.name != "Candidate":
            result["candidate_name"] = cand.name
        result["filename"] = cand.filename or "Resume.pdf"
        result["job_title"] = payload.job_title
        
        # Save each to DB history
        record = MatchResultRecord(
            candidate_name=result["candidate_name"],
            job_title=payload.job_title or "Target Position",
            filename=result["filename"],
            overall_score=result["overall_score"],
            cosine_similarity=result["cosine_similarity"],
            skill_match_score=result["skill_match_score"],
            experience_score=result.get("experience_score", 0.0),
            education_score=result.get("education_score", 0.0),
            projects_score=result.get("projects_score", 0.0),
            score_breakdown=result.get("score_breakdown", {}),
            ai_score_explanation=result.get("ai_score_explanation"),
            matched_skills=result["matched_skills"],
            missing_skills=result["missing_skills"],
            matched_required_skills=result.get("matched_required_skills", []),
            missing_required_skills=result.get("missing_required_skills", []),
            matched_preferred_skills=result.get("matched_preferred_skills", []),
            missing_preferred_skills=result.get("missing_preferred_skills", []),
            matched_skills_with_evidence=result.get("matched_skills_with_evidence", []),
            candidate_additional_skills=result["candidate_additional_skills"],
            related_skills=result.get("related_skills", {}),
            recommendation=result["recommendation"],
            experience_comparison=result.get("experience_comparison", {}),
            education_analysis=result.get("education_analysis", {}),
            projects_analysis=result.get("projects_analysis", {}),
            suggestions=result.get("suggestions", [])
        )
        db.save_match(record)
        
        result["id"] = record.id
        result["created_at"] = record.created_at
        candidate_matches.append(result)
        
    # Rank candidates and formulate top-candidate selection reasoning
    ranking_data = rank_candidates(candidate_matches, payload.job_title)
    
    return ranking_data

@router.post("/match-files-batch")
async def match_files_batch_endpoint(
    files: List[UploadFile] = File(...),
    job_description: str = Form(...),
    job_title: str = Form("Target Role"),
    db: SQLiteDatabase = Depends(get_db)
):
    """Direct multipart endpoint: HR Admin uploads multiple resume files (PDF, DOCX, TXT)
    along with job description, matches all, and returns ranked profiles with AI selection reasoning.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")
        
    candidate_matches = []
    errors = []
    
    for file in files:
        try:
            content = await file.read()
            if not content:
                errors.append({"filename": file.filename, "error": "Empty file"})
                continue
                
            parsed = parse_resume_file(content, file.filename or "Resume.pdf")
            raw_text = parsed.get("raw_text", "")
            if not raw_text.strip():
                errors.append({"filename": file.filename, "error": "No readable text extracted"})
                continue
                
            result = match_resume_to_job(raw_text, job_description)
            result["candidate_name"] = parsed.get("candidate_name") or file.filename.split(".")[0]
            result["filename"] = file.filename
            result["job_title"] = job_title
            
            # Save to database
            record = MatchResultRecord(
                candidate_name=result["candidate_name"],
                job_title=job_title,
                filename=result["filename"],
                overall_score=result["overall_score"],
                cosine_similarity=result["cosine_similarity"],
                skill_match_score=result["skill_match_score"],
                experience_score=result.get("experience_score", 0.0),
                education_score=result.get("education_score", 0.0),
                projects_score=result.get("projects_score", 0.0),
                score_breakdown=result.get("score_breakdown", {}),
                ai_score_explanation=result.get("ai_score_explanation"),
                matched_skills=result["matched_skills"],
                missing_skills=result["missing_skills"],
                matched_required_skills=result.get("matched_required_skills", []),
                missing_required_skills=result.get("missing_required_skills", []),
                matched_preferred_skills=result.get("matched_preferred_skills", []),
                missing_preferred_skills=result.get("missing_preferred_skills", []),
                matched_skills_with_evidence=result.get("matched_skills_with_evidence", []),
                candidate_additional_skills=result["candidate_additional_skills"],
                related_skills=result.get("related_skills", {}),
                recommendation=result["recommendation"],
                experience_comparison=result.get("experience_comparison", {}),
                education_analysis=result.get("education_analysis", {}),
                projects_analysis=result.get("projects_analysis", {}),
                suggestions=result.get("suggestions", [])
            )
            db.save_match(record)
            
            result["id"] = record.id
            result["created_at"] = record.created_at
            candidate_matches.append(result)
        except Exception as e:
            errors.append({"filename": file.filename, "error": str(e)})
            
    ranking_data = rank_candidates(candidate_matches, job_title)
    ranking_data["errors"] = errors
    return ranking_data

@router.get("/db-status")
def db_status_endpoint(db: SQLiteDatabase = Depends(get_db)):
    """Check live SQLite database connection status."""
    return db.check_connection()

@router.get("/stats")
def stats_endpoint(db: SQLiteDatabase = Depends(get_db)):
    """Return dashboard analytics and statistics."""
    return db.get_stats()

@router.get("/history")
def history_endpoint(db: SQLiteDatabase = Depends(get_db)):
    """Return analysis history list."""
    return db.list_matches()

@router.get("/history/{record_id}")
def history_item_endpoint(record_id: str, db: SQLiteDatabase = Depends(get_db)):
    """Get single match analysis record."""
    record = db.get_match(record_id)
    if record:
        return record
    raise HTTPException(status_code=404, detail="Analysis record not found.")

@router.delete("/history/{record_id}")
def delete_history_item_endpoint(record_id: str, db: SQLiteDatabase = Depends(get_db)):
    """Delete a single match analysis record from history."""
    if db.delete_match(record_id):
        return {"status": "deleted", "id": record_id}
    raise HTTPException(status_code=404, detail="Record not found.")

@router.get("/resumes")
def list_resumes_endpoint(db: SQLiteDatabase = Depends(get_db)):
    """List all uploaded and parsed resumes."""
    return db.list_resumes()
