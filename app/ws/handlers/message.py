from app.services.message_service import MessageService

async def handle_message(ws, db, user_id, data, chat_manager):

    payload = data["payload"]
    chat_type = payload.get("chat_type")

    if chat_type == "room":
        msg = MessageService.send_room_message(
            db, user_id, payload.get("room"), payload.get("content")
        )
    
        await chat_manager.broadcast(payload.get("room"), {
            "type": "message",
            "chat_type": "room",
            "from": user_id,
            "content": msg.content
        })

    elif chat_type == "private":
        msg, target_user = MessageService.send_private_messgae(
            db, user_id, payload.get("to"), payload.get("content")
        )

        if target_user.id in chat_manager.active:
            await chat_manager.active[target_user.id].send_json(
                {
                "type": "message",
                "chat_type": "private",
                "from": user_id,
                "content": msg.content
                }
            )
        

        await ws.send_json({
            "type": "message",
            "chat_type": "private",
            "from": user_id,
            "content": msg.content
        })