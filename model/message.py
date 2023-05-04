from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Announcement:
    _id: int
    _title: str
    _content: str
    _date: datetime = field(default_factory=datetime.now)
    
    def info(self) -> dict:
        return {"id": self._id, "title": self._title, "content": self._content, "date": self._date}
    
    def id(self) -> int:
        return self._id
    
    @property
    def title(self) -> str:
        return self._title
    
    @title.setter
    def title(self, new_title: str) -> None:
        self._title = new_title
    
    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, new_content: str) -> None:
        self._content = new_content
    
    def date(self) -> datetime:
        return self._date

#-------------------------------------------------------------------------------------------
@dataclass 
class Message:
    _id: int
    _sender_id: int
    _content: str
    _date: datetime = field(default_factory=datetime.now)
    
    def info(self) -> dict:
        return {
            "id": self._id,
            "sender_id": self._sender_id,
            "content": self._content,
            "date": self._date.strftime("%m/%d/%Y %I:%M %p")
        }
    
    
# class D