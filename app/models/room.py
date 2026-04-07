from sqlalchemy import Column, String, Boolean
from app.db.base import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(String, primary_key=True, index=True)
    room_name = Column(String)
    private = Column(Boolean)