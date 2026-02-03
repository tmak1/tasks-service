from sqlalchemy import Column, Integer, String
from database import Base

class Task(Base):
    __tablename__ = 'tasks'
    
    id: int = Column(Integer, primary_key=True) # type: ignore
    title: str = Column(String(100), nullable=False) # type: ignore
    owner_id: int = Column(Integer, nullable=False) # type: ignore