from sqlalchemy import Column, String, ForeignKey, DateTime
from datetime import datetime
from app.db.base import Base

class Membership(Base):
    __tablename__ = "memberships"
     
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    room_id = Column(String, ForeignKey("rooms.id"), primary_key=True)

    role = Column(String, default="member") #member | owner | moderator
    status = Column(String, default="active") #active | pending | banned
    joined_at = Column(DateTime, default=datetime.utcnow)

