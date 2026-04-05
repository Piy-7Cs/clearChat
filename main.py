from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

app = FastAPI()





class ConnectionManager():
    def __init__(self):
        self.active ={}
        
    


    async def connect(self, user_id, websocket: WebSocket):
        await websocket.accept()
        
        self.active[user_id] = websocket

    def disconnect(self, user_id, websocket: WebSocket):
        self.active.pop(user_id, None)
        

    async def send_message(self, user_id, target, message:str):
        if target in self.active:
            await self.active[target].send_json(message)
        else:
            raise KeyError("Recipient Not connected")


chat = ConnectionManager()






@app.websocket("/ws")
async def websocket_endpoint(websocket : WebSocket):
    user_id = websocket.query_params.get("user")
    target = websocket.query_params.get("target")
    await chat.connect(user_id, websocket)
    try :

        while True:
            data = await websocket.receive_text()
            message = {
                "user" : user_id,
                "target" : target,
                "message" : data
            }
            await chat.send_message(user_id, target, message)

    except WebSocketDisconnect:
        chat.disconnect(user_id, target, websocket)
        print("client Disconnected")
        

        
