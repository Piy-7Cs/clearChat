from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from datetime import datetime
from app.db.base import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(String, primary_key=True)
    name = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)


