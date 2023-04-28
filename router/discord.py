from model import AccountSystem, ServerSystem, AnnouceSystem
from schema import UserSchema
import random

discord_account = AccountSystem()
discord_server = ServerSystem()
system_annoucer = AnnouceSystem()

## this is a mockup section
test_admin1 = UserSchema(email="admin@mail.com", username="admin", password="1234")
test_user1 = UserSchema(email="admin@mail.com", username="admin", password="1234")
test_user2 = UserSchema(email="admin@pic.com", username="admin", password="1234")
discord_account.add_admin(test_admin1)
discord_account.add_user(test_user1)
discord_account.add_user(test_user2)
discord_account.set_avatar(test_user2.email, "static/assets/disquote.png")

test_server1 = discord_server.add_server("test_server1", 1, "/static/assets/DiscordDefaultAvatar.jpg")
test_server2 = discord_server.add_server("test_server2", 1, "/static/assets/member.png")

pic_choic = ["/static/assets/DiscordDefaultAvatar.jpg", "/static/assets/member.png", "/static/assets/disquote.png"]
for i in range(15):
    discord_server.add_server(f"test_server{i}", 1, random.choice(pic_choic))

system_annoucer.add_annoucement("test_server1", "test_annoucement1")