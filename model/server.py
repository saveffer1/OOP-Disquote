from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from .channel import TextChannel, VoiceChannel


@dataclass
class Invite():
    _server_id: int
    _server_name: str
    _code: str = None
    
    def generate_code(self):
        self._code = "INVITE-" + str(self._server_id) + str(self._server_name)
        return self._code
    
@dataclass
class Role():
    id: int
    name: str
    color: str
    permissions: list
    
@dataclass
class Server:
    _id: int
    _name: str
    _owner_id: int
    _image: Optional[str] = None
    _members: list[int] = field(default_factory=list)
    _channels: list[TextChannel, VoiceChannel] = field(default_factory=list)
    _invite_code: str = None
    # _roles: list[Role] = field(default_factory=list)
    _channel_id: int = 0
    # _role_id: int = 1
    
    def info(self) -> dict:
        return {"id": self._id, 
                "name": self._name, 
                "owner_id": self._owner_id,
                "image": self._image,
                "member": self.get_member_list(),
                "channel": self.get_channel_list(),
                "invite_code": self._invite_code
            }
    
    def id(self) -> int:
        return self._id
    
    def name(self) -> str:
        return self._name
    
    def owner_id(self) -> int:
        return self._owner_id
    
    def get_member_list(self) -> list[int]:
        return self._members
    
    def get_invite_code(self) -> str:
        return self._invite_code

    def add_invite(self) -> None:
        invite = Invite(self._id, self._name)
        self._invite_code = invite.generate_code()
    
    def add_member(self, member_id: int) -> None:
        if member_id not in self._members:
            self._members.append(member_id)

    def remove_member(self, member_id: int):
        if member_id in self._members:
            self._members.remove(member_id)

    def change_owner(self, user_id: int) -> None:
        self.owner_id = user_id

    def add_channel(self, name: str, type: str, category: str) -> None:
        if type == "text":
            self._channels.append(TextChannel(self._channel_id, name, type, category))
        elif type == "voice":
            self._channels.append(VoiceChannel(self._channel_id, name, type, category))
        self._channel_id += 1

    def remove_channel(self, channel_id: int) -> None:
        for channel in self._channels:
            if channel.id() == channel_id:
                self._channels.remove(channel)

    def get_channel_list(self) -> list[dict]:
        lst_ch = []
        for channel in self._channels:
            lst_ch.append(channel.info())
        return lst_ch
    
    def get_channel_by_id(self, channel_id: int) -> TextChannel | VoiceChannel | None:
        for channel in self._channels:
            if channel.id() == channel_id:
                return channel
        return None
    
    # def add_role(self, role: Role):
    #     self._roles.append(role)
    #     self._role_id += 1

    # def remove_role(self, role_id: int):
    #     for role in self._roles:
    #         if role.id == role_id:
    #             self._roles.remove(role)
