from model import AccountSystem, ServerSystem
from schema import UserSchema

discord_account = AccountSystem()
discord_server = ServerSystem()

## this is a mockup section
test_user1 = UserSchema(email="admin@mail.com", username="admin", password="1234")
test_user2 = UserSchema(email="admin@pic.com", username="admin", password="1234")
discord_account.add_user(test_user1)
discord_account.add_user(test_user2)
discord_account.set_avatar(test_user2.email, "static/assets/disquote.png")

test_server1 = discord_server.add_server("test_server1", 0, "static/assets/DiscordDefaultAvatar.jpg")
test_server2 = discord_server.add_server("test_server2", 0, "static/assets/member.png")
