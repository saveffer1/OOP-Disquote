from model import AccountSystem, ServerSystem, AnnouceSystem
import random
import shutil
import os

discord_account = AccountSystem()
discord_server = ServerSystem()
system_annoucer = AnnouceSystem()

## this is a mockup section use for testing

# admin account
discord_account.add_admin(email="admin@mail.com", username="admin", password="1234")

# user account
discord_account.add_user(email="admin@mail.com", username="admin", password="1234") #0
discord_account.add_user(email="admin@min.com", username="HIW", password="1234") #1
discord_account.add_user(email="theway@mail.com", username="theway", password="1234") #2
discord_account.add_user(email="todie@mail.com", username="todie", password="1234") #3

# get user account by email
hiw = discord_account.get_user_account(email="admin@mail.com")
theway = discord_account.get_user_account(email="theway@mail.com")
todie = discord_account.get_user_account(email="todie@mail.com")

# set user account status
hiw.state = 1 # online
theway.state = 2 # idle
todie.state = 3 # offline

# add friend section add to admin@mail.com
discord_account.get_user_account("admin@mail.com").add_request(1)
discord_account.get_user_account("admin@mail.com").add_request(2)
discord_account.get_user_account("admin@mail.com").add_request(3)
# duplicate add friend request test
discord_account.get_user_account("admin@mail.com").add_request(1)

# create server section
test_server1 = discord_server.add_server("test_server1", 1, "default")
test_server2 = discord_server.add_server("test_server2", 1, "default")

# random image for server and create server
images = ['1.png', '2.png']
for i in range(5):
    discord_server.add_server(f"test_server{i}", 0, random.choice(images))

