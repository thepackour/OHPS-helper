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
    name VARCHAR(255),
    stars TINYINT,
    type TINYINT DEFAULT 0,
    req TINYINT,
    exp SMALLINT
);''',
'''
CREATE TABLE IF NOT EXISTS levels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quest_id BIGINT,
    artist VARCHAR(255),
    song VARCHAR(255),
    creator VARCHAR(255),
    exp SMALLINT
);''',
'''
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(255) PRIMARY KEY,
    last_level_clear INT,
    last_quest_clear INT,
    username VARCHAR(255),
    level INT DEFAULT 1,
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
    part VARCHAR(255),
    video VARCHAR(255),
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
    print("CREATE: completed")
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
    print("INSERT: completed")
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
    print("INSERT: completed")
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
    print("INSERT: completed")
    con.close()
