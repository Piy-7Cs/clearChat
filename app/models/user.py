from sqlalchemy import Column, String, Boolean
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String)
    user_email = Column(String)
    private = Column(Boolean)