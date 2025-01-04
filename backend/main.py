from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uuid
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

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/cases")
def create_case():
    """ Create new case """
    case_id = str(uuid.uuid4())
    cases_store[case_id] = {
        "id": case_id,
        "created_at": datetime.utcnow().isoformat(),
        "status": "submitted",
    }
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
