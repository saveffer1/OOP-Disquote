from dataclasses import dataclass, field
import bcrypt
from typing import Optional
from . import UserStatus, EmailStr
from . import User, Admin
from schema import AdminSchema, UserSchema, LoginSchema
from . import Server
from . import Announcement, Message


@dataclass
class AccountSystem():
    user_account: dict = field(default_factory=dict)
    admin_account: dict = field(default_factory=dict)
    user_id: int = 1
    admin_id: int = 1

    def get_user_list(self) -> list:
        return [user for user in self.user_account.values()]

    def get_admin_list(self) -> list:
        return [admin for admin in self.admin_account.values()]
    
    def get_user_account(self, email: EmailStr) -> User:
        return self.user_account[email]
    
    def get_user_id(self, email: EmailStr) -> int:
        return self.get_user_account(email).id

    def add_user(self, schema: UserSchema):
        """ register function add the user obj to user_account """
        if not self.user_account or schema.email not in self.user_account:
            hashed_password = bcrypt.hashpw(
                schema.password.encode('utf-8'), bcrypt.gensalt(5))
            if schema.username in [user.username for user in self.user_account.values()]:
                tag = max([int(user.tag)
                          for user in self.user_account.values()]) + 1
                tag = str(tag).zfill(4)
                account = User(self.user_id, schema.email, schema.username,
                               hashed_password, schema.avatar, tag=tag)
            else:
                account = User(self.user_id, schema.email,
                               schema.username, hashed_password, schema.avatar)
            self.user_account[schema.email] = account
            self.user_id += 1
            return True
        else:
            return False

    def add_admin(self, schema: AdminSchema):
        """ add admin to admin_account """
        if not self.admin_account or schema.email not in self.admin_account:
            account = Admin(self.admin_id, schema.email,
                            schema.username, schema.password.encode('utf-8'))
            self.admin_account[schema.email] = account
            self.admin_id += 1
            return True
        else:
            return False

    def check_password(self, input_password, check_password):
        """ function check the password """
        return bcrypt.checkpw(input_password.encode('utf-8'), check_password)

    def user_login(self, schema: LoginSchema) -> bool:
        """ login function check email and password in user_account """
        if not self.user_account:
            return False
        elif schema.email in self.user_account:
            is_login_pass = self.check_password(
                schema.password, self.get_user_account(schema.email).password
            )
            login_state = is_login_pass
            if is_login_pass:
                self.get_user_account(schema.email).login()
            return login_state
        else:
            return False

    def admin_login(self, schema: LoginSchema) -> bool:
        """ login function check email and password in admin_account """
        if not self.admin_account:
            return False
        elif schema.email in self.admin_account:
            is_login_pass = self.check_password(
                schema.password, self.get_user_account(schema.email).password
            )
            login_state = is_login_pass
            if is_login_pass:
                self.admin_account[schema.email].login()
            return login_state
        else:
            return False

    def get_status(self, email: EmailStr) -> UserStatus:
        """ get user status """
        return self.user_account[email].status

    def set_status(self, email: EmailStr, status: UserStatus):
        """ set user status """
        self.user_account[email].status = status

    def get_avatar(self, email: EmailStr) -> str:
        """ get user avatar """
        return self.user_account[email].avatar

    def set_avatar(self, email: EmailStr, avatar: str):
        """ set user avatar """
        self.user_account[email].avatar = avatar
    
    def get_username_by_id(self, user_id: int) -> str:
        """ get username by user id """
        for user in self.user_account.values():
            if user.id == user_id:
                return user.username
        return None
    
    def get_user_account_by_id (self, user_id: int) -> User:
        """ get user account by user id """
        for user in self.user_account.values():
            if user.id == user_id:
                return user
        return None
    
    def get_friend_list(self, email: EmailStr) -> dict:
        """ get user friend list """
        friends = dict()
        for friend_id in self.get_user_account(email).get_friend_list():
            friend_name = self.get_username_by_id(friend_id)
            friends[friend_id] = friend_name
        return friends

#-------------------------------- class -----------------------------------------------------------
    

@dataclass
class ServerSystem():
    servers: list = field(default_factory=list)
    server_id: int = 0

    def add_server(self, name: str, owner: int, image: str = None):
        """ add server to server_list """
        server = Server(self.server_id, name, owner, image)
        server.add_member(owner)
        server.add_channel("general", "text", "general")
        server.add_channel("general", "voice", "general")
        self.servers.append(server)
        self.server_id += 1

    def list_server(self, user_id: int):
        """ list of user server """
        server_list = []
        for server in self.servers:
            if user_id in server.member:
                server_list.append(server)
        return server_list

    def get_server_by_id(self, server_id: int) -> Server:
        """ get server instance by server id """
        for server in self.servers:
            if server.id == server_id:
                return server
        return self.servers
    
    def get_server_id(self):
        return self.server_id

#-------------------------------- class -----------------------------------------------------------

@dataclass
class AnnouceSystem():
    annouce_id: int = 0
    annouces: list = field(default_factory=list)
    
    def add_annoucement(self, title: str, content: str):
        """ add annouce to annouce_list """
        annouce = Announcement(self.annouce_id, title, content)
        self.annouces.append(annouce)
        self.annouce_id += 1

    def edit_annoucement(self, annouce_id: int, title: str, content: str):
        """ edit annouce from annouce_list """
        for annouce in self.annouces:
            if annouce.id == annouce_id:
                annouce.title = title
                annouce.content = content
                return True
        return False

    def del_annoucement(self, annouce_id: int):
        """ delete annouce from annouce_list """
        for annouce in self.annouces:
            if annouce.id == annouce_id:
                self.annouces.remove(annouce)
                return True
        return False
    
    def get_annouce(self):
        return self.annouces
    