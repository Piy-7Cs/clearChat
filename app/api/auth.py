from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.auth import SignupRequest, LoginRequest
from sqlalchemy import or_, and_

import uuid

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup")
def signup(data: SignupRequest):
    
    db: Session = SessionLocal()


    existing = db.query(User).filter(User.user_email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User Email Already Exists")
    try : 
        user = User(
            id= str(uuid.uuid4()),
            username = data.username,
            user_email = data.email,
            hashed_password = hash_password(data.password)
        )

        db.add(user)
        db.commit()

        return {"message" : "User Registered Successfully"}
    except Exception as e:
        return {"message" : str(e)}

@router.post("/login")
def login(data: LoginRequest):
    db: Session = SessionLocal()

    user = db.query(User).filter(   or_(User.user_email == data.identifier,
                                        User.username == data.identifier)
                                ).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    token = create_access_token({"sub": user.id})

    return {"access_token": token}