import datetime
import json
import os
import sqlite3

import numpy


class QuitWhilePrompting(Exception):
    pass

class NoSuchData(Exception):
    pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
task_queue_path = os.path.join(BASE_DIR, 'db', 'json', 'task_queue.json')

_con = None

def create_connection(db_file='test.db'):
    global _con
    if _con is None:
        _con = sqlite3.connect(db_file)
        _con.row_factory = sqlite3.Row
    return _con

def minEXP(level: int):
    return numpy.ceil(numpy.divide(numpy.power(1.2, level)-1.2, 0.012))

def EXPtoLevel(exp: int):
    return numpy.trunc(numpy.divide(numpy.log(numpy.multiply(0.012, exp) + 1.2),numpy.log(1.2)))


def users():
    columns = ('username', 'level', 'exp', 'tier', 'last_level_clear', 'last_quest_clear', 'main_hand',
               'number_of_keys', 'multi_input_direction', 'details', 'created_at')
    int_columns = ('level', 'exp', 'tier', 'last_level_clear', 'last_quest_clear')
    str_columns = ('username', 'main_hand', 'number_of_keys', 'multi_input_direction', 'details')

    while True:
        print("---------- /users ---------- \n"
              "1. add user \n"
              "2. update user \n"
              "3. delete user \n"
              "4. hard-delete user \n"
              "0. exit \n")

        cmd = input("> ")

        if cmd == '0':
            break
        elif cmd == '1':
            print("---------- /users/add_user ---------- \n")
            user_id = input("id: ")
            username = input("username: ")
            exp = input("exp: ")
            tier = input("tier (1~4): ")
            last_level_clear = input("last_level_clear: ")
            last_quest_clear = input("last_quest_clear: ")
            main_hand = input("main_hand: ")
            number_of_keys = input("number_of_keys: ")
            multi_input_direction = input("multi_input_direction: ")
            details = input("details: ")

            if input("Confirm? (y/n): ") == 'y':
                con = create_connection()
                cur = con.cursor()
                cur.execute('''SELECT EXISTS (SELECT 1 FROM users WHERE id = ?)''', (user_id,))
                if cur.fetchone()[0]:
                    print("Existing user")
                else:
                    try:
                        if not user_id.isdigit(): raise TypeError
                        entry = {
                            'id': user_id,
                            'username': username,
                            'exp': 0 if not exp else int(exp),
                            'tier': 4 if not tier else int(tier),
                            'last_level_clear': None if not last_level_clear else int(last_level_clear),
                            'last_quest_clear': None if not last_quest_clear else int(last_quest_clear),
                            'main_hand': None if not main_hand else main_hand,
                            'number_of_keys': None if not number_of_keys else number_of_keys,
                            'multi_input_direction': None if not multi_input_direction else multi_input_direction,
                            'details': None if not details else details,
                        }
                    except TypeError: print("Invalid input (especially int)")
                    try:
                        cur.execute('''
                        INSERT INTO users 
                        (id, username, exp, tier, last_level_clear, last_quest_clear, main_hand, number_of_keys, multi_input_direction, details)
                        VALUES (:id, :username, :exp, :tier, :last_level_clear, :last_quest_clear, :main_hand, :number_of_keys, :multi_input_direction, :details)
                        ''', entry)
                        con.commit()
                        print("Added new user")
                    except sqlite3.ProgrammingError: print("ProgrammingError while running INSERT")

        elif cmd == '2':
            print("---------- /users/update_user ---------- \n")
            user_id = input("Type user id: ")
            con = create_connection()
            cur = con.cursor()
            cur.execute('''SELECT EXISTS (SELECT 1 FROM users WHERE id = ?)''', (user_id,))
            if cur.fetchone()[0]:
                s = "Which column to change \n(" + ", ".join(columns) + ") \n:"
                target = input(s)
                if target in int_columns:
                    change = input("Change into (only digit): ")
                    if change.isdigit():
                        cur.execute(f'''
                            UPDATE users SET {target} = ? WHERE id = ?
                            ''', (int(change), user_id))
                        con.commit()
                        print("Updated user")
                        if target == 'tier':
                            print("****************************************\n"
                                  "Don't forget to change tier role"
                                  "****************************************\n")
                    else: print("Invalid input (only digit)")
                elif target in str_columns:
                    change = input("Change into: ")
                    cur.execute(f'''
                        UPDATE users SET {target} = ? WHERE id = ?
                        ''', (change, user_id))
                    con.commit()
                    print("Updated user")
                elif target == "created_at":
                    change = input(f"Change into (ex. {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}): ")
                    try:
                        datetime.datetime.strptime(change, "%Y-%m-%d %H:%M:%S")
                        cur.execute(f'''
                            UPDATE users SET {target} = ? WHERE id = ?
                            ''', (change, user_id))
                        con.commit()
                        print("Updated user")
                    except ValueError: print("Invalid date format")
                else: print("Invalid column name")
            else: print("User does not exist")

        elif cmd == '3':
            print("---------- /users/delete_user ---------- \n")
            user_id = input("Type user id: ")
            if input("Confirm? (y/n): ") == 'y':
                con = create_connection()
                cur = con.cursor()
                cur.execute('''SELECT EXISTS (
                SELECT 1 FROM users
                WHERE id = ?
                )''', (user_id,))
                if cur.fetchone()[0]:
                    cur.execute('''
                    UPDATE users SET deleted_at = ? WHERE id = ?
                    ''', (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id))
                    print("Deleted user")
                else: print("No such user")

        elif cmd == '4':
            print("---------- /users/hard-delete_user ---------- \n")
            user_id = input("Type user id: ")
            if input("Confirm? (y/n): ") == 'y':
                con = create_connection()
                cur = con.cursor()
                cur.execute('''SELECT EXISTS (
                            SELECT 1 FROM users
                            WHERE id = ?
                            )''', (user_id,))
                if cur.fetchone()[0]:
                    cur.execute('''
                                DELETE FROM users WHERE id = ?
                                ''', (user_id,))
                    print("Hard-deleted user")
                else: print("No such user")


