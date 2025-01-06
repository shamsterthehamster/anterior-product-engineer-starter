from sqlalchemy import Column, String, Boolean, TIMESTAMP, JSON, ARRAY
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class CaseRecord(Base):
    """Table for storing case records"""
    __tablename__ = "case_records"

    case_id = Column(String, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    status = Column(String, nullable=False, default="submitted")
    procedure_name = Column(String, nullable=True)
    cpt_codes = Column(ARRAY(String), nullable=True)  # Store as comma-separated values
    steps = Column(JSON, nullable=True)  # Stores nested list of dicts as JSON
    summary = Column(String, nullable=True)
    is_met = Column(Boolean, nullable=True)