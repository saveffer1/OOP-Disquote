from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from .channel import Channel, Invite


@dataclass
class Role():
    id: int
    name: str
    color: str
    permissions: list
    
@dataclass
class Server:
    id: int
    name: str
    owner_id: int
    image: Optional[str] = None
    member: list[int] = field(default_factory=list)
    channels: list[Channel] = field(default_factory=list)
    invite_code: Optional[Invite] = None
    roles: list[Role] = field(default_factory=list)
    channel_id: int = 1
    role_id: int = 1

    def add_member(self, user_id: int):
        if user_id not in self.member:
            self.member.append(user_id)

    def remove_member(self, user_id: int):
        if user_id in self.member:
            self.member.remove(user_id)

    def change_owner(self, user_id: int):
        self.owner_id = user_id

    def add_channel(self, name: str, type: str, category: str):
        self.channels.append(Channel(self.channel_id, name, type, category))
        self.channel_id += 1

    def remove_channel(self, channel_id: int):
        for channel in self.channels:
            if channel.id == channel_id:
                self.channels.remove(channel)

    def add_role(self, role: Role):
        self.roles.append(role)
        self.role_id += 1

    def remove_role(self, role_id: int):
        for role in self.roles:
            if role.id == role_id:
                self.roles.remove(role)
