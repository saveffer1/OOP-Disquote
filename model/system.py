from dataclasses import dataclass, field
import bcrypt
from typing import Optional
from . import UserStatus, EmailStr
from . import User, Admin
from . import Server, Invite
from . import Announcement
from . import TextChannel, VoiceChannel

@dataclass
class AccountSystem():
    _user_account: dict = field(default_factory=dict)
    _admin_account: dict = field(default_factory=dict)
    _user_id: int = 0
    _admin_id: int = 0
    
    def systeminfo(self) -> dict:
        user_count = len(self._user_account)
        admin_count = len(self._admin_account)
        return {"User": user_count, "Admin": admin_count, "last_user_id": self._user_id, "last_admin_id": self._admin_id}

    def get_user_list(self) -> list:
        return [user for user in self._user_account.values()]

    def get_admin_list(self) -> list:
        return [admin for admin in self._admin_account.values()]
    
    def get_user_account(self, email: EmailStr) -> User | None:
        if self._user_account.get(email):
            return self._user_account[email]
    
    def get_user_id(self, email: EmailStr) -> int:
        account = self.get_user_account(email)
        return account.id()

    def add_user(self, email, username, password, avatar='default'):
        """ register function add the user obj to user_account """
        if not self._user_account or email not in self._user_account:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(5))
            if username in [user.username() for user in self._user_account.values()]:
                tag = max([int(user.tag()) for user in self._user_account.values()]) + 1
                tag = str(tag).zfill(4)
                account = User(self._user_id, email, username, hashed_password, avatar, _tag=tag)
            else:
                account = User(self._user_id, email, username, hashed_password, avatar)
            self._user_account[email] = account
            self._user_id += 1
            return True
        else:
            return False
    
    def email_is_exist(self, email: EmailStr) -> bool:
        """ check email is exist """
        if email in self._user_account:
            return True
        else:
            return False

    def add_admin(self, email, username, password):
        """ add admin to admin_account """
        if not self._admin_account or email not in self._admin_account:
            account = Admin(self._admin_id, email, username, password.encode('utf-8'))
            self._admin_account[email] = account
            self._admin_id += 1
            return True
        else:
            return False

    #protected method
    def _check_password(self, input_password, check_password):
        """ function check the password """
        return bcrypt.checkpw(input_password.encode('utf-8'), check_password)

    def user_login(self, email, password) -> bool:
        """ login function check email and password in user_account """
        if not self._user_account:
            return False
        elif email in self._user_account:
            account = self.get_user_account(email)
            is_login_pass = self._check_password(password, account.get_hashed_password())
            login_state = is_login_pass
            if is_login_pass:
                account.login()
            return login_state
        else:
            return False

    def admin_login(self, email, password) -> bool:
        """ login function check email and password in admin_account """
        if not self._admin_account:
            return False
        elif email in self._admin_account:
            account = self.get_user_account(email)
            is_login_pass = self._check_password(password, account.get_hashed_password())
            login_state = is_login_pass
            if is_login_pass:
                account.login()
            return login_state
        else:
            return False

    def get_status(self, email: EmailStr) -> UserStatus:
        """ get user status """
        return self.get_user_account(email).state()

    def set_status(self, email: EmailStr, status: UserStatus):
        """ set user status """
        account = self.get_user_account(email)
        account.state(status)

    def get_avatar(self, email: EmailStr) -> str:
        """ get user avatar """
        account = self.get_user_account(email)
        return account.profile_image()

    def set_avatar(self, email: EmailStr, avatar: str):
        """ set user avatar """
        account = self.get_user_account(email)
        account.profile_image(avatar)
    
    def get_username_by_id(self, user_id: int) -> str:
        """ get username by user id """
        for user in self._user_account.values():
            if user.id() == user_id:
                return user.username()
        return None
    
    def get_user_account_by_id (self, user_id: int) -> User | None:
        """ get user account by user id """
        for user in self._user_account.values():
            if user.id() == user_id:
                return user
        return None
    
    def get_user_account_by_name_and_tag(self, username: str, tag: str) -> User | None:
        """ get user account by username and tag """
        tag = tag.split('#')[-1]
        for user in self._user_account.values():
            if user.username() == username and user.tag() == tag:
                return user
        return None
    
    def get_user_friend_list(self, email: EmailStr) -> list:
        """ get user friend list """
        account = self.get_user_account(email)
        return account.get_friend_list()

#-------------------------------------------------------------------------------------------

