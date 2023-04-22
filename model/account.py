from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from . import EmailStr, UserStatus


@dataclass
class Account(ABC):
    id: int
    email: EmailStr
    username: str
    password: bytes
    avatar: Optional[str] = "https://res.cloudinary.com/dmtnecr2n/image/upload/UserAvatar/DiscordDefaultAvatar.jpg"
    tag: Optional[str] = "0000"

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
    status: Optional[UserStatus] = UserStatus.online
    friends: Optional[list] = field(default_factory=list)
    notifications: Optional[list] = field(default_factory=list)

    def login(self):
        print("User login")

    def logout(self):
        print("User logout")

    @property
    def state(self):
        return self.status

    @state.setter
    def state(self, input: int):
        self.status = UserStatus(input)

    @property
    def profile_image(self):
        return self.avatar

    @profile_image.setter
    def profile_image(self, input: str):
        self.avatar = input

    def get_info(self):
        if self.avatar:
            return {'id': self.id, 'email': self.email, 'username': self.username, 'tag': self.tag, 'avatar': self.avatar, 'status': self.status}
