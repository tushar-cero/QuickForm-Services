import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    create_engine, Column, String, DateTime, func, ForeignKey, Boolean
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
# from sqlalchemy import JSON # Generic JSON type
from sqlalchemy.orm import declarative_base, relationship, Mapped

from app.db.users import User

Base = declarative_base()


class Form(Base):
    """
    SQLAlchemy model for the 'forms' table.
    Represents a form created by a user.
    """
    __tablename__ = "forms"

    id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True
    )
    name: Mapped[str] = Column(
        String(200),
        nullable=False
    )
    user_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    form_data: Mapped[dict | list] = Column(
        JSONB,
        nullable=False,
        server_default='{}'
    )
    created_on: Mapped[datetime] = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_on: Mapped[datetime] = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    is_published: Mapped[bool] = Column(
        Boolean,
        default=False,
        nullable=False,
        server_default='false'
    )
    published_link: Mapped[Optional[str]] = Column(
        String(512),
        nullable=True
    )

    user: Mapped["User"] = relationship("User", back_populates="forms")

    def __repr__(self):
        return f"<Form(id={self.id}, name='{self.name}', user_id='{self.user_id}')>"

# Example of creating the table (usually done with Alembic migrations)
# if __name__ == "__main__":
#     # Replace with your actual database connection string
#     DATABASE_URL = "postgresql://user:password@host:port/database"
#     engine = create_engine(DATABASE_URL)
#     print("Creating tables...")
#     Base.metadata.create_all(bind=engine)
#     print("Tables created.")