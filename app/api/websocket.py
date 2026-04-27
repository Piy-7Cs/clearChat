from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.services.connection_manager import chat_manager
from app.services.message_service import MessageService
from app.services.room_service import RoomService
from app.ws.router import handlers
from sqlalchemy import or_, and_



#DB imports
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.message import Message
from app.models.user import User
from app.db.session import SessionLocal
import uuid

#auth imports
from app.core.security import decode_token




router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    db = SessionLocal()

    token = websocket.query_params.get("token")

    if not token:
        await websocket.close()
        return

    payload = decode_token(token)

    if not payload:
        await websocket.close()
        return

    user_id = payload.get("sub")


    if not user_id:
        await websocket.close()
        return
    
    await chat_manager.connect(user_id, websocket)


    try:
        while True:
            data = await websocket.receive_json()
            
            msg_type = data.get("type")
            handler = handlers.get(msg_type)

            if not handler:
                await websocket.send_json({
                    "type": "error",
                    "message" : "Invalid type"
                })

            await handler(websocket, db, user_id, data, chat_manager)

    except WebSocketDisconnect:
        chat_manager.disconnect(user_id)
    
    finally:
        db.close()
