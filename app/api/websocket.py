from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.services.connection_manager import chat_manager
from app.services.message_service import MessageService
from app.services.room_service import RoomService
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
            action = data.get("action")

            data["from"] = user_id


            if action == "private":
            
                try: 

                    msg, target_id = MessageService.send_private_messgae(
                    db, user_id, data.get("target"), data.get("message")
                )

                    if target_id in chat_manager.active:
                        await chat_manager.active[target_id].send_json({
                            "from" : user_id,
                            "message" : msg.content
                        })
                except ValueError as e:
                    await websocket.send_json({"error": str(e)})
            


            elif action == "get_private_history":
                try:
                    messages = MessageService.get_private_history(
                        db, user_id, data.get("target")
                    )
                
                    await websocket.send_json({
                        "type": "private_history",
                        "messages": [
                            {
                                "from": msg.sender_id,
                                "message": msg.content
                            } for msg in messages
                        ]
                    })
                except ValueError as e:
                    await websocket.send_json("error", str(e))
                

            elif action == "join":

                try: 
                    room = RoomService.join_room(db, user_id, data.get("room_id"))

                    chat_manager.join_room(room.id, user_id)

                    messages = MessageService.get_room_history(db, room.id)

                    
                    await websocket.send_json({
                        "from": "system",
                        "message": f"Joined room {room.id}"
                    })

                    await websocket.send_json(
                        {
                            "type": "history",
                            "messages": [
                                {
                                    "from": user_id,
                                    "message": msg.content
                                } for msg in messages
                            ]
                        })


                except ValueError as e:
                    await websocket.send_json({"error": str(e)})




            elif action == "send_room_message":

                try:
                    msg = MessageService.send_room_message(
                        db, user_id, data.get("room_id"), data.get("message")
                    )

                    await chat_manager.broadcast(
                        data.get("room_id"), 
                        {
                            "from" : user_id,
                            "message" : msg.content
                        }
                    )
                except ValueError as e:
                    await websocket.send_json({"error" : str(e)})


    except WebSocketDisconnect:
        chat_manager.disconnect(user_id)


    finally:
        db.close()