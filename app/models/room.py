from sqlalchemy import Column, String, Boolean, DateTime
from app.db.base import Base
from datetime import datetime

class Room(Base):
    __tablename__ = "rooms"

    id = Column(String, primary_key=True, index=True)
    room_name = Column(String)
    #private = Column(Boolean)

    created_at = Column(DateTime, default=datetime.utcnow)