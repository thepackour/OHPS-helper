import json

from ConnFactory import with_connection
from main.db import NoSuchUser
from main.msgformat import requirement_list


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


@with_connection
def quest_data_constructor(cursor, quest: dict):
    stars = quest['stars']
    req = requirement_list[quest['req']]

    cursor.execute('''SELECT * FROM levels WHERE quest_id = ?''', quest['id'])
    level_rows = cursor.fetchall()
    level_list = [dict(row) for row in level_rows]

    level_s = ""
    latest_s = ""
    for i, level in enumerate(level_list, start=1):
        level_s += f"**Level #{i}** \n"
        level_s += f"{level['artist']} - {level['song']} (by {level['creator']}) ({level['exp']} EXP) \n"

        cursor.execute('''
        SELECT * FROM level_clears 
        WHERE level_id = ? 
        ORDER BY id DESC
        LIMIT 1;
        ''', level['id'])
        latest_clear_row = cursor.fetchone()
        if latest_clear_row:
            latest_clear_dict = dict(latest_clear_row)
            cursor.execute('''
            SELECT * FROM users 
            WHERE id = ? 
            ''', latest_clear_dict['user_id'])
            user_row = cursor.fetchone()[0]
            if user_row:
                u = dict(user_row)
                latest_s += f"Level #{i} : {u['username']}\n"
            else:
                latest_s += f"Level #{i} : none\n"
                raise NoSuchUser()
        else:
            latest_s += f"Level #{i} : none\n"

    cursor.execute('''
    SELECT * FROM quest_clears 
    WHERE quest_id = ? 
    ORDER BY id
    ''', quest['id'])
    user = cursor.fetchone()[0]

    if user:
        u = dict(user)
        latest_s += f"All Clear : {u['username']}\n"
    else:
        latest_s += f"All Clear : none\n"


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

    cursor.execute('''SELECT * FROM levels WHERE quest_id = ?''', quest['id'])
    level_rows = cursor.fetchall()
    level_list = [dict(row) for row in level_rows]

    level_s = ""
    for i, level in enumerate(level_list, start=1):
        level_s += f"**Level #{i}** \n"
        level_s += f"{level['artist']} - {level['song']} (by {level['creator']}) ({level['exp']} EXP) \n"

        cursor.execute('''SELECT * FROM level_clears WHERE level_id = ?''', level['id'])
        level_clears_rows = cursor.fetchall()
        level_clears_dict_list = [dict(row) for row in level_clears_rows]
        tmp = []
        for level_clear_dict in level_clears_dict_list:
            cursor.execute('''SELECT * FROM collab_quest_progress WHERE level_clear_id = ? ''', int(level_clear_dict['id']))
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
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    name = data['name'] + "~ " + data['period'].split("~")
    stars = data['stars']
    period = data['period']
    desc = data['desc_kor'] + "\n" + data['desc_eng']
    req = data['req_kor'] + "\n" + data['req_eng']

    level_s = f"{data['artist']} - {data['song']} ({data['exp']} EXP))"
    clears_s = ""
    level_id = data['level_id']

    cursor.execute('''
            SELECT * FROM level_clears 
            WHERE level_id = ? 
            ORDER BY id DESC
            ''', level_id)
    latest_clears_row_list = cursor.fetchall()
    if latest_clears_row_list:
        latest_clears_dict_list = [dict(row) for row in latest_clears_row_list]
        i = 1
        for clear in latest_clears_dict_list:
            cursor.execute('''
                    SELECT * FROM users 
                    WHERE id = ? 
                    ''', clear['user_id'])
            user_row = cursor.fetchone()[0]
            if user_row:
                u = dict(user_row)
                clears_s += f"#{i} : {u['username']}\n"
                i += 1
            else:
                raise NoSuchUser()
    else: clears_s += "none\n"

    return {
        'name': name,
        'stars': stars,
        'period': period,
        'req': req,
        'desc': desc,
        'level': level_s,
        'clears': clears_s
    }