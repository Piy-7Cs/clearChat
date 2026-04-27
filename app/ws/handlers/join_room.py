from app.services.message_service import MessageService
from app.services.room_service import RoomService

async def handle_join(ws, db, user_id, data, chat_manager):
    
    room_id = data["payload"]["room_id"]
    room_name = data["payload"]["room_name"]


    if not RoomService.is_member(db, user_id, room_id):
        await ws.send_json({
            "type": "error",
            "message" : "Not a member of this rooms"
        })

        return 
    
    try: 
        chat_manager.join_room(room_id, user_id)

        messages = MessageService.get_room_history(db, room_id)

        await ws.send_json({
            "type": "system",
            "message": f"joined {room_name}"
        })

        await ws.send_json({
            "type": "history",
            "chat_type": "room",
            "messages": [
                {"from": msg.sender_id, "content": msg.content}
                for msg in messages
            ]
        })
    except ValueError as e:
        await ws.send_json({
            "type": "error",
            "message" : str(e)
        })