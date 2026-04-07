from sqlalchemy import Column, String, Boolean, DateTime
from app.db.base import Base
from datetime import datetime





class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String)
    user_email = Column(String)
    #private = Column(Boolean)

    created_at = Column(DateTime, default=datetime.utcnow)