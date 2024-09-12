import uuid
from datetime import datetime

from pydantic import BaseModel
from typing import Union, Optional

from server.models.user import UserRole

class UserBase(BaseModel):
    id: Optional[str]
    full_name: Optional[str]
    photo_url: Optional[str]
    
    email: Optional[str]
    email_verified: Optional[bool] = False
    
    role: Optional[UserRole] = UserRole.member
    
    reward_credits: Optional[float]
    one_time_credits: Optional[float]
    recurring_credits: Optional[float]
    lifetime_deal_credits: Optional[float]
    

    created_date: Optional[datetime]
    last_signed_date: Optional[datetime]
    last_used_date: Optional[datetime]
    
    dial_number: Optional[uuid.UUID]

class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


# Session login
class Token(BaseModel):
    access_token: bytes
    token_type: str
    
class TokenData(BaseModel):
    username: Union[str, None] = None

class Login(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "t",
                "password": "t",
            }
        }