from app.services.message_service import MessageService

async def handle_history(ws, db, user_id, data, chat_manager):
    
    payload = data["payload"]

    if payload.get("chat_type") == "private":

        try:
            messages = MessageService.get_private_history(
                db, user_id, payload.get("with"),  
                )
            
            if messages:
            
                await ws.send_json({
                    "type": "history",
                    "chat_type": "private",
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