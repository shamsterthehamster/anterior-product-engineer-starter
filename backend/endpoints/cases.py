from fastapi import APIRouter, BackgroundTasks
import json
from models.cases import CaseRecord
from pathlib import Path
import time

router = APIRouter()

# Temporary in-memory storage for cases
cases_store: dict[str, CaseRecord] = {}

def _get_case_responses(status: str) -> dict:
    """ Helper method to get example case responses"""
    asset_path = Path(__file__).parent.parent.parent.resolve() / "assets"
    if status == "submitted":
        json_path = asset_path / "response-1.json"
    elif status == "processing":
        json_path = asset_path / "response-2.json"
    elif status == "completed":
        json_path = asset_path / "response-3.json"
    else:
        raise ValueError(f"Invalid status: {status}")
    
    with open(json_path, "r") as file:
        data = json.load(file)
        sanitized_record = CaseRecord(**data).dict(exclude={"case_id", "created_at"})
        return sanitized_record
    

def simulate_case_processing(case_id: str):
    """ Simulates background case processing """
    if case_id in cases_store:
        case = cases_store[case_id]
    else:
        return
    if case.status == "submitted":
        case_response = _get_case_responses(case.status)
        case = case.model_copy(update=case_response)
        cases_store[case_id] = case
        time.sleep(10)
        case.status = "processing"
    if case.status == "processing":
        case_response = _get_case_responses(case.status)
        case = case.model_copy(update=case_response)
        cases_store[case_id] = case
        time.sleep(20)
        case.status = "completed"
    if case.status == "completed":
        case_response = _get_case_responses(case.status)
        case = case.model_copy(update=case_response)
        cases_store[case_id] = case


@router.post("/")
def create_case(background_tasks: BackgroundTasks):
    """ Create new case and returns generated id """
    case = CaseRecord()
    cases_store[case.case_id] = case
    background_tasks.add_task(simulate_case_processing, case.case_id)
    return {"id": case.case_id}


@router.get("/{case_id}", response_model=CaseRecord)
def get_case(case_id: str):
    """ Get case by id """
    case = cases_store.get(case_id)
    if not case:
        return {"error": "Case not found"}
    return case


@router.get("/", response_model=list[CaseRecord])
def get_cases():
    """ Get all cases """
    return list(cases_store.values())
