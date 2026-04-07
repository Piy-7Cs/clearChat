from fastapi import WebSocket


class ConnectionManager():
    def __init__(self):
        self.active = {}
        self. rooms = {}



    async def connect(self, user_id, websocket: WebSocket):
        if user_id in self.active:
            await self.active[user_id].close()

        await websocket.accept()
        self.active[user_id] = websocket



    def disconnect(self, user_id):
        self.active.pop(user_id, None)

        for room in self.rooms.values():
            room.discard(user_id)



    def join_room(self, room_id, user_id):
        if room_id not in self.rooms:
            self.rooms[room_id] = set()
        self.rooms[room_id].add(user_id)
    


    async def broadcast(self, room_id, message):
        if room_id not in self.rooms:
            raise KeyError("Room Not found")
        
        for user in self.rooms[room_id]:
            if user in self.active:
                await self.active[user].send_json(message)



    def get_target_connection(self, target):
        if target in self.active:
            return self.active[target]
        else:
            raise KeyError("Recipient Not Connected")



chat_manager = ConnectionManager()
