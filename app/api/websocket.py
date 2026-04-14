from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.services.connection_manager import chat_manager

#DB imports
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.message import Message
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
                target = data.get("target")

                msg = Message(
                    id = str(uuid.uuid4()),
                    sender_id = user_id,
                    room_id = None,
                    content = data["message"]
                )

                db.add(msg)
                db.commit()

                try: 
                    target_socket = chat_manager.get_target_connection(target)
                    await target_socket.send_json({
                        "from": user_id,
                        "message": data["message"]
                    })
                except KeyError:
                    await websocket.send_json({"error": "recipient not connected"})
            


            elif action == "join":
                room_id = data.get("room_id")
                chat_manager.join_room(room_id, user_id)

                await websocket.send_json({
                    "from": "system",
                    "message": f"Joined room {room_id}"
                })



            elif action == "send_room_message":

                room_id = data.get("room_id")

                if "message" not in data:
                    continue
                
                msg = Message(
                    id = str(uuid.uuid4()),
                    sender_id = user_id,
                    room_id = room_id,
                    content = data["message"]
                )

                db.add(msg)
                db.commit()

                try:
                    await chat_manager.broadcast(room_id, {
                        "from": user_id,
                        "message": data["message"]
                    })
                except KeyError:
                    await websocket.send_json({
                        "error" : "room not found"
                    })
    except WebSocketDisconnect:
        chat_manager.disconnect(user_id)


    finally:
        db.close()