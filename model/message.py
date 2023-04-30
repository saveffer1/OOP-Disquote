from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass
class Announcement:
    id: int
    title: str
    content: str
    date: datetime = field(default_factory=datetime.now)

#-------------------------------- class -----------------------------------------------------------
@dataclass 
class Message:
    sender_id: int
    content: str
    date: datetime = field(default_factory=datetime.now)
    
# class DM