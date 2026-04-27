from app.services.message_service import MessageService

async def handle_message(ws, db, user_id, data, chat_manager):

    payload = data["payload"]
    chat_type = payload.get("chat_type")

    if chat_type == "room":
        try: 
            msg = MessageService.send_room_message(
                db, user_id, payload.get("room"), payload.get("content")
            )
        
            await chat_manager.broadcast(payload.get("room"), {
                "type": "message",
                "chat_type": "room",
                "from": user_id,
                "content": msg.content
            })
        except ValueError as e:
            await ws.send_json({
                "type": "error",
                "message" : str(e)
            })

    elif chat_type == "private":

        try: 
            msg, target_user = MessageService.send_private_messgae(
                db, user_id, payload.get("to"), payload.get("content")
            )

            if target_user in chat_manager.active:
                await chat_manager.active[target_user].send_json(
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
        except ValueError as e:
            await ws.send_json({
                "type": "error",
                "message" : str(e)
            })