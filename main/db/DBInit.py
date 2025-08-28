import sqlite3 as sql

from main.dto.register_dto import RegisterDto

con = sql.connect('test.db')
con.execute('PRAGMA foreign_keys = ON')
cur = con.cursor()


query_list = ('''
CREATE TABLE IF NOT EXISTS quests (
    id SMALLINT PRIMARY KEY,
    name VARCHAR(255),
    stars TINYINT,
    type TINYINT DEFAULT 0,
    req TINYINT,
    exp SMALLINT
);''',
'''
CREATE TABLE IF NOT EXISTS levels (
    id MEDIUMINT PRIMARY KEY,
    quest_id BIGINT
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
    id BIGINT PRIMARY KEY,
    user_id VARCHAR(255),
    level_id MEDIUMINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(level_id) REFERENCES levels(id)
);''',
'''CREATE TABLE IF NOT EXISTS quest_clears (
    id BIGINT PRIMARY KEY,
    user_id VARCHAR(255),
    quest_id SMALLINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(quest_id) REFERENCES quests(id)
);''',
'''CREATE TABLE IF NOT EXISTS collab_quest_progress (
    id SMALLINT PRIMARY KEY,
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
    print("CREATE TABLE: completed")
    con.commit()
    con.close()


### TEST ###
def add_testuser():
    con = sql.connect('test.db')
    cur = con.cursor()
    testuser = RegisterDto(id='433224189194010654', username='thepackour')
    cur.execute("INSERT INTO users (id, username) VALUES (:id, :username)", testuser.dict())

