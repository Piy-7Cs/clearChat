from fastapi import FastAPI
from app.api.websocket import router as websocket_router
from app.db.session import engine
from app.db.base import Base
from app.api.auth import router as auth_router





import app.models.user
import app.models.room
import app.models.message

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(websocket_router)
app.include_router(auth_router)



