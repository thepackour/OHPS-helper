import sqlite3
from functools import wraps

import main.debug as debug

_con = None

def create_connection(db_file='test.db'):
    global _con
    if _con is None:
        _con = sqlite3.connect(db_file)
        _con.row_factory = sqlite3.Row
    return _con

# cursor는 선언할 때에만 필요하고 호출할 때는 필요 없음
def with_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = create_connection()
        cursor = conn.cursor()
        try:
            result = func(cursor, *args, **kwargs)
            debug.log_w(func.__name__, args, kwargs, result)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            debug.log_w(func.__name__, args, kwargs, e)
            raise
    return wrapper

### 10분마다 메모리에 저장하고 꺼내는 코드 필요!!! ###