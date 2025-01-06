from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from datetime import datetime
import json
from models.cases import CaseRecord
from models.um_database import CaseRecord as DBCaseRecord
from sqlalchemy.orm import Session
from db import get_db
from pathlib import Path
import time
import uuid
router = APIRouter()

def _get_case_responses(status: str) -> CaseRecord:
    """ Helper method to get example case responses"""
    asset_path = Path(__file__).parent.parent.parent.resolve() / "assets"
    if status == "submitted":
        json_path = asset_path / "response-1.json"
    elif status == "processing":
        json_path = asset_path / "response-2.json"
    elif status == "complete":
        json_path = asset_path / "response-3.json"
    else:
        raise ValueError(f"Invalid status: {status}")
    
    with open(json_path, "r") as file:
        data = json.load(file)
        sanitized_record = CaseRecord(**data).model_copy()
        return sanitized_record
    

def simulate_case_processing(case_id: str, db: Session):
    """ Simulates background case processing """
    # Get case from database
    case = db.query(DBCaseRecord).filter(DBCaseRecord.case_id == case_id).first()
    if not case:
        return
    
    # Submission takes 10 seconds
    if case.status == "submitted":
        case_response = _get_case_responses(case.status)
        for key, value in case_response.model_dump(exclude={"case_id", "created_at"}).items():
            setattr(case, key, value)
        db.commit()
        time.sleep(10)
        case.status = "processing"
    if case.status == "processing":
        case_response = _get_case_responses(case.status)
        for key, value in case_response.model_dump(exclude={"case_id", "created_at"}).items():
            setattr(case, key, value)
        db.commit()
        time.sleep(20)
        case.status = "complete"
    if case.status == "complete":
        case_response = _get_case_responses(case.status)
        for key, value in case_response.model_dump(exclude={"case_id", "created_at"}).items():
            setattr(case, key, value)
        db.commit()


@router.post("/")
def create_case(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """ Create new case and returns generated id """
    case = DBCaseRecord(case_id=str(uuid.uuid4()), status="submitted")
    db.add(case)
    db.commit()
    background_tasks.add_task(simulate_case_processing, case.case_id, db)
    return {"id": case.case_id}


@router.get("/{case_id}", response_model=CaseRecord)
def get_case(case_id: str, db: Session = Depends(get_db)):
    """ Get case by id """
    case = db.query(DBCaseRecord).filter(DBCaseRecord.case_id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.get("/", response_model=list[CaseRecord])
def get_cases(db: Session = Depends(get_db)):
    """ Get all cases """
    all_cases = db.query(DBCaseRecord).all()
    return all_cases