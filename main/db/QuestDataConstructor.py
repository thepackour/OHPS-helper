from main.db.ConnFactory import with_connection
from main.db import NoSuchUser, NoSuchLevel
from main.msgformat.variables import requirement_list
import main.debug as debug


number_of_collab_parts = {
    '7' : (
        None,
        {'A': 8, 'B': 14},
        None,
        {'A': 9, 'B': 5},
        None
    ),

    '15' : (
        None,
        None,
        None,
        None,
        None
    )

}


def _part_parse(part: str):
    return tuple(part.split('-'))


def _str_constructor(level: dict):
    s = ""
    if level['artist']: s += f"{level['artist']} - "
    s += f"{level['song']} "
    if level['creator']: s += f"(by {level['creator']}) "
    s += f"({level['exp']} EXP) \n"
    return s


@with_connection
def quest_data_constructor(cursor, quest: dict):
    stars = quest['stars']
    req = requirement_list[quest['req']]

    cursor.execute('''SELECT * FROM levels WHERE quest_id = :id''', quest)
    level_rows = cursor.fetchall()
    if not level_rows:
        debug.log(f"Failed to find levels by quest_id: {quest['id']}", level_rows)
        raise NoSuchLevel()
    debug.log(f"Successfully found levels by quest_id: {quest['id']}", level_rows)
    level_list = [dict(row) for row in level_rows]

    level_s = ""
    latest_s = ""
    for i, level in enumerate(level_list, start=1):
        level_s += f"**Level #{i}** \n"
        level_s += _str_constructor(level)

        cursor.execute('''
        SELECT * FROM level_clears 
        WHERE level_id = :id 
        ORDER BY id DESC
        LIMIT 1;
        ''', level)
        latest_clear_row = cursor.fetchone()
        if latest_clear_row is None:
            debug.log(f"Failed to find latest level clear by level_id: {level['id']}", latest_clear_row)
            latest_s += f"Level #{i} : none\n"
        else:
            debug.log(f"Successfully found latest level clear by level_id: {level['id']}", latest_clear_row)
            latest_clear_dict = dict(latest_clear_row)
            cursor.execute('''
            SELECT * FROM users 
            WHERE id = :user_id 
            ''', latest_clear_dict)
            user_row = cursor.fetchone()
            if user_row:
                debug.log(f"Successfully found user by user_id: {latest_clear_dict['user_id']}", user_row)
                u = dict(user_row)
                latest_s += f"Level #{i} : {u['username']}\n"
            else:
                debug.log(f"Failed to find user by user_id: {latest_clear_dict['user_id']} (Maybe logic error)", user_row)
                latest_s += f"Level #{i} : none\n"
                raise NoSuchUser()

    cursor.execute('''
    SELECT * FROM quest_clears 
    WHERE quest_id = :id 
    ORDER BY id
    LIMIT 1;
    ''', quest)
    latest_quest_clear_row = cursor.fetchone()

    if latest_quest_clear_row is None:
        debug.log(f"Failed to find latest quest clear by quest_id: {quest['id']}", latest_quest_clear_row)
        latest_s += f"All Clear : none\n"
    else:
        latest_quest_clear = dict(latest_quest_clear_row)
        cursor.execute('''
                        SELECT * FROM users 
                        WHERE id = :user_id 
                        ''', latest_quest_clear)
        user_row = cursor.fetchone()
        if user_row is None:
            debug.log(f"(Maybe logic error) Failed to find user by user_id: {latest_quest_clear['user_id']} (from latest_quest_clear)", user_row)
            raise NoSuchUser()
        debug.log(
            f"Successfully found user by user_id: {latest_quest_clear['user_id']} (from latest_quest_clear)", user_row)
        u = dict(user_row)
        latest_s += f"All Clear : {u['username']}\n"

    return {
        'name': quest['name'],
        'stars': stars,
        'req': req,
        'levels': level_s,
        'exp': quest['exp'],
        'latest_clear': latest_s
    }


