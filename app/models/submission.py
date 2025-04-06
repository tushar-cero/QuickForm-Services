import uuid
from datetime import datetime
from typing import Optional, List, Any, Dict # Import Any/Dict
from pydantic import BaseModel, Field

# --- Submission Base Schemas ---
class SubmissionBase(BaseModel):
    """ Base schema for Submission, primarily containing the answer data. """
    answer: Dict[str, Any] = Field(..., description="Submitted answers/data as a JSON object")

# --- Submission Create Schemas ---
class SubmissionCreate(SubmissionBase):
    """
    Schema for creating a new submission.
    Requires the ID of the form being submitted to.
    """
    form_id: uuid.UUID = Field(..., description="The ID of the form this submission belongs to")

# --- Submission Read Schemas ---
class Submission(SubmissionBase):
    """ Schema for reading/representing a Submission """
    id: uuid.UUID = Field(..., description="Unique identifier for the submission")
    form_id: uuid.UUID = Field(..., description="ID of the form this submission belongs to")
    submitted_on: datetime = Field(..., description="Timestamp when the submission was recorded")

    class Config:
        # Pydantic V2: Enable reading data directly from ORM objects from_attributes = True
        orm_mode = True

# --- Schema for representing a Form with its Submissions (Example) ---
# class FormWithSubmissions(Form):
#     submissions: List[Submission] = []