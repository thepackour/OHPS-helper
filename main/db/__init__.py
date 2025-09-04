import main.db.DBInit as dbinit
from main.db.database import *

from main.db.exceptions import *

dbinit.drop_all_tables()
dbinit.create_table()
dbinit.add_quests_data()
dbinit.add_levels_data()
dbinit.add_event_quest_data()