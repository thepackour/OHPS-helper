import main.db.DBInit as dbinit
from .database import *

from .exceptions import *

dbinit.create_table()
dbinit.add_quests_data()
dbinit.add_users_data()
dbinit.add_levels_data()