from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.services.connection_manager import chat_manager


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
                target = data.get("target")

                target_user = db.query(User).filter(User.username == target).first()

                if not target_user:
                    await websocket.send_json({"error": "user not found"})
                    continue

                target_id = target_user.id

                msg = Message(
                    id = str(uuid.uuid4()),
                    sender_id = user_id,
                    recipient_id = target,
                    room_id = None,
                    content = data["message"]
                )

                db.add(msg)
                db.commit()


                sender = db.query(User).filter(User.id == msg.sender_id).first()


                try: 
                    target_socket = chat_manager.get_target_connection(target_id)
                    await target_socket.send_json({
                        "from": sender.username if sender else "Unknown",
                        "message": data["message"]
                    })
                except KeyError:
                    await websocket.send_json({"error": "recipient not connected"})
            


            elif action == "get_private_history":
                from sqlalchemy import or_, and_

                messages = db.query(Message).filter(
                    or_(
                        and_(
                                Message.sender_id == user_id,
                                Message.recipient_id == target
                            ),

                        and_(
                                Message.sender_id == target,
                                Message.recipient_id == user_id
                            )
                    )
                ).order_by(Message.created_at.desc()).all()
                    
                messages = list(reversed(messages))

                sender = db.query(User).filter(User.id == msg.sender_id).first()

                await websocket.send_json({
                    "type": "private_history",
                    "messages": [
                        {
                            "from": sender.username if sender else "Unknown",
                            "message": msg.content
                        } for msg in messages
                    ]
                })
                

            elif action == "join":

                room_id = data.get("room_id")
                chat_manager.join_room(room_id, user_id)

                await websocket.send_json({
                    "from": "system",
                    "message": f"Joined room {room_id}"
                })

                messages = db.query(Message).filter(
                    Message.room_id == room_id
                ).order_by(Message.created_at.desc()).all()

                messages = list(reversed(messages))

                sender = db.query(User).filter(User.id == msg.sender_id).first()

                await websocket.send_json(
                    {
                        "type": "history",
                        "messages": [
                            {
                                "from": sender.username if sender else "Unknown",
                                "message": msg.content
                            } for msg in messages
                        ]
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

                sender = db.query(User).filter(User.id == msg.sender_id).first()

                try:
                    await chat_manager.broadcast(room_id, {
                        "from": sender.username if sender else "unknown",
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