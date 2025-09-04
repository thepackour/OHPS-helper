import copy
import json
import os
import sqlite3 as sql

from main.dto.register_dto import RegisterDto

con = sql.connect('test.db')
con.execute('PRAGMA foreign_keys = ON')
cur = con.cursor()


query_list = ('''
CREATE TABLE IF NOT EXISTS quests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    stars TINYINT NOT NULL,
    type TINYINT DEFAULT 0,
    req TINYINT NOT NULL,
    exp SMALLINT NOT NULL
);''',
'''
CREATE TABLE IF NOT EXISTS levels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quest_id BIGINT NOT NULL,
    artist VARCHAR(255) NOT NULL,
    song VARCHAR(255) NOT NULL,
    creator VARCHAR(255) NOT NULL,
    exp SMALLINT NOT NULL
);''',
'''
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(255) PRIMARY KEY,
    last_level_clear INT,
    last_quest_clear INT,
    username VARCHAR(255) NOT NULL,
    exp BIGINT DEFAULT 0,
    tier TINYINT DEFAULT 4,
    main_hand VARCHAR(255),
    number_of_keys VARCHAR(255),
    multi_input_direction VARCHAR(255),
    details VARCHAR(1023),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);''',
'''
CREATE TABLE IF NOT EXISTS level_clears (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(255),
    level_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(level_id) REFERENCES levels(id)
);''',
'''CREATE TABLE IF NOT EXISTS quest_clears (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(255),
    quest_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(quest_id) REFERENCES quests(id)
);''',
'''CREATE TABLE IF NOT EXISTS collab_quest_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    level_clear_id INT,
    part VARCHAR(255) NOT NULL,
    video VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(level_clear_id) REFERENCES level_clears(id)
);''')

def create_table():
    con = sql.connect('test.db')
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()
    for query in query_list:
        cur.execute(query)
    con.commit()
    print("create_table: completed")
    con.close()


def add_quests_data():
    con = sql.connect('test.db')
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 위치
    json_path = os.path.join(BASE_DIR, 'json', 'quests.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for _ in data:
        cur.execute('''
        INSERT INTO quests (name, stars, type, req, exp) 
        VALUES (?, ?, ?, ?, ?)
        ''', (_['name'], _['stars'], _['type'], _['req'], _['exp']))
    con.commit()
    print("add_quests_data: completed")
    con.close()




def add_users_data():
    con = sql.connect('test.db')
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 위치
    json_path = os.path.join(BASE_DIR, 'json', 'users.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for _ in data:
            cur.execute('''
        INSERT INTO users (id, username) 
        VALUES (?, ?)
        ''', (_['id'], _['username']))
    con.commit()
    print("add_users_data: completed")
    con.close()


def add_levels_data():
    con = sql.connect('test.db')
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 위치
    json_path = os.path.join(BASE_DIR, 'json', 'levels.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for _ in data:
        cur.execute('''
        INSERT INTO levels (quest_id, artist, song, creator, exp) 
        VALUES (:quest_id, :artist, :song, :creator, :exp)
        ''', _)
    con.commit()
    print("add_levels_data: completed")
    con.close()


def add_event_quest_data():
    con = sql.connect('test.db')
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 위치
    json_path = os.path.join(BASE_DIR, 'json', 'event_quest_info.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data['quest']['type'] = 2
    data['quest']['req'] = 0
    cur.execute('''
    INSERT INTO quests (name, stars, type, req, exp) 
    VALUES (:name, :stars, :type, :req, :exp)
    ''', data['quest'])
    cur.execute('''SELECT seq FROM sqlite_sequence WHERE name = 'quests';''')
    data['quest']['quest_id'] = cur.fetchone()[0]

    levels = data['levels']
    for i in levels:
        level = copy.deepcopy(levels[i])
        level['quest_id'] = data['quest']['quest_id']
        cur.execute('''
        INSERT INTO levels (quest_id, artist, song, creator, exp) 
        VALUES (:quest_id, :artist, :song, :creator, :exp)
        ''', level)
        cur.execute('''SELECT seq FROM sqlite_sequence WHERE name = 'levels';''')
        data['levels'][i]['level_id'] = cur.fetchone()

    con.commit()
    con.close()
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
    print("add_event_quest_data: completed")


def drop_all_tables():
    con = sql.connect('test.db')
    con.execute('PRAGMA foreign_keys = OFF;')
    cur = con.cursor()

    cur.execute('''SELECT name FROM sqlite_master WHERE type='table';''')
    tables = cur.fetchall()

    if ('sqlite_sequence',) in tables: tables.remove(('sqlite_sequence',))

    for table in tables:
        table_name = table[0]
        cur.execute(f'DROP TABLE IF EXISTS {table_name}')
        print(f'Dropped table: {table_name}')

    con.commit()
    con.close()