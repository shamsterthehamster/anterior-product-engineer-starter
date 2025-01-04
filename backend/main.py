from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uuid
import time
from typing import Optional
import json
from pathlib import Path
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary in-memory storage for cases
cases_store = {}

def _get_case_responses(status: str) -> dict:
    """ Helper method to get example case responses"""
    asset_path = Path(__file__).parent.parent.resolve() / "assets"
    if status == "submitted":
        json_path = asset_path / "response-1.json"
    elif status == "processing":
        json_path = asset_path / "response-2.json"
    elif status == "completed":
        json_path = asset_path / "response-3.json"
    else:
        raise ValueError(f"Invalid status: {status}")
    
    with open(json_path, "r") as file:
        return json.load(file)
    

def simulate_case_processing(case_id: str):
    """ Simulates background case processing """
    if case_id in cases_store:
        current_status = cases_store[case_id]["status"]
    else:
        return
    if current_status == "submitted":
        case_response = _get_case_responses(current_status)
        cases_store[case_id]["procedure_name"] = case_response["procedure_name"]
        cases_store[case_id]["cpt_codes"] = case_response["cpt_codes"]
        cases_store[case_id]["summary"] = case_response["summary"]
        cases_store[case_id]["is_met"] = case_response["is_met"]
        cases_store[case_id]["is_complete"] = case_response["is_complete"]
        cases_store[case_id]["steps"] = case_response["steps"]
        time.sleep(10)
        current_status = "processing"
        cases_store[case_id]["status"] = current_status
    if current_status == "processing":
        case_response = _get_case_responses(current_status)
        cases_store[case_id]["procedure_name"] = case_response["procedure_name"]
        cases_store[case_id]["cpt_codes"] = case_response["cpt_codes"]
        cases_store[case_id]["summary"] = case_response["summary"]
        cases_store[case_id]["is_met"] = case_response["is_met"]
        cases_store[case_id]["is_complete"] = case_response["is_complete"]
        cases_store[case_id]["steps"] = case_response["steps"]
        time.sleep(20)
        current_status = "completed"
        cases_store[case_id]["status"] = current_status
    if current_status == "completed":
        case_response = _get_case_responses(current_status)
        cases_store[case_id]["procedure_name"] = case_response["procedure_name"]
        cases_store[case_id]["cpt_codes"] = case_response["cpt_codes"]
        cases_store[case_id]["summary"] = case_response["summary"]
        cases_store[case_id]["is_met"] = case_response["is_met"]
        cases_store[case_id]["is_complete"] = case_response["is_complete"]
        cases_store[case_id]["steps"] = case_response["steps"]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/cases")
def create_case(background_tasks: BackgroundTasks):
    """ Create new case """
    case_id = str(uuid.uuid4())
    case = {
        "case_id": case_id,
        "created_at": datetime.utcnow().isoformat(),
        "status": "submitted",
        "procedure_name": "Facet Joint Injection",
        "cpt_codes": [
            "64490",
            "64491",
            "64492",
            "64493",
            "64494",
            "64495"
        ],
        "summary": None,
        "is_met": False,
        "is_complete": False,
        "steps": []
    }
    cases_store[case_id] = case
    background_tasks.add_task(simulate_case_processing, case_id)
    return {"id": case_id}


@app.get("/cases/{case_id}")
def get_case(case_id: str):
    """ Get case by id """
    case = cases_store.get(case_id)
    if not case:
        return {"error": "Case not found"}
    return case


@app.get("/cases")
def get_cases():
    """ Get all cases """
    return list(cases_store.values())
