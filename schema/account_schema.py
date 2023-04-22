from typing import Optional
from pydantic import BaseModel, Field
from model import UserStatus, EmailStr

class AccountSchema(BaseModel):
    email: EmailStr
    username: str
    password: str
    avatar: Optional[str] = "https://res.cloudinary.com/dmtnecr2n/image/upload/UserAvatar/DiscordDefaultAvatar.jpg"

class UpdateAccountModel(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str]
    password: Optional[str]
    avatar: Optional[str]

class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    
class UserSchema(AccountSchema):
    #status: UserStatus = UserStatus.online
    pass

class UpdateUserModel(BaseModel):
    username: Optional[str]
    avatar: Optional[str]
    status: Optional[UserStatus]
    