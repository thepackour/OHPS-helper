import time
from dbmanagertest import *
from DBInit import *

create_table()

testuser1 = {
    'id': '433224189194010654',
    'username': 'thepackour'
}

add_user(testuser1)

res = find_all_users()

for r in res:
    print(r)

time.sleep(30)