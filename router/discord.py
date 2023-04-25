from model import AccountSystem, ServerSystem
from schema import UserSchema

discord_account = AccountSystem()
discord_server = ServerSystem()

## this is a mockup section
test_user = UserSchema(email="admin@mail.com", username="admin", password="1234")
discord_account.add_user(test_user)
