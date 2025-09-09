import discord
import datetime

import numpy

import main.calc as calc
import main.db as db
from main.calc import EXPtoLevel
from main.db.QuestDataConstructor import *
from main.msgformat.variables import *
import main.debug as debug


class InvalidQuestType(Exception):
    def __str__(self):
        return "Invalid quest type"


async def profile_embed(type: str, user: dict):
    if type == 'level':
        embed = discord.Embed(
            title="유저 프로필ㅣUser Profile",
            description="< 레벨ㅣLevel >",
            colour=tier_list[user['tier']]['color']
        )
        embed.set_thumbnail(url=user['image_url'])
        embed.add_field(
            name="Username",
            value=user['username'],
            inline=False
        )
        embed.add_field(
            name="레벨ㅣLevel",
            value=int(calc.EXPtoLevel(user['exp'])),
            inline=False
        )
        embed.add_field(
            name="총 경험치ㅣTotal EXP",
            value=user['exp'],
            inline=False
        )
        embed.add_field(
            name="다음 레벨까지 남은 경험치ㅣEXP left until next level",
            value=int(numpy.subtract(calc.minEXP(calc.EXPtoLevel(user['exp']) + 1), user['exp'])),
            inline=False
        )
        return embed
    elif type == 'quest': # datebase 사용
        level_list = []
        level_clear_list = []
        quest_list = []
        quest_clear_list = []
        try:
            level_clear_list = db.find_level_clears(user['id'])
            quest_clear_list = db.find_quest_clears(user['id'])

            if level_clear_list:
                level_id_list = [clear['level_id'] for clear in level_clear_list]
                level_list = db.find_levels(level_id_list)
            else: level_list = []


            if quest_clear_list:
                quest_id_list = [clear['quest_id'] for clear in level_clear_list]
                quest_list = db.find_levels(quest_id_list)
            else: quest_list = []

        except Exception as e:
            debug.log("Failed to generate profile_embed", e=e)

        s = ""
        last_clear = "None"
        if level_list:
            for clear in level_clear_list:
                s += quest_list[clear['quest_id']]['name']
                s += "ㅣ"
                s += level_list[clear['level_id']]['artist']
                s += " - "
                s += level_list[clear['level_id']]['song']
                s += "\n"

            last_clear = s.split('\n')[-2] if s else "none"

            if quest_list:
                for clear in quest_clear_list:
                    s += quest_list[clear['quest_id']]['name']
                    s += "ㅣAll Clear\n"
        else:
            s = "None"
            last_clear = "None"

        embed = discord.Embed(
            title="유저 프로필ㅣUser Profile",
            description="< 퀘스트ㅣQuest >",
            colour=tier_list[user['tier']]['color']
        )
        embed.set_thumbnail(url=user['image_url'])

        embed.add_field(
            name="Username",
            value=user['username'],
            inline=False
        )
        embed.add_field(
            name="마지막으로 완료한 퀘스트ㅣLastly Completed Quest",
            value=last_clear,
            inline=False
        )
        embed.add_field(
            name="클리어한 퀘스트ㅣCompleted Quests",
            value=s,
            inline=False
        )
        return embed
    elif type == "play":
        embed = discord.Embed(
            title="유저 프로필ㅣUser Profile",
            description="< 플레이 방식ㅣPlaying Style >",
            colour=tier_list[user['tier']]['color']
        )
        embed.set_thumbnail(url=user['image_url'])
        embed.add_field(
            name="Username",
            value=user['username'],
            inline=False
        )

        embed.add_field(
            name="사용하는 손ㅣMain Hand",
            value=user['main_hand'],
            inline=False
        )
        embed.add_field(
            name="사용하는 키 개수ㅣNumber of Keys",
            value=user['number_of_keys'],
            inline=False
        )
        embed.add_field(
            name="계단 방향ㅣMultiple Input Direction",
            value=user['multi_input_direction'],
            inline=False
        )
        embed.add_field(
            name="세부사항ㅣDetails",
            value=user['details'],
            inline=False
        )
        return embed
    elif type == 'all':  # datebase 사용
        try:
            level_clear_list = db.find_level_clears(user['id'])
            quest_clear_list = db.find_quest_clears(user['id'])

            if level_clear_list:
                level_id_list = [clear['level_id'] for clear in level_clear_list]
                level_list = db.find_levels(level_id_list)
            else: level_list = []

            if quest_clear_list:
                quest_id_list = [clear['quest_id'] for clear in level_clear_list]
                quest_list = db.find_levels(quest_id_list)
            else: quest_list = []

        except Exception as e:
            debug.log("Failed to generate profile_embed", e=e)

        s = ""
        last_clear = "None"
        if level_list:
            for clear in level_clear_list:
                s += quest_list[clear['quest_id']]['name']
                s += "ㅣ"
                s += level_list[clear['level_id']]['artist']
                s += " - "
                s += level_list[clear['level_id']]['song']
                s += "\n"

            last_clear = s.split('\n')[-2] if s else "None"

            if quest_list:
                for clear in quest_clear_list:
                    s += quest_list[clear['quest_id']]['name']
                    s += "ㅣAll Clear\n"
        else:
            s = "None"
            last_clear = "None"

        embed = discord.Embed(
            title="유저 프로필ㅣUser Profile",
            description="< 모두ㅣAll >",
            colour=tier_list[user['tier']]['color']
        )
        embed.set_thumbnail(url=user['image_url'])

        embed.add_field(
            name="Username",
            value=user['username'],
            inline=False
        )
        embed.add_field(
            name="레벨ㅣLevel",
            value=int(calc.EXPtoLevel(['level'])),
            inline=False
        )
        embed.add_field(
            name="총 경험치ㅣTotal EXP",
            value=user['exp'],
            inline=False
        )
        embed.add_field(
            name="다음 레벨까지 남은 경험치ㅣEXP left until next level",
            value=int(numpy.subtract(calc.minEXP(calc.EXPtoLevel(user['exp']) + 1), user['exp'])),
            inline=False
        )
        embed.add_field(
            name="레벨ㅣLevel",
            value=int(calc.EXPtoLevel(user['exp'])),
            inline=False
        )
        embed.add_field(
            name="마지막으로 완료한 퀘스트ㅣLastly Completed Quest",
            value=last_clear,
            inline=False
        )
        embed.add_field(
            name="클리어한 퀘스트ㅣCompleted Quests",
            value=s,
            inline=False
        )
        embed.add_field(
            name="사용하는 손ㅣMain Hand",
            value=user['main_hand'],
            inline=False
        )
        embed.add_field(
            name="사용하는 키 개수ㅣNumber of Keys",
            value=user['number_of_keys'],
            inline=False
        )
        embed.add_field(
            name="계단 방향ㅣMultiple Input Direction",
            value=user['multi_input_direction'],
            inline=False
        )
        embed.add_field(
            name="세부사항ㅣDetails",
            value=user['details'],
            inline=False
        )
        return embed
    return None


