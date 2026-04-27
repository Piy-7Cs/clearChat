# clearChat
chat api built using python


Message format :
{
  "type": "message | room | history",
  "payload": {
    "chat_type": "room | private",
    "content": "...",
    "room_id": "...",
    "to": "..."
  }
}