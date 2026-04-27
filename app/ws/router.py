from app.ws.handlers.history import handle_history
from app.ws.handlers.message import handle_message
from app.ws.handlers.join_room import handle_join


handlers = {
    "message" : handle_message,
    "join": handle_join,
    "history": handle_history,
}