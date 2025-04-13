import uuid
from datetime import datetime, timezone
from typing import Dict
from fastapi import FastAPI, HTTPException, status, Path

from app.db.form import Form
from app.models.form import FormCreate

# --- In-Memory Data Store (Simulates a Database) ---
forms_db: Dict[uuid.UUID, Form] = {}

# --- FastAPI Application ---
app = FastAPI(
    title="Form Management API",
    description="API for Creating, Reading, and Deleting Forms.",
    version="1.0.0"
)

# --- API Endpoints ---
@app.post(
    "/forms/",
    response_model=Form,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Form",
    tags=["Forms"]
)
async def create_form(form_in: FormCreate) -> Form:
    """
    Creates a new form with the provided data.

    - **name**: The name/title of the form.
    - **form_data**: The JSON definition of the form's structure and fields.

    Server-side generated fields (`id`, `user_id`, timestamps, `is_published`, `published_link`)
    will be added automatically.
    """
    now = datetime.now(timezone.utc)
    new_id = uuid.uuid4()

    # --- To Do: Simulate getting user_id from authentication ---
    # In a real app, this would come from the authenticated user context
    # Example: current_user: User = Depends(get_current_active_user)
    # user_id = current_user.id
    simulated_user_id = uuid.uuid4() # Replace with actual user ID logic
    # ----------------------------------------------------

    db_form = Form(
        id=new_id,
        user_id=simulated_user_id,
        name=form_in.name,
        form_data=form_in.form_data,
        created_on=now,
        updated_on=now,
        is_published=False,
        published_link=None
    )

    forms_db[db_form.id] = db_form

    return db_form

@app.get(
    "/forms/{form_id}",
    response_model=Form,
    summary="Read a specific Form by ID",
    tags=["Forms"]
)
async def read_form(
    form_id: uuid.UUID = Path(..., description="The unique identifier of the form to retrieve")
) -> Form:
    """
    Retrieves the details of a specific form using its unique ID.
    """
    form = forms_db.get(form_id)
    if not form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Form with ID {form_id} not found"
        )
    return form

@app.delete(
    "/forms/{form_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a specific Form by ID",
    tags=["Forms"]
)
async def delete_form(
    form_id: uuid.UUID = Path(..., description="The unique identifier of the form to delete")
) -> None:
    """
    Deletes a specific form using its unique ID.

    Returns `204 No Content` on successful deletion.
    Returns `404 Not Found` if the form ID does not exist.
    """
    if form_id not in forms_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Form with ID {form_id} not found"
        )

    del forms_db[form_id]
    return None