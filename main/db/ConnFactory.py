import sqlite3
from functools import wraps


def create_connection(db_file='test.db'):
    return sqlite3.connect(db_file)

# cursor는 선언할 때에만 필요하고 호출할 때는 필요 없음
def with_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = create_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            result = func(cursor, *args, **kwargs)
            conn.commit()
            return result
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    return wrapper

### 10분마다 메모리에 저장하고 꺼내는 코드 필요!!! ###