async def quest_embed(quest): # database 사용
    if type(quest) is dict:
        if quest['type'] == 0:
            data = quest_data_constructor(quest)
            stars = data['stars']
            difficulty = f"Difficulty : {stars} "
            difficulty += "star" if stars == 1 else "stars"
            embed = discord.Embed(
                title=data['name'],
                description=difficulty,
                colour=stars_colour_list[stars]
            )
            embed.add_field(
                name="조건ㅣRequirement",
                value=data['req'],
                inline=False
            )
            embed.add_field(
                name="레벨ㅣLevels",
                value=data['levels'],
                inline=False
            )
            embed.add_field(
                name="올클리어 보상ㅣAll Clear Reward",
                value=f"{data['exp']} EXP",
                inline=False
            )
            embed.add_field(
                name="최근 클리어자 목록ㅣRecent Clear List",
                value=data['latest_clear'],
                inline=False
            )
        elif quest['type'] == 1:
            data = collab_quest_data_constructor(quest)
            stars = data['stars']
            difficulty = f"Difficulty : {stars} "
            difficulty += "star" if stars == 1 else "stars"
            embed = discord.Embed(
                title=data['name'],
                description=difficulty,
                colour=stars_colour_list[data['stars']]
            )
            embed.add_field(
                name="설명ㅣDescription",
                value=data['desc'],
                inline=False
            )
            embed.add_field(
                name="레벨ㅣLevels",
                value=data['levels'],
                inline=False
            )
            embed.add_field(
                name="올클리어 보상ㅣAll Clear Reward",
                value=f"{data['exp']} EXP",
                inline=False
            )
        elif quest['type'] == 2:
            data = event_quest_data_constructor(quest)
            stars = data['stars']
            difficulty = f"Difficulty : {stars} "
            difficulty += "star" if stars == 1 else "stars"
            embed = discord.Embed(
                title=data['name'],
                description=difficulty,
                colour=0xffa0ff
            )
            embed.add_field(
                name="이벤트 기간ㅣEvent Period",
                value=data['period'],
                inline=False
            )
            embed.add_field(
                name="설명ㅣDescription",
                value=data['desc'],
                inline=False
            )
            embed.add_field(
                name="조건ㅣRequirement",
                value=data['req'],
                inline=False
            )
            embed.add_field(
                name= "레벨ㅣLevels" if len(data['level'].split("\n")) == 1 else "레벨ㅣLevel",
                value=data['level'],
                inline=False
            )
            embed.add_field(
                name="올클리어 보상ㅣAll Clear Reward",
                value=f"{data['exp']} EXP",
                inline=False
            )
            embed.add_field(
                name="클리어자 목록ㅣClear List",
                value=data['level_clears'],
                inline=False
            )
            embed.add_field(
                name="올클리어자 목록ㅣAll Clear List",
                value=data['quest_clears'],
                inline=False
            )
        else: raise InvalidQuestType()
    elif type(quest) is int:
        if 1 <= quest <= 5:
            data = db.find_quests_by_stars(quest)
            event_info = db.get_event_info()

            difficulty = f"Difficulty : {quest} "
            difficulty += "star" if quest == 1 else "stars"
            embed = discord.Embed(
                title="퀘스트 목록ㅣQuest List",
                description=difficulty,
                color=stars_colour_list[quest]
            )
            name_s = "\n"
            exp_s = "\n"
            for quest_dict in data:
                if (quest_dict['type'] == 2) and event_info is None: continue
                name_s += quest_dict['name'] + "\n\n"
                levels_list = db.find_levels(quest_dict['id'])
                exp_list = [level['exp'] for level in levels_list]
                exp_min, exp_max = min(exp_list), max(exp_list)
                exp_s += f"{exp_min} - {exp_max}   ({quest_dict['exp']})\n\n"

            embed.add_field(
                name="퀘스트ㅣQuest",
                value=name_s,
                inline=True
            )
            embed.add_field(
                name="EXP",
                value=exp_s,
                inline=True
            )
        else: raise db.NoSuchDifficulty()

    else: raise TypeError
    return embed


