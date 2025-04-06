import uuid
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, String, DateTime, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    """
    SQLAlchemy model for the 'users' table.
    """
    __tablename__ = "user"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True
    )
    name = Column(
        String(100),
        nullable=False
    )
    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    created_on = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_on = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"

# Example of creating the table (usually done with Alembic migrations)
# if __name__ == "__main__":
#     # Replace with your actual database connection string
#     DATABASE_URL = "postgresql://user:password@host:port/database"
#     engine = create_engine(DATABASE_URL)
#     print("Creating tables...")
#     Base.metadata.create_all(bind=engine)
#     print("Tables created.")