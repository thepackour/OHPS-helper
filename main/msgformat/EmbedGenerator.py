import discord
import datetime

from main.calc import minEXP
#from main.db import find_level_clears, find_levels, find_quest_clears
import main.db as db
from main.db.QuestCmd import *

tier4 = {'name': "Tier 4ㅣδelta",
             'color': 0x00D166}
tier3 = {'name': "Tier 3ㅣγamma",
             'color': 0xF8C300}
tier2 = {'name': "Tier 2ㅣβeta",
             'color': 0xF93A2F}
tier1 = {'name': "Tier 1ㅣαlpha",
             'color': 0xFD0061}
tier_not_found = {
        'name': "Not found",
        'color': 0x808080
}

# ex) 3 티어 dict == tier_list[3]
tier_list = tier_not_found, tier1, tier2, tier3, tier4

# ex) 3성 hex코드 == stars_colour_list[3]
stars_colour_list = 0x808080, 0xbfbfff, 0xbfffbf, 0xffffbf, 0xffdfbf, 0xffbfbf

requirement_list = (
    None,
    "한손 클리어\nOne-handed Clear",
    "한손 완벽한 플레이\nOne-handed Pure Perfect",
    "한손 3키 클리어\nOne-handed 3 key clear"
)


class InvalidQuestType(Exception):
    def __str__(self):
        return "Invalid quest type"



def _console_log(message: str, data_dict: dict = None):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[EmbedGenerator] ({now}) | {message}")
    if data_dict:
        for key, value in data_dict.items():
            print(f"{key}: {value} \n")


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
            _console_log(f"Failed to generate profile_embed ({e})")

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
        embed = discord.Embed(
            title=data['name'],
            description=data['stars'],
            colour=stars_colour_list[data['stars']]
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
            value=data['exp'],
            inline=False
        )
        embed.add_field(
            name="최근 클리어자 목록ㅣRecent Clear List",
            value=data['latest_clear'],
            inline=False
        )
        return embed
    elif quest['type'] == 1:
        data = collab_quest_data_constructor(quest)
        embed = discord.Embed(
            title=data['name'],
            description=data['stars'],
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
            value=data['exp'],
            inline=False
        )
    elif quest['type'] == 2:
        data = event_quest_data_constructor(quest)
        embed = discord.Embed(
            title=data['name'],
            description=data['stars'],
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
            name="클리어자 목록ㅣClear List",
            value=data['clears'],
            inline=False
        )
    else: raise InvalidQuestType()


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