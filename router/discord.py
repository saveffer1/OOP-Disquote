from model import AccountSystem, ServerSystem, AnnouceSystem
import random
import shutil
import os

discord_account = AccountSystem()
discord_server = ServerSystem()
system_annoucer = AnnouceSystem()

## this is a mockup section
discord_account.add_admin(email="admin@mail.com", username="admin", password="1234")

discord_account.add_user(email="admin@mail.com", username="admin", password="1234") #0
discord_account.add_user(email="admin@min.com", username="HEE", password="1234") #1
discord_account.add_user(email="theway@mail.com", username="theway", password="1234") #2
discord_account.add_user(email="todie@mail.com", username="todie", password="1234") #3

hee = discord_account.get_user_account(email="admin@mail.com")
theway = discord_account.get_user_account(email="theway@mail.com")
todie = discord_account.get_user_account(email="todie@mail.com")

hee.state = 1
theway.state = 2
todie.state = 3

discord_account.get_user_account("admin@mail.com").add_request(1)
discord_account.get_user_account("admin@mail.com").add_request(2)
discord_account.get_user_account("admin@mail.com").add_request(3)
discord_account.get_user_account("admin@mail.com").add_request(1)

test_server1 = discord_server.add_server("test_server1", 1, "default")
test_server2 = discord_server.add_server("test_server2", 1, "default")

images = ['1.png', '2.png']
for i in range(5):
    discord_server.add_server(f"test_server{i}", 0, random.choice(images))

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

#system_annoucer.edit_annoucement(1, "test annoucement 2", "Lorem ipsum dolor sit amet, consectetur adipiscing elit.")