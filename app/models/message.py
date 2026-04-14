from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from datetime import datetime
from app.db.base import Base
from app.models.user import User
from app.models.room import Room


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, index=True)

    sender_id = Column(String, ForeignKey("users.id"))
    recipient_id = Column(String, ForeignKey("users.id"), nullable=True)

    room_id = Column(String, ForeignKey("rooms.id"), nullable=True)
    content = Column(String)
    
    created_at = Column(DateTime, default=datetime.utcnow)


