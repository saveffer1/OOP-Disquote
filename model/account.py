from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from . import EmailStr, UserStatus


@dataclass
class Account(ABC):
    _id: int
    _email: EmailStr
    _username: str
    _password: bytes
    _avatar: Optional[str] = "default"
    _tag: Optional[str] = "0000"

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def logout(self):
        pass

    # def change_avatar(self, avatar: Image):
    #     self.avatar = avatar.upload_image()


@dataclass
class Admin(Account):
    def login(self):
        print("Admin login")

    def logout(self):
        print("Admin logout")


@dataclass
class User(Account):
    _status: Optional[UserStatus] = UserStatus.online
    _friends: Optional[list] = field(default_factory=list)
    _friends_request: Optional[list] = field(default_factory=list)

    def login(self):
        print("User login")

    def logout(self):
        print("User logout")
    
    def id(self) -> int:
        return self._id
    
    def username(self) -> str:
        return self._username
    
    def tag(self) -> str:
        return self._tag
    
    def get_hashed_password(self) -> str:
        return self._password

    @property
    def state(self):
        return self._status

    @state.setter
    def state(self, input: int):
        self._status = UserStatus(input)

    @property
    def profile_image(self):
        return self._avatar

    @profile_image.setter
    def profile_image(self, input: str):
        self._avatar = input

    def get_friend_list(self):
        return self._friends

    def unfriend(self, id: int):
        self._friends.remove(id)
    
    @property
    def request_list(self):
        return self._friends_request

    @request_list.setter
    def request_list(self, id: int, accept: bool):
        if accept:
            self._friends.append(id)
        self._friends_request.remove(id)
    
    def add_request(self, id: int):
        self._friends_request.append(id)
    
    def info(self):
        return {"id": self._id, "username": self._username, "tag": self._tag, "avatar": self._avatar, "status": self._status.value} 