# annouce mockup
system_annoucer.add_annoucement("test_server1", "test_annoucement1")
system_annoucer.add_annoucement("test annoucement 2", """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                                In the above code snippet, the dom option specifies the layout of the DataTables 
                                elements. The lfr options stand for length changing input control, the table, and 
                                filtering input control, respectively. The "thead-dark" option specifies a custom 
                                class for the thead element of the DataTable. The "bottom"ip option specifies the 
                                positioning of the table information and pagination control elements at the bottom of 
                                the table.test annoucement 2 Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                                In the above code snippet, the dom option specifies the layout of the DataTables
                                elements. The lfr options stand for length changing input control, the table, and
                                filtering input control, respectively. The "thead-dark" option specifies a custom
                                class for the thead element of the DataTable. The "bottom"ip option specifies the
                                In the above code snippet, the dom option specifies the layout of the DataTables 
                                elements. The lfr options stand for length changing input control, the table, and 
                                filtering input control, respectively. The "thead-dark" option specifies a custom 
                                class for the thead element of the DataTable. The "bottom"ip option specifies the 
                                positioning of the table information and pagination control elements at the bottom of 
                                the table.test annoucement 2 Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                                In the above code snippet, the dom option specifies the layout of the DataTables
                                elements. The lfr options stand for length changing input control, the table, and
                                filtering input control, respectively. The "thead-dark" option specifies a custom
                                class for the thead element of the DataTable. The "bottom"ip option specifies the
                                In the above code snippet, the dom option specifies the layout of the DataTables 
                                elements. The lfr options stand for length changing input control, the table, and 
                                filtering input control, respectively. The "thead-dark" option specifies a custom 
                                class for the thead element of the DataTable. The "bottom"ip option specifies the 
                                positioning of the table information and pagination control elements at the bottom of 
                                the table.test annoucement 2 Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                                In the above code snippet, the dom option specifies the layout of the DataTables
                                elements. The lfr options stand for length changing input control, the table, and
                                filtering input control, respectively. The "thead-dark" option specifies a custom
                                class for the thead element of the DataTable. The "bottom"ip option specifies the
                                In the above code snippet, the dom option specifies the layout of the DataTables 
                                elements. The lfr options stand for length changing input control, the table, and 
                                filtering input control, respectively. The "thead-dark" option specifies a custom 
                                class for the thead element of the DataTable. The "bottom"ip option specifies the 
                                positioning of the table information and pagination control elements at the bottom of 
                                the table.test annoucement 2 Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                                In the above code snippet, the dom option specifies the layout of the DataTables
                                elements. The lfr options stand for length changing input control, the table, and
                                filtering input control, respectively. The "thead-dark" option specifies a custom
                                class for the thead element of the DataTable. The "bottom"ip option specifies the
                                In the above code snippet, the dom option specifies the layout of the DataTables 
                                elements. The lfr options stand for length changing input control, the table, and 
                                filtering input control, respectively. The "thead-dark" option specifies a custom 
                                class for the thead element of the DataTable. The "bottom"ip option specifies the 
                                positioning of the table information and pagination control elements at the bottom of 
                                the table.test annoucement 2 Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                                In the above code snippet, the dom option specifies the layout of the DataTables
                                elements. The lfr options stand for length changing input control, the table, and
                                filtering input control, respectively. The "thead-dark" option specifies a custom
                                class for the thead element of the DataTable. The "bottom"ip option specifies the
                                In the above code snippet, the dom option specifies the layout of the DataTables 
                                elements. The lfr options stand for length changing input control, the table, and 
                                filtering input control, respectively. The "thead-dark" option specifies a custom 
                                class for the thead element of the DataTable. The "bottom"ip option specifies the 
                                positioning of the table information and pagination control elements at the bottom of 
                                the table.test annoucement 2 Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                                In the above code snippet, the dom option specifies the layout of the DataTables
                                elements. The lfr options stand for length changing input control, the table, and
                                filtering input control, respectively. The "thead-dark" option specifies a custom
                                class for the thead element of the DataTable. The "bottom"ip option specifies the
                                In the above code snippet, the dom option specifies the layout of the DataTables 
                                elements. The lfr options stand for length changing input control, the table, and 
                                filtering input control, respectively. The "thead-dark" option specifies a custom 
                                class for the thead element of the DataTable. The "bottom"ip option specifies the 
                                positioning of the table information and pagination control elements at the bottom of 
                                the table.test annoucement 2 Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                                In the above code snippet, the dom option specifies the layout of the DataTables
                                elements. The lfr options stand for length changing input control, the table, and
                                filtering input control, respectively. The "thead-dark" option specifies a custom
                                class for the thead element of the DataTable. The "bottom"ip option specifies the
                                In the above code snippet, the dom option specifies the layout of the DataTables 
                                elements. The lfr options stand for length changing input control, the table, and 
                                filtering input control, respectively. The "thead-dark" option specifies a custom 
                                class for the thead element of the DataTable. The "bottom"ip option specifies the 
                                positioning of the table information and pagination control elements at the bottom of 
                                the table.test annoucement 2 Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                                In the above code snippet, the dom option specifies the layout of the DataTables
                                elements. The lfr options stand for length changing input control, the table, and
                                filtering input control, respectively. The "thead-dark" option specifies a custom
                                class for the thead element of the DataTable. The "bottom"ip option specifies the
                                In the above code snippet, the dom option specifies the layout of the DataTables 
                                elements. The lfr options stand for length changing input control, the table, and 
                                filtering input control, respectively. The "thead-dark" option specifies a custom 
                                class for the thead element of the DataTable. The "bottom"ip option specifies the 
                                positioning of the table information and pagination control elements at the bottom of 
                                the table.test annoucement 2 Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                                In the above code snippet, the dom option specifies the layout of the DataTables
                                elements. The lfr options stand for length changing input control, the table, and
                                filtering input control, respectively. The "thead-dark" option specifies a custom
                                class for the thead element of the DataTable. The "bottom"ip option specifies the
                                In the above code snippet, the dom option specifies the layout of the DataTables 
                                elements. The lfr options stand for length changing input control, the table, and 
                                filtering input control, respectively. The "thead-dark" option specifies a custom 
                                class for the thead element of the DataTable. The "bottom"ip option specifies the 
                                positioning of the table information and pagination control elements at the bottom of 
                                the table.test annoucement 2 Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                                In the above code snippet, the dom option specifies the layout of the DataTables
                                elements. The lfr options stand for length changing input control, the table, and
                                filtering input control, respectively. The "thead-dark" option specifies a custom
                                class for the thead element of the DataTable. The "bottom"ip option specifies the
                                In the above code snippet, the dom option specifies the layout of the DataTables 
                                elements. The lfr options stand for length changing input control, the table, and 
                                filtering input control, respectively. The "thead-dark" option specifies a custom 
                                class for the thead element of the DataTable. The "bottom"ip option specifies the 
                                positioning of the table information and pagination control elements at the bottom of 
                                the table.test annoucement 2 Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                                In the above code snippet, the dom option specifies the layout of the DataTables
                                elements. The lfr options stand for length changing input control, the table, and
                                filtering input control, respectively. The "thead-dark" option specifies a custom
                                class for the thead element of the DataTable. The "bottom"ip option specifies the
                                In the above code snippet, the dom option specifies the layout of the DataTables 
                                elements. The lfr options stand for length changing input control, the table, and 
                                filtering input control, respectively. The "thead-dark" option specifies a custom 
                                class for the thead element of the DataTable. The "bottom"ip option specifies the 
                                positioning of the table information and pagination control elements at the bottom of 
                                the table.test annoucement 2 Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                                In the above code snippet, the dom option specifies the layout of the DataTables
                                elements. The lfr options stand for length changing input control, the table, and
                                filtering input control, respectively. The "thead-dark" option specifies a custom
                                class for the thead element of the DataTable. The "bottom"ip option specifies the
                                In the above code snippet, the dom option specifies the layout of the DataTables 
                                elements. The lfr options stand for length changing input control, the table, and 
                                filtering input control, respectively. The "thead-dark" option specifies a custom 
                                class for the thead element of the DataTable. The "bottom"ip option specifies the 
                                positioning of the table information and pagination control elements at the bottom of 
                                the table.test annoucement 2 Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                                In the above code snippet, the dom option specifies the layout of the DataTables
                                elements. The lfr options stand for length changing input control, the table, and
                                filtering input control, respectively. The "thead-dark" option specifies a custom
                                class for the thead element of the DataTable. The "bottom"ip option specifies the
                                In the above code snippet, the dom option specifies the layout of the DataTables 
                                elements. The lfr options stand for length changing input control, the table, and 
                                filtering input control, respectively. The "thead-dark" option specifies a custom 
                                class for the thead element of the DataTable. The "bottom"ip option specifies the 
                                positioning of the table information and pagination control elements at the bottom of 
                                the table.test annoucement 2 Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                                In the above code snippet, the dom option specifies the layout of the DataTables
                                elements. The lfr options stand for length changing input control, the table, and
                                filtering input control, respectively. The "thead-dark" option specifies a custom
                                class for the thead element of the DataTable. The "bottom"ip option specifies the
                                In the above code snippet, the dom option specifies the layout of the DataTables 
                                elements. The lfr options stand for length changing input control, the table, and 
                                filtering input control, respectively. The "thead-dark" option specifies a custom 
                                class for the thead element of the DataTable. The "bottom"ip option specifies the 
                                positioning of the table information and pagination control elements at the bottom of 
                                the table.test annoucement 2 Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                                In the above code snippet, the dom option specifies the layout of the DataTables
                                elements. The lfr options stand for length changing input control, the table, and
                                filtering input control, respectively. The "thead-dark" option specifies a custom
                                class for the thead element of the DataTable. The "bottom"ip option specifies the
                                In the above code snippet, the dom option specifies the layout of the DataTables 
                                elements. The lfr options stand for length changing input control, the table, and 
                                filtering input control, respectively. The "thead-dark" option specifies a custom 
                                class for the thead element of the DataTable. The "bottom"ip option specifies the 
                                positioning of the table information and pagination control elements at the bottom of 
                                the table.test annoucement 2 Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                                In the above code snippet, the dom option specifies the layout of the DataTables
                                elements. The lfr options stand for length changing input control, the table, and
                                filtering input control, respectively. The "thead-dark" option specifies a custom
                                class for the thead element of the DataTable. The "bottom"ip option specifies the
                                In the above code snippet, the dom option specifies the layout of the DataTables 
                                elements. The lfr options stand for length changing input control, the table, and 
                                filtering input control, respectively. The "thead-dark" option specifies a custom 
                                class for the thead element of the DataTable. The "bottom"ip option specifies the 
                                positioning of the table information and pagination control elements at the bottom of 
                                the table.test annoucement 2 Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                                In the above code snippet, the dom option specifies the layout of the DataTables
                                elements. The lfr options stand for length changing input control, the table, and
                                filtering input control, respectively. The "thead-dark" option specifies a custom
                                class for the thead element of the DataTable. The "bottom"ip option specifies the
                                positioning of the table information and pagination control elements at the bottom of"""
                                )

# edit annoucement
#system_annoucer.edit_annoucement(1, "test annoucement 2", "Lorem ipsum dolor sit amet, consectetur adipiscing elit.")