async def leaderboard_embed():
    samples = db.get_all_users()
    rank_s = ""
    username_s = ""
    # exp_s = ""
    level_s = ""

    for i, user in enumerate(samples, start=1):
        if i > 20: break;
        rank_s += f"#{i}\n"
        username_s += f"{user['username']}\n"
        # exp_s += f"{user['exp']}\n"
        level_s += f"{int(calc.EXPtoLevel(user['exp']))}\n"

    embed = discord.Embed(
        title="레벨 랭킹ㅣLevel Leaderboard",
        colour=0x00ffff
    )
    embed.add_field(
        name="Rank",
        value=rank_s,
        inline=True
    )
    embed.add_field(
        name="Player",
        value=username_s,
        inline=True
    )
    embed.add_field(
        name="Level",
        value=level_s,
        inline=True
    )
    return embed


async def notice_embed(entry: dict):
    try:
        if entry['type'] == 'level clear':
            q = db.find_quest_by_id(entry['quest_id'])
            embed = discord.Embed(
                title='레벨 클리어ㅣLevel Clear',
                description=f'Submitted on {entry['submitted_at']}',
                color=stars_colour_list[q['stars']]
            )
            embed.add_field(
                name="플레이어 이름ㅣPlayer name",
                value=db.find_user(entry['user_id'])['name'],
                inline=True
            )
            exp_s = f"{entry['exp_before']} EXP → {entry['exp_after']} EXP (+{entry['exp_after'] - entry['exp_before']})"
            if EXPtoLevel(entry['exp_after']) > EXPtoLevel(entry['exp_before']):
                exp_s += f"\n{EXPtoLevel(entry['exp_before'])} Level → {EXPtoLevel(entry['exp_after'])} Level"
            embed.add_field(
                name="경험치 & 레벨ㅣEXP & Level",
                value=exp_s,
                inline=True
            )
            embed.add_field(
                name="퀘스트 이름ㅣQuest name",
                value=q['name'],
                inline=True
            )
            played_level = db.find_level(entry['quest_id'])
            embed.add_field(
                name="플레이한 레벨ㅣPlayed level",
                value=msgformat.level_str(played_level),
                inline=True
            )

        elif entry['type'] == 'quest clear':
            q = db.find_quest_by_id(entry['quest_id'])
            embed = discord.Embed(
                title='퀘스트 클리어ㅣQuest Clear',
                description=f'Submitted on {entry['submitted_at']}',
                color=stars_colour_list[q['stars']]
            )
            embed.add_field(
                name="플레이어 이름ㅣPlayer name",
                value=db.find_user(entry['user_id'])['name'],
                inline=True
            )
            exp_s = f"{entry['exp_before']} EXP → {entry['exp_after']} EXP (+{entry['exp_after'] - entry['exp_before']})"
            if EXPtoLevel(entry['exp_after']) > EXPtoLevel(entry['exp_before']):
                exp_s += f"\n{EXPtoLevel(entry['exp_before'])} Level → {EXPtoLevel(entry['exp_after'])} Level"
            embed.add_field(
                name="경험치 & 레벨ㅣEXP & Level",
                value=exp_s,
                inline=True
            )
            embed.add_field(
                name="퀘스트 이름ㅣQuest name",
                value=q['name'],
                inline=True
            )

        elif entry['type'] == 'challenge clear':
            t = tier_list[int(entry['level'].split('-')[0])]
            try: l = db.get_challenge_levels()
            except Exception as e: debug.log("Failed to get challenge_levels.json", e=e)
            else:
                embed = discord.Embed(
                    title='챌린지 클리어ㅣChallenge Clear',
                    description=f'Submitted on {entry['submitted_at']}',
                    color=t['color']
                )
                embed.add_field(
                    name="플레이어 이름ㅣPlayer name",
                    value=db.find_user({'id': entry['user_id']})['username'],
                    inline=True
                )
                embed.add_field(
                    name="챌린지 티어ㅣChallenge Tier",
                    value=t['name'],
                    inline=True
                )
                embed.add_field(
                    name="플레이한 레벨ㅣPlayed level",
                    value=msgformat.level_str(l[entry['level']]),
                    inline=True
                )

        elif entry['type'] == 'tear up':
            t_after = tier_list[int(entry['level'].split('-')[0])]
            t_before = tier_list[int(entry['level'].split('-')[0]) + 1]
            embed = discord.Embed(
                title='티어 승급ㅣTier Elevation',
                description=f'Submitted on {entry['submitted_at']}',
                color=t_after['color']
            )
            embed.add_field(
                name="플레이어 이름ㅣPlayer name",
                value=db.find_user(entry['user_id'])['name'],
                inline=True
            )
            embed.add_field(
                name="티어ㅣTier",
                value=f"{t_before} → **{t_after}**",
                inline=True
            )

        else: embed = None
    except Exception as e:
        debug.log("Failed to generate notice_embed", embed, e)
    else:
        debug.log("Successfully generated notice_embed", embed)

    return embed