@dataclass
class ServerSystem():
    _servers: list = field(default_factory=list)
    _server_id: int = 0
    
    def get_all_invite(self) -> list[str]:
        for server in self.get_all_server():
            yield server.get_invite_code()
    
    def get_all_server(self) -> list[Server]:
        """ get all server """
        return self._servers

    def get_user_server_list(self, member_id: int) -> list:
        """ list of user server """
        for server in self.get_all_server():
            if member_id in server.get_member_list():
                yield server.info()

    def get_server_by_id(self, server_id: int) -> Server | None:
        """ get server instance by server id """
        for server in self.get_all_server():
            if server.id() == server_id:
                return server
        return None
    
    def get_member_server_list(self, server_id: int) -> list:
        """ get member in server """
        server = self.get_server_by_id(server_id)
        if server:
            return server.get_member_list()           
        
    def member_in_server(self, server_id: int, member_id: int) -> bool:
        """ check member in server """
        server = self.get_server_by_id(server_id)
        if member_id in server.get_member_list():
            return True
        return False
    
    def get_server_id(self) -> int:
        return self._server_id
    
    def add_server(self, name: str, owner: int, image: str = None):
        """ add server to server_list """
        server = Server(self._server_id, name, owner, image)
        server.add_member(owner)
        server.add_channel("textchat", "text", "general")
        server.add_channel("voicechat", "voice", "general")
        server.add_invite()
        self._servers.append(server)
        self._server_id += 1
    
    def del_server(self, server_id: int) -> bool:
        """ delete server from server_list """
        for server in self.get_all_server():
            if server.id() == server_id:
                self._servers.remove(server)
                return True
        return False

    def get_server_id_by_invite(self, invite_code: str) -> int:
        """ get server id by invite code """
        for server in self.get_all_server():
            if server.get_invite_code() == invite_code:
                return server.id()
        return None
    
    def join_server(self, server_id: int, user_id: int) -> bool:
        """ join server """
        server = self.get_server_by_id(server_id)
        print("here")
        if server:
            server.add_member(user_id)
            print("added")
            print(server.get_member_list())
            return True
        else:
            print("not added")
            return False
    
    def leave_server(self, server_id: int, user_id: int) -> bool:
        """ leave server """
        server = self.get_server_by_id(server_id)
        if server:
            server.remove_member(user_id)
            return True
        else:
            return False

    def add_channel(self, server_id: int, name: str, type: str, category: str = None) -> bool:
        """ add channel to server """
        server = self.get_server_by_id(server_id)
        if server:
            if not category:
                category = "general"
            server.add_channel(name, type, category)
            return True
        else:
            return False
    
    def _channel_manager(self, sv_id: int, ch_id: int) -> TextChannel | VoiceChannel | None:
        server = self.get_server_by_id(sv_id)
        if server:
            channel = server.get_channel_by_id(ch_id)
            return channel
        return None
    
    def add_message(self, sv_id: int, ch_id: int, user_id: int, content: str) -> bool:
        channel = self._channel_manager(sv_id, ch_id)
        if channel:
            added_msg = channel.add_message(user_id, content)
            if added_msg:
                return True
            else:
                return False
        else:
            return False
    
    def del_message(self, sv_id: int, ch_id: int, msg_id: int) -> bool:
        channel = self._channel_manager(sv_id, ch_id)
        if channel:
            deleted_msg = channel.del_message(msg_id)
            if deleted_msg:
                return True
            else:
                return False
        else:
            return False
        
    def get_msg_list(self, sv_id: int, ch_id: int) -> list | None:
        channel = self._channel_manager(sv_id, ch_id)
        if channel:
            return channel.get_messages()
        else:
            return None

#-------------------------------------------------------------------------------------------

@dataclass
class AnnouceSystem():
    _annouce_id: int = 0
    _annouces: list = field(default_factory=list)

    def add_annoucement(self, title: str, content: str):
        """ add annouce to annouce_list """
        annouce = Announcement(self._annouce_id, title, content)
        self._annouces.append(annouce)
        self._annouce_id += 1

    def edit_annoucement(self, annouce_id: int, title: str, content: str):
        """ edit annouce from annouce_list """
        for annouce in self.get_annouce():
            if annouce.id() == annouce_id:
                annouce.title(title)
                annouce.content(content)
                return True
        return False

    def del_annoucement(self, annouce_id: int):
        """ delete annouce from annouce_list """
        for annouce in self.get_annouce():
            if annouce.id() == annouce_id:
                self._annouces.remove(annouce)
                return True
        return False

    def get_annouce(self) -> list[Announcement]:
        for annouce in self._annouces:
            yield annouce.info()
