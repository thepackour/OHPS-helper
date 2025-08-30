import main.db.DBInit as dbinit
from .database import *

from .exceptions import *

dbinit.drop_all_tables()
dbinit.create_table()
dbinit.add_quests_data()
dbinit.add_users_data()
dbinit.add_levels_data()
dbinit.add_event_quest_data()