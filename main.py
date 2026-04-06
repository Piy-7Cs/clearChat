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
        

    def get_target_connection(self, target):
        if target in self.active:
            return self.active[target]
        else:
            raise KeyError("Recipient Not connected")


chat = ConnectionManager()






@app.websocket("/ws")
async def websocket_endpoint(websocket : WebSocket):
    user_id = websocket.query_params.get("user")
    await chat.connect(user_id, websocket)
    try :
        
        
         
        while True:
            data = await websocket.receive_json()
            print(data)
            target = data["target"]

            data["from"] = user_id
            try:
                target_socket = chat.get_target_connection(target)
                await target_socket.send_json(data)

            except KeyError:
                await websocket.send_json({"error": "recipient not connected", "target": target})
            

    except WebSocketDisconnect:
        chat.disconnect(user_id, websocket)
        print("client Disconnected")
        

        
