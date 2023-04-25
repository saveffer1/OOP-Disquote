from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from model import EmailStr, UserStatus


@dataclass
class Channel():
    id: int
    name: str
    type: str
    category: str
    _messages: Optional[list] = field(default_factory=list)

    def create_invite(self):
        pass

@dataclass
class Invite():
    id:int
    channel_list:list
    auther_id:int
    date_create:datetime