from pydantic import BaseModel

class CreateRoomRequest(BaseModel):
    name: str
    type: str = "public"


class JoinRoomRequest(BaseModel):
    room_id : str