@with_connection
def collab_quest_data_constructor(cursor, quest: dict):
    stars = quest['stars']
    desc = "아래에서 자신이 원하는 파트를 골라 한손으로 플레이합니다. 단, 각 행마다 하나의 파트만 도전할 수 있으며, 한 행의 모든 파트가 제출되면 완성본 영상이 업로드되고 진행도가 리셋됩니다.\n"\
           "Play the segments you want below with one hand. One player can try only one part on each row. When all the segments in a row are submitted, the completion video will be uploaded, and the progress will be reset."

    cursor.execute('''SELECT * FROM levels WHERE quest_id = :id''', quest)
    level_rows = cursor.fetchall()
    level_list = [dict(row) for row in level_rows]

    level_s = ""
    for i, level in enumerate(level_list, start=1):
        level_s += f"**Level #{i}** \n"
        level_s += f"{level['artist']} - {level['song']} (by {level['creator']}) ({level['exp']} EXP) \n"

        cursor.execute('''SELECT * FROM level_clears WHERE level_id = :id''', level)
        level_clears_rows = cursor.fetchall()
        level_clears_dict_list = [dict(row) for row in level_clears_rows]
        tmp = []
        for level_clear_dict in level_clears_dict_list:
            cursor.execute('''SELECT * FROM collab_quest_progress WHERE level_clear_id = ? ''', (int(level_clear_dict['id']),))
            tmp = cursor.fetchall()
        collab_quest_progress_list = [dict(row) for row in tmp]
        collab_quest_progress_list.sort(key=lambda x: x['part']) # level_id 오름차순, part 오름차순

        A_l = ['□' for i in range(number_of_collab_parts[quest['id']][i]['A'])]
        B_l = ['□' for i in range(number_of_collab_parts[quest['id']][i]['B'])]
        for progress in collab_quest_progress_list:
            level, AorB, part = _part_parse(progress['part'])
            if AorB == 'A': A_l[int(AorB)] = '■'
            elif AorB == 'B': B_l[int(AorB)] = '■'
        A_s = " ".join(A_l)
        B_s = " ".join(B_l)

        level_s += "A Typeㅣ" + A_s
        level_s += "B Typeㅣ" + B_s
        level_s += "\n"

    return {
        'name': quest['name'],
        'stars': stars,
        'desc': desc,
        'levels': level_s,
        'exp': quest['exp'],
    }


### EVENT QUEST SETTING ###
@with_connection
def event_quest_data_constructor(cursor, quest: dict):
    quest_info = quest['json']['quest']
    name = quest_info['name'] + "(~ " + quest_info['period'].split("~")[1] + ")"
    stars = quest_info['stars']
    period = quest_info['period']
    desc = quest_info['desc_kor'] + "\n" + quest_info['desc_eng']
    req = quest_info['req_kor'] + "\n" + quest_info['req_eng']
    exp = quest_info['exp']

    level_list = quest['json']['levels']
    level_s = ""
    level_clears_s = ""
    quest_clears_s = ""
    level_id_list = []
    user_memory = {} # key: user_id , value: u
    for i, level in level_list.items():
        level_id_list.append(level['level_id'])
        level_s += f"**Level #{i}** \n"
        level_s += _str_constructor(level)

        cursor.execute('''
            SELECT * FROM level_clears 
            WHERE level_id = :level_id 
            ORDER BY id ASC
            ''', level['level_id'])
        level_clears_s += f"- Level #{i}\n"
        level_clears_rows = cursor.fetchall()
        if level_clears_rows:
            debug.log(f"Successfully found level clears by level_id: {level['level_id']}", level_clears_rows)
            level_clears_list = [dict(row) for row in level_clears_rows]

            for clear in level_clears_list:
                if clear['user_id'] not in user_memory:
                    cursor.execute('''
                        SELECT * FROM users 
                        WHERE id = :user_id 
                        ''', clear)
                    user_row = cursor.fetchone()
                    if user_row is None:
                        debug.log(f"Failed to find user by user_id: {clear['user_id']} (Maybe logic error)",
                                  user_row)
                        raise NoSuchUser()
                    else:
                        u = dict(user_row)
                        user_memory[u['id']] = u
                        level_clears_s += f"{u['username']}\n"
                        debug.log(f"Successfully found user by user_id: {clear['user_id']}", u)
                else:
                    u = user_memory[clear['user_id']]
                    level_clears_s += f"- {u['username']}\n"
        else:
            debug.log(f"Failed to find level clears by quest_id: {quest_info['quest_id']}", level_clears_rows)
            level_clears_s += f"none\n"
        level_clears_s += "\n"

    cursor.execute('''
                SELECT * FROM quest_clears 
                WHERE quest_id = :quest_id 
                ORDER BY id ASC
                ''', quest_info)
    quest_clears_rows = cursor.fetchall()
    if quest_clears_rows:
        debug.log(f"Successfully found quest clear by quest_id: {quest_info['quest_id']}", quest_clears_rows)
        quest_clears_list = [dict(row) for row in quest_clears_rows]
        try:
            for clear in quest_clears_list:
                u = user_memory[clear['user_id']]
                quest_clears_s += f"{u['username']}\n"
        except Exception as e:
            debug.log("Exception while making quest_clears_s", e)
            raise e
    else:
        debug.log(f"Failed to find quest clear by quest_id: {quest_info['quest_id']}", quest_clears_rows)
        quest_clears_s = "none\n"
    quest_clears_s += "\n"

    return {
        'name': name,
        'stars': stars,
        'period': period,
        'req': req,
        'desc': desc,
        'level': level_s,
        'exp': exp,
        'level_clears': level_clears_s,
        'quest_clears': quest_clears_s
    }
