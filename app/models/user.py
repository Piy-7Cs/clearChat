from sqlalchemy import Column, String, Boolean, DateTime, CheckConstraint
from app.db.base import Base
from datetime import datetime





class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    user_email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    #private = Column(Boolean)

    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("length(username) > 2", name="username not empty"),
                      )