import uuid
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, Field, HttpUrl

# --- Form Base Schemas ---
class FormBase(BaseModel):
    """ Base schema for Form, containing common fields """
    name: str = Field(..., min_length=1, max_length=200, description="Name of the form")
    form_data: dict[str, Any] = Field(..., description="JSON structure defining the form fields and layout")

# --- Form Create Schema ---
class FormCreate(FormBase):
    """ Schema for creating a new form. Requires user_id. """
    # user_id: uuid.UUID 
    # Usually set server-side based on authenticated user, but include if client needs to specify it.
    pass

# --- Form Update Schema ---
class FormUpdate(BaseModel):
    """ Schema for updating a form. All fields are optional. """
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="Optional new name for the form")
    form_data: Optional[dict[str, Any]] = Field(None, description="Optional new JSON structure for the form")
    is_published: Optional[bool] = Field(None, description="Optional new publication status")
    published_link: Optional[HttpUrl | None] = Field(None, description="Optional new published link (set to null if unpublished)")

# --- Form Read Schema ---
class Form(FormBase):
    """ Schema for reading/representing a Form, including DB-generated fields """
    id: uuid.UUID = Field(..., description="Unique identifier for the form")
    user_id: uuid.UUID = Field(..., description="ID of the user who owns the form")
    created_on: datetime = Field(..., description="Timestamp when the form was created")
    updated_on: datetime = Field(..., description="Timestamp when the form was last updated")
    is_published: bool = Field(..., description="Whether the form is currently published")
    published_link: Optional[HttpUrl] = Field(None, description="Publicly accessible link if the form is published")

    class Config:
        # Pydantic V2 replaces orm_mode with from_attributes=True
        orm_mode = True

# --- Schema for representing a User with their Forms (Example) ---
# class UserWithForms(User):
#    forms: List[Form] = []