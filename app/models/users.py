import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# --- Base User Schema ---
class UserBase(BaseModel):
    """
    Base Pydantic schema for User, containing common fields.
    """
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's unique email address") # Built-in email validation

# --- Update Schema ---
class UserCreate(UserBase):
    """
    Schema for creating a new user. Inherits name and email from UserBase.
    No additional fields needed here based on the request, but could include password etc.
    """
    pass


# --- Update Schema ---
class UserUpdate(BaseModel):
    """
    Schema for updating an existing user. All fields are optional.
    """
    name: str | None = Field(None, min_length=1, max_length=100, description="Optional new name")
    email: EmailStr | None = Field(None, description="Optional new email address")


# --- Read Schema ---
class User(UserBase):
    """
    Schema for reading user data, including database-generated fields.
    Used for API responses.
    """
    id: uuid.UUID = Field(..., description="Unique identifier for the user")
    created_on: datetime = Field(..., description="Timestamp when the user was created")
    updated_on: datetime = Field(..., description="Timestamp when the user was last updated")

    class Config:
        orm_mode = True