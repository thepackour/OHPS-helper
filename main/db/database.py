import datetime
import json
import os

from main.db.ConnFactory import with_connection
from main.db.exceptions import *
import main.debug as debug


def _is_details_dict_valid(details_dict: dict):
    keys = ('main_hand', 'number_of_keys', 'multi_input_direction', 'details')
    for key in keys:
        if key not in details_dict:
            return False
    return True

def _find_user(cursor, user_id: str):
    cursor.execute('''SELECT * FROM users WHERE id = ?''', (user_id,))
    if cursor.fetchone()[0] is None: raise NoSuchUser()
    return cursor.fetchone()

def _find_quest(cursor, quest_id: int):
    cursor.execute('''SELECT * FROM quests WHERE id = ?''', (quest_id,))
    res = cursor.fetchone()[0]
    if res is None: raise NoSuchQuest()
    return res

def _find_level_clears(cursor, quest_id: int):
    if _find_quest(cursor, quest_id) is None: raise NoSuchQuest()
    cursor.execute('''SELECT * FROM level_clears WHERE quest_id = ?''', (quest_id,))
    res = cursor.fetchall()
    dict_list = [dict(row) for row in res]
    dict_list.sort(key=lambda x: (x['id'], x['level_id']))
    return dict_list

def _find_quest_clears(cursor, quest_id: int):
    if _find_quest(cursor, quest_id) is None: raise NoSuchQuest()
    cursor.execute('''SELECT * FROM quest_clears WHERE quest_id = ?''', (quest_id,))
    res = cursor.fetchall()
    dict_list = [dict(row) for row in res]
    dict_list.sort(key=lambda x: x['id'])
    return dict_list

def _find_levels(cursor, quest_id: int):
    cursor.execute('''SELECT * FROM levels WHERE quest_id = ?''', (quest_id,))
    res = cursor.fetchall()
    if res:
        dict_list = [dict(row) for row in res]
        dict_list.sort(key=lambda x: x['id'])
        return dict_list
    else: return None


def get_event_quest():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 위치
    json_path = os.path.join(BASE_DIR, 'json', 'event_quest_info.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if data['open']:
        return find_quest_by_id(data['quest']['quest_id'])
    else: return None


def get_event_info():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(BASE_DIR, 'json', 'event_quest_info.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if data['open']: return data
        else: return None
    except FileNotFoundError:
        return None


@with_connection
def add_user(cursor, register_dict: dict):
    if _find_user(cursor, register_dict['id']) is None:
        cursor.execute("INSERT INTO users (id, username) VALUES (:id, :username)", register_dict)
    else:
        raise ExistingUser()


@with_connection
def add_details(cursor, id: str, details_dict: dict):
    cursor.execute('''SELECT EXISTS (SELECT * FROM users WHERE id = :id)''', (id,))
    if cursor.fetchone()[0]:
        cursor.execute('''
            UPDATE users
            SET main_hand = :main_hand,
            number_of_keys = :number_of_keys,
            multi_input_direction = :multi_input_direction,
            details = :details
            WHERE id = :target_id
            ''', details_dict)
    else:
        raise NoSuchUser()


@with_connection
def find_user(cursor, query_dict: dict):
    if 'id' in query_dict:
        cursor.execute('''SELECT * FROM users WHERE id = :id''', query_dict)
        res = cursor.fetchone()
        if res is None: raise NoSuchUser()
        return dict(res)
    elif 'username' in query_dict:
        cursor.execute('''SELECT * FROM users WHERE username = :username''', query_dict)
        res = cursor.fetchall()
        if res:
            dict_list = [dict(row) for row in res]
            return dict_list[0]
        else: raise NoSuchUser()
    else:
        raise InvalidDict()


@with_connection
def delete_user(cursor, user_id: str):
    cursor.execute('''SELECT EXISTS (SELECT * FROM users WHERE id = :user_id)''', (user_id,))
    if cursor.fetchone()[0]:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("UPDATE users SET deleted_at = :deleted_at WHERE id = :user_id", {"deleted_at": timestamp, "user_id": user_id})
    else:
        raise NoSuchUser()


@with_connection
def get_all_users(cursor): # 레벨 순으로 정렬
    cursor.execute('''SELECT * FROM users ORDER BY level DESC''')
    users_row_list = cursor.fetchall()
    users_dict_list = [dict(row) for row in users_row_list]
    return users_dict_list


@with_connection
def get_quest_name_list(cursor):
    cursor.execute('''SELECT id, name FROM quests''')
    id_name_list = cursor.fetchall()
    dict_list = [dict(row) for row in id_name_list]
    dict_list.sort(key=lambda x: x['id'])
    return dict_list


@with_connection
def find_quests_by_stars(cursor, stars: int):
    if stars < 1 or stars > 5: raise InvalidStars()
    else:
        cursor.execute('''SELECT * FROM quests WHERE stars = ?''', (stars,))
        res = cursor.fetchall()
        if not res: # res가 빈 리스트 or sqlite3.Row 객체로 이루어진 리스트
            raise NoSuchQuest()
        else:
            dict_list = [dict(row) for row in res]
            return dict_list


@with_connection
def find_quest_by_id(cursor, quest_id: int):
    cursor.execute('''SELECT * FROM quests WHERE id = ?''', (quest_id,))
    res = cursor.fetchone()
    debug.log(f"Found quest by id: {quest_id}", res)
    if res is None: return None
    else: return dict(res)


@with_connection
def find_quest_by_name(cursor, quest_name: str):
    cursor.execute('''SELECT * FROM quests WHERE name = ?''', (quest_name,))
    res = cursor.fetchone()
    if res is None:
        raise NoSuchQuest()
    else:
        return dict(res)


@with_connection
def find_level_clears(cursor, user_id: str):
    if _find_user(cursor, user_id) is None: raise NoSuchUser()
    cursor.execute('''SELECT * FROM level_clears WHERE user_id = ?''', (user_id,))
    res = cursor.fetchall()
    dict_list = [dict(row) for row in res]
    dict_list.sort(key=lambda x: x['id'])
    return dict_list


@with_connection
def find_quest_clears(cursor, user_id: str):
    if _find_user(cursor, user_id) is None: raise NoSuchUser()
    cursor.execute('''SELECT * FROM quest_clears WHERE user_id = ?''', (user_id,))
    res = cursor.fetchall()
    dict_list = [dict(row) for row in res]
    dict_list.sort(key=lambda x: x['id'])
    return dict_list


@with_connection
def find_levels(cursor, query):
    if type(query) is list:
        placeholders = ', '.join(['?'] * len(query))

        query = f'''SELECT * FROM levels WHERE id IN ({placeholders})'''
        cursor.execute(query, query)
        rows = cursor.fetchall()
        dict_list = [dict(row) for row in rows]
        return dict_list

    elif type(query) is int:
        dict_list = _find_levels(cursor, query)
        return dict_list

    else: raise TypeError()


@with_connection
def find_quests(cursor, quest_id_list: list):
    placeholders = ', '.join(['?'] * len(quest_id_list))

    query = f'''SELECT * FROM levels WHERE id IN ({placeholders})'''
    cursor.execute(query, quest_id_list)
    rows = cursor.fetchall()
    dict_list = [dict(row) for row in rows]
    return dict_list