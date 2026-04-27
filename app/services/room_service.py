import uuid
from app.models.room import Room
from app.models.membership import Membership
from app.models.user import User
from sqlalchemy.orm import Session
from fastapi import HTTPException


class RoomService:

    @staticmethod
    def create_room(db: Session, creator_id: str, name: str, type: str):
        if not name:
            raise ValueError("Name of Room Required")
        
        existing = db.query(Room).filter(Room.name == name).first()

        if existing:
            raise ValueError("Room with That name already Exists, Choose another name")
        
        room = Room(
            id = str(uuid.uuid4()),
            name = name,
            type = type
        )

        db.add(room)

        membership = Membership(
            user_id = creator_id,
            room_id = room.id,
            role = "owner",
            status = "active"
        )

        db.add(membership)

        db.commit()
        return room


    @staticmethod
    def join_room(db: Session, user_id: str, room_name : str):
        room = db.query(Room).filter(Room.name == room_name).first()

        if not room:
            raise HTTPException(status_code=404, detail="Room Not Found")
        
        existing = db.query(Membership).filter(
            Membership.user_id == user_id,
            Membership.room_id == room.id
        ).first()

        if not existing:
            member = Membership(user_id = user_id, room_id = room.id)

            db.add(member)
            db.commit()
        
        return room
    

    @staticmethod
    def is_member(db: Session, user_id: str, room_id: str) -> bool:
        return db.query(Membership).filter(
            Membership.user_id == user_id,
            Membership.room_id == room_id
        ).first() is not None


    @staticmethod
    def get_role(db: Session, user_id: str, room_id: str) -> str | None :
        m = db.query(Membership).filter(
            Membership.user_id == user_id,
            Membership.room_id == room_id
        ).first()

        return m.role if m else None


    


