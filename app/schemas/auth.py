from pydantic import BaseModel, EmailStr, field_validator

class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


    @field_validator("username")
    @classmethod
    def username_not_empty(cls, v):
        v = v.strip()

        if not v:
            raise ValueError("Username Cannot be Empty")
        
        if len(v) < 3:
            raise ValueError("Username too short")
        
        return v

class LoginRequest(BaseModel):
    identifier: str
    password: str