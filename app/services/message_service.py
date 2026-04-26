from app.models.message import Message
from app.models.user import User
from app.services.room_service import RoomService
import uuid
from sqlalchemy import or_ , and_

class MessageService:

    @staticmethod
    def send_private_messgae(db, sender_id, target_username, content):

        if not content:
            raise ValueError("empty error")
        
        sender = db.query(User).filter(User.username == sender_id).first()
        
        target_user = db.query(User).filter(User.username == target_username).first()
        if not target_user:
            raise ValueError("User Not found")

        if target_user.id == sender_id:
            raise ValueError("cannot Message Yourself")
        
        msg = Message(
            id=str(uuid.uuid4()),
            sender_id=sender_id,
            recipient_id= target_user.id,
            content=content
        )
        db.add(msg)
        db.commit()

        return msg, target_user.id
    
    

    @staticmethod
    def get_private_history(db, user_id, target_username):
        
        target_user = db.query(User).filter(User.username == target_username).first()

        if not target_user:
            raise ValueError("User Not Found")

        if target_user.id == user_id:
            raise ValueError("cannot fetch self chat")

        messages = db.query(Message).filter(
            or_(
                and_(Message.sender_id == user_id, Message.recipient_id == target_user.id),

                and_(Message.sender_id == target_user.id, Message.recipient_id == user_id)
            )

        ).order_by(Message.created_at.desc()).all()

        return list(reversed(messages))
    

    @staticmethod
    def get_room_history(db, room_id):

        messages = db.query(Message).filter(
            Message.room_id == room_id
        ).order_by(Message.created_at.desc()).all()

        return list(reversed(messages))



    @staticmethod
    def send_room_message(db, user_id, room_id, content):

        if not content:
            raise ValueError("Empty Messages")
        
        if not RoomService.is_member(db, user_id, room_id):
            raise ValueError("Not a Member of this room"
                             )
        msg = Message(
                    id = str(uuid.uuid4()),
                    sender_id = user_id,
                    room_id = room_id,
                    content = content
                )


        db.add(msg)
        db.commit()

        return msg