import uuid
from sqlalchemy import Column, String, Text, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from src.db.database import Base

class Vacancy(Base):
    __tablename__ = 'vacancies'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_id = Column(String, nullable=True) # ID from the source site
    title = Column(String, nullable=False)
    company = Column(String, nullable=True)
    url = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    source = Column(String, nullable=False) # e.g., 'linkedin', 'indeed'
    raw_data = Column(JSON, nullable=True)
    status = Column(String, default='new') # new, analyzed, applied, rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Vacancy(title='{self.title}', company='{self.company}')>"
