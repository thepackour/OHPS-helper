import sqlite3
import datetime
from exceptions import *
from functools import wraps

def create_connection(db_file='test.db'):
    return sqlite3.connect(db_file)

# cursor는 선언할 때에만 필요하고 호출할 때는 필요 없음
def with_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = create_connection()
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


def console_log(message):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[DBManager] ({now}) | {message}")

def is_details_dict_valid(details_dict):
    keys = ('main_hand', 'number_of_keys', 'multi_input_direction', 'details')
    for key in keys:
        if key not in details_dict:
            return False
    return True

@with_connection
def add_user(cursor, register_dict):
    cursor.execute('''SELECT EXISTS (SELECT * FROM users WHERE id = :id)''', register_dict)
    if cursor.fetchone()[0]: raise ExistingUser()
    else: cursor.execute("INSERT INTO users (id, username) VALUES (:id, :username)", register_dict)

@with_connection
def add_details(cursor, details_dict):
    cursor.execute('''
    UPDATE users
    SET main_hand = :main_hand,
    number_of_keys = :number_of_keys,
    multi_input_direction = :multi_input_direction,
    details = :details;
    ''', details_dict)

@with_connection
def find_user(cursor, dict):
    if 'id' in dict:
        cursor.execute('''SELECT * FROM users WHERE id = :id''', dict['id'])
        return cursor.fetchone()
    elif 'username' in dict:
        cursor.execute('''SELECT * FROM users WHERE username = :username''', dict['username'])
        return cursor.fetchall()
    else:
        raise InvalidDict()

@with_connection
def delete_user(cursor, id):
    cursor.execute('''SELECT EXISTS (SELECT * FROM users WHERE id = :id)''', id)
    if cursor.fetchone()[0]:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("UPDATE users SET deleted_at = :deleted_at WHERE id = :id", {"deleted_at": timestamp, "id": id})
        console_log(f"Successfully added 'deleted_at' to id: {id}")
    else:
        raise NoSuchUser()

@with_connection
def find_all_users(cursor):
    cursor.execute('''SELECT * FROM users''')
    return cursor.fetchall()