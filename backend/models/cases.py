from pydantic import BaseModel, Field, field_serializer
from datetime import datetime
from typing import Optional
import uuid

class CaseOption(BaseModel):
    """ Model for a case option """
    key: str
    text: str
    selected: bool

class CaseEvidence(BaseModel):
    """ Model for a case evidence """
    content: str
    page_number: int
    pdf_name: str
    event_datetime: Optional[str]

class CaseStep(BaseModel):
    """ Model for a case step """
    key: str
    question: str
    options: list[CaseOption]
    reasoning: str
    decision: str
    next_step: str
    is_met: bool
    is_final: bool
    evidence: list[CaseEvidence]

class CaseRecord(BaseModel):
    """ Model for creating a new case record """
    case_id: str = Field(default_factory=lambda: str(uuid.uuid4()), frozen=True)
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow(), frozen=True)
    status: str = Field(default="submitted")
    procedure_name: Optional[str] = None
    cpt_codes: Optional[list[str]] = []
    summary: Optional[str] = None
    is_met: Optional[bool] = False
    is_complete: Optional[bool] = False
    steps: Optional[list[CaseStep]] = []

    @field_serializer("created_at")
    def serialize_datetime(self, v: datetime) -> str:
        # not preferred, but needed for FastAPI response
        return v.isoformat()

    class Config:
        from_attributes = True
