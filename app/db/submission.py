# models.py
import uuid
from datetime import datetime
from typing import Any, Dict

from sqlalchemy import (
    create_engine, Column, DateTime, func, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base, relationship, Mapped

from app.db.form import Form

Base = declarative_base()

class Submission(Base):
    """
    SQLAlchemy model for the 'submissions' table.
    Represents data submitted to a specific form.
    """
    __tablename__ = "submissions"

    id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True
    )
    form_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        ForeignKey('forms.id', ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    answer: Mapped[Dict[str, Any]] = Column(
        JSONB,
        nullable=False
    )
    submitted_on: Mapped[datetime] = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )

    form: Mapped["Form"] = relationship("Form", back_populates="submissions")

    def __repr__(self):
        return f"<Submission(id={self.id}, form_id='{self.form_id}', submitted_on='{self.submitted_on}')>"

# Example of creating the table (usually done with Alembic migrations)
# if __name__ == "__main__":
#     # Replace with your actual database connection string
#     DATABASE_URL = "postgresql://user:password@host:port/database"
#     engine = create_engine(DATABASE_URL)
#     print("Creating tables...")
#     Base.metadata.create_all(bind=engine)
#     print("Tables created.")