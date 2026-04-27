from app.services.message_service import MessageService
from app.services.room_service import RoomService

async def handle_join(ws, db, user_id, data, chat_manager):
    
    room_name = data["payload"]["room"]
     
    room = RoomService.join_room(db, user_id, room_name)

    chat_manager.join_room(room.id, user_id)

    messages = MessageService.get_room_history(db, room.id)

    await ws.send_json({
        "type": "system",
        "message": f"joined {room.name}"
    })

    await ws.send_json({
        "type": "history",
        "chat_type": "room",
        "messages": [
            {"from": msg.sender_id, "content": msg.content}
            for msg in messages
        ]
    })