def clears():
    while True:
        print("---------- /clears ---------- \n"
              "1. add level clear (automatically adds quest clear) \n"
              "2. add quest clear \n"
              "3. delete level clear \n"
              "4. delete quest clear \n"
              "0. exit")

        cmd = input("> ")

        if cmd == '0':
            break
        elif cmd == '1':
            print("---------- /clears/add_level_clear ---------- \n")
            user_id = input("user_id: ")
            level_id = input("level_id: ")
            created_at = input(f"created_at (ex. {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}): ")

            if input("Confirm? (y/n): ") == 'y':
                try:
                    datetime.datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                    con = create_connection()
                    cur = con.cursor()
                    cur.execute('''SELECT * FROM users WHERE id = ?''', (user_id,))
                    u = cur.fetchone()
                    cur.execute('''SELECT * FROM levels WHERE id = ?''', (level_id,))
                    l = cur.fetchone()
                    if u is not None and l is not None:
                        u = dict(u)
                        l = dict(l)
                        cur.execute('''
                                        INSERT INTO level_clears 
                                        (user_id, level_id, created_at) VALUES (?, ?, ?)
                                        ''', (user_id, level_id, created_at))
                        print("Added new level_clear")

                        cur.execute('''
                        UPDATE users SET exp = ? WHERE id = ?
                        ''', (u['exp'] + l['exp'], user_id))
                        print("Updated user's exp")

                        with open(task_queue_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        data.append({
                            'type': 'level clear',
                            'submitted_at': created_at,
                            'user_id': user_id,
                            'level_id': level_id,
                            'exp_before': u['exp'],
                            'exp_after': u['exp'] + l['exp']
                        })
                        with open(task_queue_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                        print("Added task")

                        cur.execute('''
                        SELECT quest_id FROM levels WHERE id = ? LIMIT 1 
                        ''', (level_id,))
                        quest_id = cur.fetchone()[0]
                        cur.execute('''
                        SELECT id FROM levels WHERE quest_id = ?
                        ''', (quest_id,))
                        level_id_list = [dict(_)['id'] for _ in cur.fetchall()]
                        cte_q = 'SELECT '
                        cte_q += ' UNION ALL SELECT '.join(str(_) for _ in level_id_list)

                        query = f'''
                        WITH target_ids(id) AS (
                            {cte_q}
                        )
                        SELECT
                            t.id,
                            CASE WHEN lc.level_id IS NOT NULL THEN 1 ELSE 0 END AS e
                        FROM target_ids t
                        LEFT JOIN level_clears lc ON t.id = lc.level_id;'''
                        cur.execute(query)
                        lst = cur.fetchall()
                        if all([dict(_)['e'] for _ in lst]):
                            cur.execute('''
                            INSERT INTO quest_clears
                            (user_id, quest_id, created_at) VALUES (?, ?, ?)
                            ''', (user_id, quest_id, created_at))
                            print("Added new quest_clear")

                            cur.execute('''
                            SELECT exp FROM quests WHERE id = ? LIMIT 1 
                            ''')
                            exp = cur.fetchone()[0]
                            cur.execute('''
                            UPDATE users SET exp = ? WHERE id = ?
                            ''', (u['exp'] + l['exp'] + exp, user_id))
                            print("Updated user's exp")

                            with open(task_queue_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                            data.append({
                                'type': 'quest clear',
                                'submitted_at': created_at,
                                'user_id': user_id,
                                'quest_id': quest_id,
                                'exp_before': u['exp'] + l['exp'],
                                'exp_after': u['exp'] + l['exp'] + exp
                            })
                            with open(task_queue_path, 'w', encoding='utf-8') as f:
                                json.dump(data, f, ensure_ascii=False, indent=2)
                            print("Added task")
                        con.commit()
                        print("Committed")

                    elif l: print("No such user")
                    else: print("No such level")
                except ValueError: print("Invalid date format")

        elif cmd == '2':
            print("---------- /clears/add_quest_clear ---------- \n")
            user_id = input("user_id: ")
            quest_id = input("level_id: ")
            created_at = input(f"created_at (ex. {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}): ")

            if input("Confirm? (y/n): ") == 'y':
                try:
                    datetime.datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                    con = create_connection()
                    cur = con.cursor()
                    cur.execute('''SELECT * FROM users WHERE id = ?''', (user_id,))
                    u = cur.fetchone()
                    cur.execute('''SELECT * FROM quests WHERE id = ?''', (quest_id,))
                    q = cur.fetchone()
                    if u is not None and q is not None:
                        u = dict(u)
                        q = dict(q)
                        cur.execute('''
                            INSERT INTO quest_clears
                            (user_id, quest_id, created_at) VALUES (?, ?, ?)
                            ''', (int(user_id), int(quest_id), created_at))

                        print("Added new quest_clear (not committed yet)")
                        cur.execute('''
                            UPDATE users SET exp = ? WHERE id = ?
                            ''', (u['exp'] + q['exp'], user_id))
                        con.commit()
                        print("Updated user's exp (committed)")

                        with open(task_queue_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        data.append({
                            'type': 'quest clear',
                            'submitted_at': created_at,
                            'user_id': user_id,
                            'quest_id': quest_id,
                            'exp_before': u['exp'],
                            'exp_after': u['exp'] + q['exp']
                        })
                        with open(task_queue_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                        print("Added task")
                    elif q: print("No such user or invalid input")
                    else: print("No such quest or invalid input")
                except ValueError: print("Invalid date format")

        elif cmd == '3':
            print("---------- /clears/delete_level_clear ---------- \n")
            c_id = input("id: ")

            if input("Confirm? (y/n): ") == 'y':
                if c_id.isdigit():
                    con = create_connection()
                    cur = con.cursor()
                    cur.execute('''SELECT * FROM level_clears WHERE id = ? LIMIT 1''', (c_id,))
                    c = cur.fetchone()
                    if c is not None:
                        c = dict(c)
                        cur.execute('''DELETE FROM level_clears WHERE id = ? ''', (c_id,))
                        con.commit()
                        print("Deleted level_clear")
                        try:
                            cur.execute('''
                            SELECT exp FROM users WHERE id = ? LIMIT 1
                            ''', (c['user_id'],))
                            u_exp = cur.fetchone()[0]
                            cur.execute('''
                            SELECT exp FROM levels WHERE id = ? LIMIT 1 
                            ''', (c['level_id'],))
                            l_exp = cur.fetchone()[0]
                            cur.execute('''
                            UPDATE users SET exp = ? WHERE id = ?
                            ''', (u_exp - l_exp, c['user_id']))
                            print("Updated user's exp")
                        except Exception as e: print("Error occurred:", e)
                    else: print("No such level_clear")
                else: print("Invalid input (only digit)")

        elif cmd == '4':
            print("---------- /clears/delete_quest_clear ---------- \n")
            c_id = input("id: ")

            if input("Confirm? (y/n): ") == 'y':
                if c_id.isdigit():
                    con = create_connection()
                    cur = con.cursor()
                    cur.execute('''SELECT EXISTS (SELECT 1 FROM quest_clears WHERE id = ?)''', (int(c_id),))
                    c = cur.fetchone()[0]
                    if c is not None:
                        cur.execute('''DELETE FROM quest_clears WHERE id = ? ''', (int(c_id),))
                        con.commit()
                        print("Deleted quest_clear")
                        try:
                            cur.execute('''
                            SELECT exp FROM users WHERE id = ? LIMIT 1
                            ''', (c['user_id'],))
                            u_exp = cur.fetchone()[0]
                            cur.execute('''
                            SELECT exp FROM quests WHERE id = ? LIMIT 1 
                            ''', (c['quest_id'],))
                            q_exp = cur.fetchone()[0]
                            cur.execute('''
                            UPDATE users SET exp = ? WHERE id = ?
                            ''', (u_exp - q_exp, c['user_id']))
                            print("Updated user's exp")
                        except Exception as e: print("Error occurred:", e)
                    else: print("No such quest_clear")
                else: print("Invalid input (only digit)")

def levels():
    columns = ('quest_id', 'artist', 'song', 'creator', 'exp')
    int_columns = ('quest_id', 'exp')
    str_columns = ('artist', 'song', 'creator')

    while True:
        print("---------- /levels ---------- \n"
              "1. add level \n"
              "2. update level \n"
              "3. delete level \n"
              "0. exit \n")

        cmd = input("> ")

        if cmd == '0':
            break
        elif cmd == '1':
            print("---------- /levels/add_level ---------- \n")
            quest_id = input("quest_id: ")
            artist = input("artist: ")
            song = input("song: ")
            creator = input("creator: ")
            exp = input("exp: ")

            if input("Confirm? (y/n): ") == 'y':
                if exp.isdigit():
                    con = create_connection()
                    cur = con.cursor()
                    cur.execute('''SELECT EXISTS (SELECT 1 FROM quests WHERE id = ?)''', (int(quest_id),))
                    if cur.fetchone()[0]:
                        entry = {
                            'quest_id': quest_id,
                            'artist': artist,
                            'song': song,
                            'creator': creator,
                            'exp': exp
                        }
                        cur.execute('''
                        INSERT INTO levels 
                        (quest_id, artist, song, creator, exp)
                        VALUES (:quest_id, :artist, :song, :creator, :exp)
                        ''', entry)
                        con.commit()
                        print("Added new level")
                    else: print("No such quest")
                else: print("Invalid exp")

        elif cmd == '2':
            print("---------- /levels/update_level ---------- \n")
            level_id = input("Type level id: ")
            if level_id.isdigit():
                con = create_connection()
                cur = con.cursor()
                cur.execute('''SELECT EXISTS (SELECT 1 FROM levels WHERE id = ?)''', (int(level_id),))
                if cur.fetchone()[0]:
                    s = "Which column to change \n(" + ", ".join(columns) + ") \n:"
                    target = input(s)
                    if target in int_columns:
                        change = input("Change into (only digit): ")
                        if change.isdigit():
                            cur.execute(f'''
                                UPDATE levels SET {target}= ? WHERE id = ?
                                ''', (int(change), int(level_id)))
                            con.commit()
                            print("Updated level")
                        else: print("Invalid input (only digit)")
                    elif target in str_columns:
                        change = input("Change into: ")
                        cur.execute(f'''
                            UPDATE levels SET {target} = ? WHERE id = ?
                            ''', (change, int(level_id)))
                        con.commit()
                        print("Updated level")
                    else: print("Invalid column name")
                else: print("Level does not exist")
            else: print("Invalid input (only digit)")

        elif cmd == '3':
            print("---------- /levels/delete_level ---------- \n")
            level_id = input("Type level id: ")
            if level_id.isdigit():
                if input("Confirm? (y/n): ") == 'y':
                    con = create_connection()
                    cur = con.cursor()
                    cur.execute('''SELECT EXISTS (
                                SELECT 1 FROM levels
                                WHERE id = ?
                                )''', (int(level_id),))
                    if cur.fetchone()[0]:
                        cur.execute('''
                                    DELETE FROM levels WHERE id = ?
                                    ''', (int(level_id),))
                        con.commit()
                        print("Deleted level")
                    else: print("No such level")
            else: print("Invalid input (only digit)")

def quests():
    columns = ('name', 'stars', 'type', 'req', 'exp')
    int_columns = ('stars', 'type', 'req', 'exp')
    str_columns = ('name',)

    while True:
        print("---------- /quests ---------- \n"
              "1. add quest \n"
              "2. update quest \n"
              "3. delete quest \n"
              "0. exit \n")

        cmd = input("> ")

        if cmd == '0':
            break
        elif cmd == '1':
            print("---------- /quests/add_quest ---------- \n")
            name = input("name: ")
            stars = input("stars: ")
            type = input("type: ")
            req = input("req: ")
            exp = input("exp: ")

            entry = {
                'name': name,
                'stars': stars,
                'type': type,
                'req': req,
                'exp': exp
            }

            if input("Confirm? (y/n): ") == 'y':
                if all(entry[_].isdigit() for _ in int_columns):
                    con = create_connection()
                    cur = con.cursor()
                    cur.execute('''
                        INSERT INTO levels 
                        (quest_id, artist, song, creator, exp)
                        VALUES (:quest_id, :artist, :song, :creator, :exp)
                        ''', entry)
                    con.commit()
                    print("Added new quest")
                else:
                    print("Invalid input (only digit)")

        elif cmd == '2':
            print("---------- /quests/update_quest ---------- \n")
            quest_id = input("Type quest id: ")
            if quest_id.isdigit():
                con = create_connection()
                cur = con.cursor()
                cur.execute('''SELECT EXISTS (SELECT 1 FROM quests WHERE id = ?)''', (int(quest_id),))
                if cur.fetchone()[0]:
                    s = "Which column to change \n(" + ", ".join(columns) + ") \n:"
                    target = input(s)
                    if target in int_columns:
                        change = input("Change into (only digit): ")
                        if change.isdigit():
                            cur.execute(f'''
                                    UPDATE quests SET {target} = ? WHERE id = ?
                                    ''', (int(change), int(quest_id)))
                            con.commit()
                            print("Updated quest")
                        else:
                            print("Invalid input (only digit)")
                    elif target in str_columns:
                        change = input("Change into: ")
                        cur.execute(f'''
                                UPDATE quests SET {target} = ? WHERE id = ?
                                ''', (change, int(quest_id)))
                        con.commit()
                        print("Updated quest")
                    else: print("Invalid column name")
                else: print("Quest does not exist")
            else: print("Invalid input (only digit)")

        elif cmd == '3':
            print("---------- /quests/delete_quest ---------- \n")
            quest_id = input("Type quest id: ")
            if quest_id.isdigit():
                if input("Confirm? (y/n): ") == 'y':
                    con = create_connection()
                    cur = con.cursor()
                    cur.execute('''SELECT EXISTS (
                                    SELECT 1 FROM quests
                                    WHERE id = ?
                                    )''', (int(quest_id),))
                    if cur.fetchone()[0]:
                        cur.execute('''
                                        DELETE FROM quests WHERE id = ?
                                        ''', (int(quest_id),))
                        print("Deleted quest")
                    else:
                        print("No such quest")
            else:
                print("Invalid input (only digit)")

def collab():
    columns = ('level_clear_id', 'part', 'video', 'created_at')

    while True:
        print("---------- /collab ---------- \n"
              "1. add progress \n"
              "2. update progress \n"
              "3. delete progress \n"
              "4. complete and reset progress \n"
              "0. exit \n")

        cmd = input("> ")

        if cmd == '0':
            break
        elif cmd == '1':
            print("---------- /collab/add_progress ---------- \n")
            level_clear_id = input("level_clear_id: ")
            part = input("part (ex. 1st level A type 2nd part = 1-A-2): ")
            video = input("video: ")
            created_at = input(f"created_at (ex. {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}): ")

            part_list = part.split("-")
            if len(part_list) == 3 and (part_list[0].isdigit() and part_list[1].isalpha() and part_list[2].isdigit()):
                try:
                    datetime.datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                    entry = {
                        'level_clear_id': level_clear_id,
                        'part': part,
                        'video': video,
                        'created_at': created_at
                    }
                    con = create_connection()
                    cur = con.cursor()
                    cur.execute('''
                        INSERT INTO levels 
                        (level_clear_id, part, video, created_at)
                        VALUES (:level_clear_id, :part, :video, :created_at)
                        ''', entry)
                    con.commit()
                    print("Added new progress")
                except ValueError: print("Invalid date format")
            else: print("Invalid input (part)")

        elif cmd == '2':
            print("---------- /collab/update_progress ---------- \n")
            progress_id = input("Type progress_id: ")

            if progress_id.isdigit():
                con = create_connection()
                cur = con.cursor()
                cur.execute('''SELECT EXISTS (SELECT 1 FROM collab_quest_progress WHERE id = ?)''', (int(progress_id),))
                if cur.fetchone()[0]:
                    s = "Which column to change \n(" + ", ".join(columns) + ") \n:"
                    target = input(s)
                    if target == 'level_clear_id':
                        change = input("Change into (only digit): ")
                        if change.isdigit():
                            cur.execute(f'''
                                UPDATE collab_quest_progress SET {target} = ? WHERE id = ?
                                ''', (int(change), int(progress_id)))
                            con.commit()
                            print("Updated progress")
                        else: print("Invalid input (only digit)")
                    elif target == 'part':
                        change = input("Change into: ")
                        part_list = change.split("-")
                        if len(part_list) == 3 and (part_list[0].isdigit() and part_list[1].isalpha() and part_list[2].isdigit()):
                            cur.execute(f'''
                                UPDATE quests SET {target} = ? WHERE id = ?
                                ''', (change, int(progress_id)))
                            con.commit()
                            print("Updated progress")
                    elif target == 'video':
                        change = input("Change into: ")
                        cur.execute(f'''
                            UPDATE collab_quest_progress SET {target} = ? WHERE id = ?
                            ''', (change, int(progress_id)))
                        con.commit()
                        print("Updated progress")
                    elif target == 'created_at':
                        change = input("Change into: ")
                        try:
                            datetime.datetime.strptime(change, "%Y-%m-%d %H:%M:%S")
                            cur.execute(f'''
                                UPDATE collab_quest_progress SET {target} = ? WHERE id = ?
                                ''', (change, int(progress_id)))
                            con.commit()
                            print("Updated progress")
                        except ValueError: print("Invalid date format")
                    else: print("Invalid column name")
                else: print("Progress does not exist")
            else: print("Invalid input (only digit)")
        elif cmd == '3':
            print("---------- /collab/delete_progress ---------- \n")
            progress_id = input("Type progress_id: ")
            if progress_id.isdigit():
                if input("Confirm? (y/n): ") == 'y':
                    con = create_connection()
                    cur = con.cursor()
                    cur.execute('''SELECT EXISTS (
                        SELECT 1 FROM collab_quest_progress
                        WHERE id = ?
                        )''', (int(progress_id),))
                    if cur.fetchone()[0]:
                        cur.execute('''
                            DELETE FROM collab_quest_progress WHERE id = ?
                            ''', (int(progress_id),))
                        print("Deleted progress")
                    else: print("No such progress")
            else: print("Invalid input (only digit)")

        elif cmd == '4':
            print("---------- /collab/complete_and_reset_progress ---------- \n")
            progress_id = input("Type progress_id: ")
            if progress_id.isdigit():
                if input("Confirm? (y/n): ") == 'y':
                    con = create_connection()
                    cur = con.cursor()
                    cur.execute('''SELECT EXISTS (
                        SELECT 1 FROM collab_quest_progress
                        WHERE id = ?
                        )''', (int(progress_id),))
                    if cur.fetchone()[0]:
                        cur.execute('''
                            DELETE FROM collab_quest_progress WHERE id = ?
                            ''', (int(progress_id),))
                        print("Deleted progress")
                    else: print("No such progress")
            else: print("Invalid input (only digit)")

def challenges():
    while True:
        print("---------- /challenges ---------- \n"
              "1. add challenge clear \n"
              "2. delete challenge level clear \n"
              "0. exit \n")

        cmd = input("> ")

        if cmd == '0':
            break
        elif cmd == '1':
            print("---------- /challenges/add_challenge_clear ---------- \n")
            user_id = input("user_id: ")
            level = input("level (ex. alpha tier 2nd level = 1-2): ")
            created_at = input(f"created_at (ex. {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}): ")

            ch_info_list = level.split("-")
            if len(ch_info_list) == 2 and ch_info_list[0].isdigit() and ch_info_list[1].isdigit():
                try:
                    datetime.datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                except ValueError: print("Invalid date format")
                except Exception as e: print(e)
                else:
                    entry = {
                        'user_id': user_id,
                        'level': level,
                        'created_at': created_at
                    }
                    con = create_connection()
                    cur = con.cursor()
                    cur.execute('''
                    INSERT INTO challenge_submission 
                    (user_id, level, created_at)
                    VALUES (:user_id, :level, :created_at)
                    ''', entry)
                    print("Added challenge clear")

                    with open(task_queue_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    data.append({
                        'type': 'challenge clear',
                        'submitted_at': created_at,
                        'user_id': user_id,
                        'level': level
                    })
                    with open(task_queue_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    print("Added task")

                    level_list = [f"SELECT '{int(ch_info_list[0])}-{i}' AS id" for i in range(1, 6)]
                    cte_q = ' UNION ALL '.join(level_list)

                    query = f'''
                        WITH target_ids(id) AS (
                            {cte_q}
                        )
                        SELECT
                            t.id,
                            CASE WHEN lc.level IS NOT NULL THEN 1 ELSE 0 END AS e
                        FROM target_ids t
                        LEFT JOIN challenge_submission lc ON t.id = lc.level;
                    '''
                    cur.execute(query)

                    lst = cur.fetchall()

                    if all([dict(_)['e'] for _ in lst]):
                        print("****************************************\n"
                              "Don't forget to change tier role"
                              "****************************************\n")
                        with open(task_queue_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        data.append({
                            'type': 'tier up',
                            'submitted_at': created_at,
                            'user_id': user_id,
                            'tier': int(ch_info_list[0]),
                        })
                        with open(task_queue_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                        print("Added task")
                    con.commit()
                    print("Committed")

            else: print("Invalid input (part)")

        elif cmd == '2':
            print("---------- /challenges/delete_challenge_level_clear ---------- \n")
            progress_id = input("Type progress_id: ")

            if progress_id.isdigit():
                con = create_connection()
                cur = con.cursor()
                cur.execute('''SELECT EXISTS (SELECT 1 FROM collab_quest_progress WHERE id = ?)''', (int(progress_id),))
                if cur.fetchone()[0]:
                    s = "Which column to change \n(" + ", ".join(columns) + ") \n:"
                    target = input(s)
                    if target == 'level_clear_id':
                        change = input("Change into (only digit): ")
                        if change.isdigit():
                            cur.execute(f'''
                                UPDATE collab_quest_progress SET {target} = ? WHERE id = ?
                                ''', (int(change), int(progress_id)))
                            con.commit()
                            print("Updated progress")
                        else: print("Invalid input (only digit)")
                    elif target == 'part':
                        change = input("Change into: ")
                        part_list = change.split("-")
                        if len(part_list) == 3 and (part_list[0].isdigit() and part_list[1].isalpha() and part_list[2].isdigit()):
                            cur.execute(f'''
                                UPDATE quests SET {target} = ? WHERE id = ?
                                ''', (change, int(progress_id)))
                            con.commit()
                            print("Updated progress")
                    elif target == 'video':
                        change = input("Change into: ")
                        cur.execute(f'''
                            UPDATE collab_quest_progress SET {target} = ? WHERE id = ?
                            ''', (change, int(progress_id)))
                        con.commit()
                        print("Updated progress")
                    elif target == 'created_at':
                        change = input("Change into: ")
                        try:
                            datetime.datetime.strptime(change, "%Y-%m-%d %H:%M:%S")
                            cur.execute(f'''
                                UPDATE collab_quest_progress SET {target} = ? WHERE id = ?
                                ''', (change, int(progress_id)))
                            con.commit()
                            print("Updated progress")
                        except ValueError: print("Invalid date format")
                    else: print("Invalid column name")
                else: print("Progress does not exist")
            else: print("Invalid input (only digit)")



def main():
    while True:
        print("---------- / ---------- \n"
              "1. users \n"
              "2. clears \n"
              "3. levels \n"
              "4. quests \n"
              "5. collab \n"
              "6. challenges \n"
              "0. exit \n")

        cmd = input("> ")

        if cmd == "0": break
        elif cmd == "1": users()
        elif cmd == "2": clears()
        elif cmd == "3": levels()
        elif cmd == "4": quests()
        elif cmd == "5": collab()
        elif cmd == "6": challenges()


main()
create_connection().close()