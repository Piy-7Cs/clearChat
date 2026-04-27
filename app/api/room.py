from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.services.room_service import RoomService
from app.models.user import User


router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.post("/create")
def create_room(name: str,
                type: str,
                db: Session = Depends(get_db), 
                user: User = Depends(get_current_user)):
    
    room = RoomService.create_room(db, user.id, name, type)

    return {
        "message" : "room created",
        "room_id" : room.id,
        "room_name" : room.name
    }

    
@router.post("/join")
def join_room(name: str,
              db: Session = Depends(get_db),
              user: User = Depends(get_current_user)):
    room = RoomService.join_room(db, user.id, name)

    return {
        "message": "joined room",
        "room_id": room.id
    }