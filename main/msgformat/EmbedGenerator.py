import discord
import datetime

from main.calc import minEXP
import main.db as db
from main.db.QuestDataConstructor import *
from main.msgformat.variables import *
import main.debug as debug


class InvalidQuestType(Exception):
    def __str__(self):
        return "Invalid quest type"


def profile_embed(type: str, user: dict):
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
            value=user['level'],
            inline=False
        )
        embed.add_field(
            name="총 경험치ㅣTotal EXP",
            value=user['exp'],
            inline=False
        )
        embed.add_field(
            name="다음 레벨까지 남은 경험치ㅣEXP left until next level",
            value=minEXP(user['level'])-user['exp'],
            inline=False
        )
        return embed
    elif type == 'quest': # datebase 사용
        try:
            level_clear_list = db.find_level_clears(user['id'])
            quest_clear_list = db.find_quest_clears(user['id'])

            level_id_list = [clear['level_id'] for clear in level_clear_list]
            quest_id_list = [clear['quest_id'] for clear in level_clear_list]

            level_list = db.find_levels(level_id_list)
            quest_list = db.find_levels(quest_id_list)
        except Exception as e:
            debug.log("Failed to generate profile_embed", e=e)

        s = ""
        last_clear = "none"
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
        else: s = "none"

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

            level_id_list = [clear['level_id'] for clear in level_clear_list]
            quest_id_list = [clear['quest_id'] for clear in level_clear_list]

            level_list = db.find_levels(level_id_list)
            quest_list = db.find_levels(quest_id_list)
        except Exception as e:
            debug.log("Failed to generate profile_embed", e=e)

        s = ""
        last_clear = "none"
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
            s = "none"

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
            value=user['level'],
            inline=False
        )
        embed.add_field(
            name="총 경험치ㅣTotal EXP",
            value=user['exp'],
            inline=False
        )
        embed.add_field(
            name="다음 레벨까지 남은 경험치ㅣEXP left until next level",
            value=minEXP(user['level']) - user['exp'],
            inline=False
        )
        embed.add_field(
            name="레벨ㅣLevel",
            value=user['level'],
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


def quest_embed(quest: dict): # database 사용
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
            name="레벨ㅣLevel",
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
    return embed


def leaderboard_embed():
    samples = db.get_all_users()
    rank_s = ""
    username_s = ""
    level_s = ""

    for i, user in enumerate(samples, start=1):
        if i > 20: break;
        rank_s += f"#{i}\n"
        username_s += f"{user['username']}\n"
        level_s += f"{user['level']}\n"

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