from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.services.room_service import RoomService
from app.models.user import User

from app.schemas.room_schema import JoinRoomRequest
from app.schemas.room_schema import CreateRoomRequest


router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.post("/create")
def create_room(
                    data: CreateRoomRequest,
                    db: Session = Depends(get_db),
                    user: User = Depends(get_current_user)
                ):
    
    room = RoomService.create_room(
        db, user.id, data.name, data.type
    )

    return {
        "message": "room created",
        "room_id": room.id,
        "room_name": room.name
    }
    
@router.post("/join")
def join_room(data: JoinRoomRequest,
              db: Session = Depends(get_db),
              user: User = Depends(get_current_user)):
    
    room = RoomService.join_room(db, user.id, data.room_id)

    return {
        "message": "joined room",
        "room_id": room.id
    }


