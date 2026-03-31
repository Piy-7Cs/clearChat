from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

app = FastAPI()





class ConnectionManager():
    def __init__(self):
        self.active ={}

    async def connect(self, user_id, websocket: WebSocket):
        await websocket.accept()
        self.active[user_id] = websocket

    def disconnect(self, user_id,  websocket: WebSocket):
        self.active.pop(user_id, None)

    async def send_message(self, user_id,message:str):
        if user_id in self.active:
            await self.active[user_id].send_text(message)


chat = ConnectionManager()


 



@app.websocket("/ws")
async def websocket_endpoint(websocket : WebSocket):
    user_id = websocket.query_params.get("user")
    await chat.connect(user_id, websocket)

    try :

        while True:
            data = await websocket.receive_text()
            target, msg = data.split(":")

            await chat.send_message(target.strip(), msg)

    except WebSocketDisconnect:
        print("client Disconnected")
        

        
