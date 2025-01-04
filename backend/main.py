from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uuid
import time
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

def simulate_case_processing(case_id: str):
    """ Simulates background case processing """
    time.sleep(10)
    if case_id in cases_store:
        cases_store[case_id]["status"] = "processing"
        cases_store[case_id]["summary"] = "Summary of the case"
    time.sleep(20)
    if case_id in cases_store:
        json_path = Path(__file__).parent.parent.resolve() / "assets" / "response-3.json"
        with open(json_path, "r") as file:
            data = json.load(file)
            if "steps" in data:
                cases_store[case_id]["steps"] = data["steps"]
            else:
                cases_store[case_id]["steps"] = "Steps not found"
        cases_store[case_id]["status"] = "completed"

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
