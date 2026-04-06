from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

class ConnectionManager():
    def __init__(self):
        self.active = {}
        self. rooms = {}

    async def connect(self, user_id, websocket: WebSocket):
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
        
chat = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    user_id = websocket.query_params.get("user")
    await chat.connect(user_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")

            data["from"] = user_id

            if action == "private":
                target = data.get("target")

                try: 
                    target_socket = chat.get_target_connection(target)
                    await target_socket.send_json({
                        "from": user_id,
                        "message": data["message"]
                    })
                except KeyError:
                    await websocket.send_json({"error": "recipient not connected"})
            
            elif action == "join":
                room_id = data.get("room_id")
                chat.join_room(room_id, user_id)

                await websocket.send_json({
                    "from": "system",
                    "message": f"Joined room {room_id}"
                })

            elif action == "send_room_message":

                room_id = data.get("room_id")

                if "message" not in data:
                    continue
                    
                try:
                    await chat.broadcast(room_id, {
                        "from": user_id,
                        "message": data["message"]
                    })
                except KeyError:
                    await websocket.send_json({
                        "error" : "room not found"
                    })
    except WebSocketDisconnect:
        chat.disconnect(user_id)