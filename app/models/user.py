from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.models import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_admin = Column(Integer, default=0)  # 0: 일반 사용자, 1: 관리자
