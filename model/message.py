from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass
class Announcement:
    id: int
    title: str
    content: str
    date: datetime = field(default_factory=datetime.now)

@dataclass 
class Message:
    pass