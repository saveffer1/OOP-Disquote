from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from abc import ABC, abstractmethod
from model import EmailStr, UserStatus
from .message import Message

@dataclass
class Channel(ABC):
    _id: int
    _name: str
    _type: str
    _category: str
    
    @abstractmethod
    def info(self) -> dict:
        return {
            "id": self._id,
            "name": self._name,
            "type": self._type,
            "category": self._category,
        }
    
    @abstractmethod
    def id(self) -> int:
        return self._id

    def name(self) -> str:
        return self._name
    
    def type(self) -> str:
        return self._type
    
    def category(self) -> str:
        return self._category
    
@dataclass
class TextChannel(Channel):
    _id: int
    _name: str
    _type: str = "text"
    _category: str = "general"
    _messages: Optional[list] = field(default_factory=list)
    _msg_id: int = 0
    
    def info(self) -> dict:
        return {
            "id": self._id,
            "name": self._name,
            "type": self._type,
            "category": self._category,
            "messages": self.get_messages()
        }
    
    def id(self) -> int:
        return self._id
    
    def msg_id(self) -> int:
        return self._msg_id

    def get_messages(self) -> list:
        all_messages = []
        for message in self._messages:
            all_messages.append(message.info())
        return all_messages

    def add_message(self, sender_id: int, message: str) -> bool:
        try:
            self._messages.append(Message(self._msg_id, sender_id, message))
            self._msg_id += 1
            return True
        except:
            return False

    def remove_message(self, msg_id: int) -> bool:
        try:
            for message in self._messages:
                if message.id() == msg_id:
                    self._messages.remove(message)
            return True
        except:
            return False

@dataclass
class VoiceChannel(Channel):
    _id: int
    _type: str = "voice"
    _category: str = "general"
    
    def info(self) -> dict:
        return {
            "id": self._id,
            "name": self._name,
            "type": self._type,
            "category": self._category,
        }
    
    def id(self) -> int:
        return self._id
    
    
