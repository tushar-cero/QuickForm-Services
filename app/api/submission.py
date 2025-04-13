import uuid
from datetime import datetime, timezone
from typing import List, Dict, Optional
from fastapi import APIRouter, HTTPException, status, Path

from app.models.submission import Submission, SubmissionCreate
from app.db.submission import Submission as SubmissionSQLAlchemy


# --- In-Memory Data Store (Simulates a Database) ---
submissions_db: Dict[uuid.UUID, SubmissionSQLAlchemy] = {}

# --- API Router ---
router = APIRouter(
    prefix="/submissions",
    tags=["Submissions"]
)

# --- Dependency (Example Placeholder) ---
# In a real app, you might have dependencies for DB sessions or getting Form objects
async def get_form_or_404(form_id: uuid.UUID):
    """
    Placeholder dependency to simulate checking if a form exists.
    In a real app, this would query the forms database.
    """
    print(f"Info: (Simulation) Checked existence for form_id: {form_id}")
    return form_id # Return the ID if valid, or raise exception

# --- API Endpoints ---

@router.post(
    "/", # Relative to the router prefix: POST /submissions/
    response_model=Submission,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Submission for a Form",
)
async def create_submission(
    submission_in: SubmissionCreate,
):
    """
    Creates a new submission record for a specified form.

    - Requires `form_id` and the submission `answer` data in the request body.
    - The server generates the unique submission `id` and `submitted_on` timestamp.
    - **Note:** In a real application, this endpoint *must* verify that the
      provided `form_id` corresponds to an existing form before creating the submission.
    """
    await get_form_or_404(submission_in.form_id)

    now = datetime.now(timezone.utc)
    new_id = uuid.uuid4()

    db_submission = Submission(
        id=new_id,
        form_id=submission_in.form_id,
        answer=submission_in.answer,
        submitted_on=now,
    )

    submissions_db[db_submission.id] = db_submission
    print(f"Debug: Created Submission {db_submission.id} for Form {db_submission.form_id}")

    return db_submission

@router.get(
    "/", # Relative to the router prefix: GET /submissions/
    response_model=List[Submission],
    summary="Read all Submissions (optionally filtered by Form ID)",
)
async def read_submissions(
    form_id: Optional[uuid.UUID] = None # Query parameter for filtering
) -> List[Submission]:
    """
    Retrieves a list of submissions.

    - Optionally filters submissions by the `form_id` query parameter.
    - **Note:** If filtering by `form_id`, ensure the form actually exists
      in a real application.
    """
    if form_id:
        # --- Optional: Check if form_id exists before filtering ---
        # await get_form_or_404(form_id) # Simulate check
        # ---
        print(f"Debug: Filtering submissions for form_id: {form_id}")
        filtered_submissions = [
            sub for sub in submissions_db.values() if sub.form_id == form_id
        ]
        return filtered_submissions
    else:
        print("Debug: Returning all submissions")
        return list(submissions_db.values())


@router.get(
    "/{submission_id}", # Relative to router prefix: GET /submissions/{submission_id}
    response_model=Submission,
    summary="Read a specific Submission by ID",
)
async def read_submission(
    submission_id: uuid.UUID = Path(..., description="The unique identifier of the submission to retrieve")
) -> Submission:
    """
    Retrieves the details of a specific submission using its unique ID.
    """
    submission = submissions_db.get(submission_id)
    if not submission:
        print(f"Debug: Submission not found: {submission_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Submission with ID {submission_id} not found"
        )
    print(f"Debug: Found submission: {submission_id}")
    return submission
