import gspread
import discord
from discord import app_commands
from discord.ext import commands
import numpy
import datetime
from dotenv import load_dotenv
import os

load_dotenv()


token = os.getenv("TOKEN")
DB = gspread.service_account(filename=os.getenv("KEY")).open("OHPS Server DB")

sheet1 = "User_Profile"
sheet2 = "Quest_List"
sht1 = "퀘스트ㅣQuest"
sheet3 = "Quest_List_Details"
sheet4 = "Event_Quest"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="o!",intents=intents)
bot.help_command = None


def tier_num2nameNcolour(tier):
    if tier == '4':
        return ["Tier 4ㅣδelta", 0x00D166]
    elif tier == '3':
        return ["Tier 3ㅣγamma", 0xF8C300]
    elif tier == '2':
        return ["Tier 2ㅣβeta", 0xF93A2F]
    elif tier == '1':
        return ["Tier 1ㅣαlpha", 0xFD0061]
    else:
        return ["Not found", 0x808080]


def make_embed(title, desc, colour, image_url, row, start, end, arr):
    db_arr = arr
    db_embed = discord.Embed(
        title=title,
        description=desc,
        colour=tier_num2nameNcolour(db_arr[row][5])[1]
    )
    db_embed.set_thumbnail(url=image_url)
    tier_name = tier_num2nameNcolour(db_arr[row][5])[0]
    for cell_n in range(start-1, end+1):
        db_embed.add_field(
            name=db_arr[0][cell_n],
            value=db_arr[row][cell_n] if cell_n != 5 else tier_name,
            inline=False
        )
    return db_embed


def make_embed_l(title, desc, colour, image_url, row, numbers, arr):
    db_arr = arr
    db_embed = discord.Embed(
        title=title,
        description=desc,
        colour=tier_num2nameNcolour(db_arr[row][5])[1]
    )
    db_embed.set_thumbnail(url=image_url)
    tier_name = tier_num2nameNcolour(db_arr[row][5])[0]
    for cell_n in numbers:
        db_embed.add_field(
            name=db_arr[0][cell_n-1],
            value=db_arr[row][cell_n-1] if cell_n-1 != 5 else tier_name,
            inline=False
        )
    return db_embed


def col_only(list, col):
    new_lst = []
    for i in range(0,len(list)):
        new_lst.append(list[i][col])
    return new_lst


def text2star(text):
    filled_star = int(text[0])
    blank_star = 5 - filled_star
    star = ("★"*filled_star) + ("☆"*blank_star)
    return star


def diff2colour(diff):
    if diff == '5 star':
        return 0xffbfbf
    elif diff == '4 star':
        return 0xffdfbf
    elif diff == '3 star':
        return 0xffffbf
    elif diff == '2 star':
        return 0xbfffbf
    elif diff == '1 star':
        return 0xbfbfff
    else:
        return 0x808080


def timestamp():
    now = datetime.datetime.now()
    y = now.year
    m = now.month
    d = now.day
    h = now.hour
    min = now.minute
    s = now.second
    ms = now.microsecond
    return f"{y}.{m}.{d} {h}:{min}:{s}:{ms}"


@bot.event
async def on_ready():
    print("Hello world")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)\n")
        await bot.change_presence(activity=discord.CustomActivity(type=discord.ActivityType.custom, name=f'Running {len(synced)} commands with one hand'))
    except Exception as e:
        print(e)


@bot.event
async def on_app_command_completion(interaction: discord.Interaction, command):
    log_interaction = interaction
    log_command = command
    log_interaction_option = " "
    if 'options' in log_interaction.data:
        for values in log_interaction.data['options']:
            log_interaction_option = log_interaction_option + f"({values['name']} : {values['value']}) "
    print(f"[{timestamp()} | Command] /{log_command.name}\n<{log_interaction.user.name} ({log_interaction.id})> /{log_command.name}{log_interaction_option}\n")


@bot.event
async def on_member_join(member):
    print(f"[{timestamp()} | New User] {member.name} ({member.id})\n")


@bot.event
async def on_message(message):
    developer = [608914438640369676, 433224189194010654]
    channel = bot.get_channel(1199387197963513887)
    dev_channel = [1195221597003456642, 1195037894402908291]
    isDev = (message.author.id in developer) and (message.channel.id in dev_channel)
    segment = message.content.split("/./")
    # [0]: one/all
    # [1]: submit_date
    # [2]: user_id
    # [3]: quest_name
    # [4]: reward_exp
    # [5]: level_name

    if isDev and (message.content == "help"):
        await message.channel.send("one/./[submit_date]/./[user_id]/./[quest_name]/./[reward_EXP]/./[level_name]\n"
                           "all/./[submit_date]/./[user_id]/./[quest_name]/./[reward_EXP]")

    if isDev and (segment[0] == "one"):
        db_arr = DB.worksheet(sheet1).get_all_values()
        clear_arr = DB.worksheet(sheet2).get_all_values()
        print(f"[{timestamp()} | Admin_command] /one")
        for i in segment:
            print(i, end=" / ")
        y = 0
        while str(segment[2]) != db_arr[y][0]:
            y = y + 1
        before_exp = db_arr[y][3]
        before_level = db_arr[y][2]
        DB.worksheet(sheet1).update_cell(y + 1,4,int(before_exp)+int(segment[4]))
        after_exp = DB.worksheet(sheet1).cell(y + 1, 4).value
        after_level = DB.worksheet(sheet1).cell(y + 1, 3).value
        DB.worksheet(sheet1).update_cell(y + 1, 7, f"{segment[3]}ㅣ{segment[5]}")
        yy = 0
        while str(segment[3]) != clear_arr[yy][0]:
            yy = yy + 1
        for i in range(0, int(clear_arr[yy+2][0])):
            if segment[5] == clear_arr[yy+i][1]:
                DB.worksheet(sheet2).update_cell(yy+i+1,4,f'{db_arr[y][1]} ({segment[1]})')
                break
        quest_history = DB.worksheet(sheet1).cell(y+1, 12).value
        if quest_history == 'none':
            quest_history = f'{segment[3]}ㅣ{segment[5]}\n'
        else:
            quest_history = quest_history + f'{segment[3]}ㅣ{segment[5]}\n'
        DB.worksheet(sheet1).update_cell(y+1, 12, quest_history)
        levelup = f"({before_level} Level → {after_level} Level)" if after_level > before_level else f"({after_level} Level)"
        embed = discord.Embed(title="퀘스트 완료ㅣQuest Complete",
                              description=f"Submitted on {segment[1]}",
                              colour=0xffffcf)
        embed.add_field(
            name="플레이어 이름ㅣPlayer name",
            value=db_arr[y][1],
            inline=True
        )
        embed.add_field(
            name="경험치 & 레벨ㅣEXP & Level",
            value=f"{before_exp}EXP → {after_exp}EXP (+{segment[4]})\n{levelup}",
            inline=True
        )
        embed.add_field(
            name="퀘스트 이름ㅣQuest name",
            value=segment[3],
            inline=True
        )
        embed.add_field(
            name="플레이한 레벨ㅣPlayed level",
            value=segment[5],
            inline=True
        )
        await channel.send(f"<@{int(segment[2])}>")
        await channel.send(embed=embed)

    if isDev and (segment[0] == "all"):
        db_arr = DB.worksheet(sheet1).get_all_values()
        clear_arr = DB.worksheet(sheet2).get_all_values()
        print(f"[{timestamp()} | Admin_command] /all")
        for i in segment:
            print(i, end=" / ")
        y = 0
        while str(segment[2]) != db_arr[y][0]:
            y = y + 1
        before_exp = db_arr[y][3]
        before_level = db_arr[y][2]
        DB.worksheet(sheet1).update_cell(y + 1, 4, int(before_exp) + int(segment[4]))
        after_exp = DB.worksheet(sheet1).cell(y + 1, 4).value
        after_level = DB.worksheet(sheet1).cell(y + 1, 3).value
        DB.worksheet(sheet1).update_cell(y + 1, 7, f"{segment[3]} - **All Clear**")
        yy = 0
        while str(segment[3]) != clear_arr[yy][0]:
            yy = yy + 1
        DB.worksheet(sheet2).update_cell(yy + 1, 5, f'{db_arr[y][1]} ({segment[1]})')
        quest_history = DB.worksheet(sheet1).cell(y+1, 12).value
        if quest_history == 'none':
            quest_history = f'{segment[3]}ㅣAll Clear\n'
        else:
            quest_history = quest_history + f'{segment[3]}ㅣAll Clear\n'
        DB.worksheet(sheet1).update_cell(y+1, 12, quest_history)
        levelup = f"({before_level} Level → {after_level} Level)" if after_level > before_level else f"({after_level} Level)"
        embed = discord.Embed(title="퀘스트 올클리어ㅣQuest All Clear",
                              description=f"Submitted on {segment[1]}",
                              colour=0xffff9f)
        embed.add_field(
            name="플레이어 이름ㅣPlayer name",
            value=db_arr[y][1],
            inline=True
        )
        embed.add_field(
            name="경험치 & 레벨ㅣEXP & Level",
            value=f"{before_exp}EXP → {after_exp}EXP (+{segment[4]})\n{levelup}",
            inline=True
        )
        embed.add_field(
            name="퀘스트 이름ㅣQuest name",
            value=segment[3],
            inline=True
        )
        await channel.send(f"<@{int(segment[2])}>")
        await channel.send(embed=embed)

    if (message.author.id in developer) and (segment[0] == 'del'):
        channel.delete_messages()


@bot.tree.command(name="ping", description="현재 봇의 응답속도를 보여줍니다ㅣShows the current latency of the bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! `{bot.latency}ms`")


@bot.tree.command(name="rank", description="서버 내 레벨 순위를 보여줍니다ㅣShows the level leaderboard in the server")
async def rank(interaction: discord.Interaction):
    await interaction.response.defer()
    player_arr = DB.worksheet(sheet1).get_all_values()
    name_level = []
    player_n = len(player_arr)
    rank = ""
    player_value = ""
    level_value = ""
    for i in range(2, player_n):
        name_level.append([player_arr[i][1],player_arr[i][2],int(player_arr[i][3])])
    name_level.sort(key=lambda x: -x[2])
    for i in range (2, 21 if player_n > 20 else player_n):
        rank = rank + f'#{i-1}' + "\n"
    for i in range (2, 21 if player_n > 20 else player_n):
        player_value = player_value + name_level[i-2][0] + "\n"
    for i in range (2, 21 if player_n > 20 else player_n):
        level_value = level_value + name_level[i-2][1] + "\n"

    embed = discord.Embed(
        title="레벨 랭킹ㅣLevel Leaderboard",
        colour=0x00ffff
    )
    embed.add_field(
        name="Rank",
        value=rank,
        inline=True
    )
    embed.add_field(
        name="Player",
        value=player_value,
        inline=True
    )
    embed.add_field(
        name="Level",
        value=level_value,
        inline=True
    )
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="register", description="서버에 등록합니다ㅣRegisters for the server")
async def register(interaction: discord.Interaction):
    await interaction.response.defer()
    if str(interaction.user.id) in DB.worksheet(sheet1).col_values(1):
        await interaction.followup.send("이미 등록된 유저입니다. `/myprofile`에서 프로필을 확인하세요.\n"
                                        "You've been already registered. See your profile with `/myprofile`.")
    else:
        blank = 1
        while DB.worksheet(sheet1).cell(blank, 1).value:
            blank += 1
        DB.worksheet(sheet1).update_cell(col=1, row=blank, value=str(interaction.user.id))
        DB.worksheet(sheet1).update_cell(col=2, row=blank, value=interaction.user.name)
        paste_dest = DB.worksheet(sheet1).cell(col=3, row=blank).address
        DB.worksheet(sheet1).copy_range('C2:L2', paste_dest)
        delta_tier = interaction.guild.get_role(1190699240683487312)
        await interaction.user.add_roles(delta_tier)
        await interaction.followup.send("성공적으로 등록되었습니다! `/myprofile`로 프로필을 볼 수 있습니다!\n"
                                        "Successfully registered! You can view your profile with `/myprofile`!")


@bot.tree.command(name="details", description="타법의 세부사항을 등록합니다.ㅣRegister the detailed info about your play")
@app_commands.describe(
    leftright = "사용하는 손ㅣYour main hand (Left/Right)",
    keys= "사용하는 키ㅣKeys that you use",
    inout = "계단 방향ㅣMultiple input direction (L to R/R to L)",
    details = "기타 세부사항ㅣOther details")
async def details(interaction: discord.Interaction, leftright: str, keys: str, inout: str, details: str):
    await interaction.response.defer()
    if str(interaction.user.id) in DB.worksheet(sheet1).col_values(1):
        user = DB.worksheet(sheet1).find(str(interaction.user.id), in_column=1)
        DB.worksheet(sheet1).update_cell(col=8, row=user.row, value=leftright)
        DB.worksheet(sheet1).update_cell(col=9, row=user.row, value=keys)
        DB.worksheet(sheet1).update_cell(col=10, row=user.row, value=inout)
        DB.worksheet(sheet1).update_cell(col=11, row=user.row, value=details)
        await interaction.followup.send("성공적으로 제출되었습니다! `/myprofile`로 프로필을 볼 수 있습니다!\n"
                                        "Successfully submitted! You can view your profile with `/myprofile`!")
    else:
        await interaction.followup.send("아직 등록되지 않았습니다. `/register`로 등록해주세요!\n"
                                        "You are not registered in the server. `/register` to register!")


@bot.tree.command(name="myprofile", description="당신의 프로필 정보를 보여줍니다ㅣShows your profile's info")
@app_commands.describe(range="표시 범위 선택ㅣRange to show (level/quest/play/all)")
async def myprofile(interaction: discord.Interaction, range: str):
    await interaction.response.defer()
    db_arr = DB.worksheet(sheet1).get_all_values()
    if str(interaction.user.id) in col_only(db_arr, 0):
        user_y = 0
        while db_arr[user_y][0] != str(interaction.user.id):
            user_y = user_y + 1
        if range == "level":
            db_embed = make_embed(
                title="유저 프로필ㅣUser Profile",
                desc="< 레벨ㅣLevel >",
                colour=tier_num2nameNcolour(db_arr[user_y][5])[1],
                image_url=interaction.user.avatar.url,
                row=user_y,
                start=3, end=4,
                arr=db_arr
            )
            await interaction.followup.send(embed=db_embed)
        elif range == "quest":
            db_embed = make_embed_l(
                title="유저 프로필ㅣUser Profile",
                desc="< 퀘스트ㅣQuest >",
                colour=tier_num2nameNcolour(db_arr[user_y][5])[1],
                image_url=interaction.user.avatar.url,
                row=user_y,
                numbers=[7, 12],
                arr=db_arr
            )
            await interaction.followup.send(embed=db_embed)
        elif range == "play":
            db_embed = make_embed(
                title="유저 프로필ㅣUser Profile",
                desc="< 플레이 방식ㅣPlaying Style >",
                colour=tier_num2nameNcolour(db_arr[user_y][5])[1],
                image_url=interaction.user.avatar.url,
                row=user_y,
                start=8, end=10,
                arr=db_arr
            )
            await interaction.followup.send(embed=db_embed)
        elif range == "all":
            db_embed = make_embed_l(
                title="유저 프로필ㅣUser Profile",
                desc="< 모두ㅣAll >",
                colour=tier_num2nameNcolour(db_arr[user_y][5])[1],
                image_url=interaction.user.avatar.url,
                row=user_y,
                numbers=[3,4,5,6,7,12,8,9,10,11],
                arr=db_arr
            )
            await interaction.followup.send(embed=db_embed)
        else:
            await interaction.followup.send("잘못된 입력입니다. 다시 시도해주세요.\nWrong input. Please try again.")

    else:
        await interaction.followup.send("아직 등록되지 않았습니다. `/register`로 등록해주세요!\n"
                                        "You are not registered in the server. `/register` to register!")


@bot.tree.command(name="level", description="입력한 레벨에 관한 정보를 보여줍니다.ㅣShows the info about the level you typed")
@app_commands.describe(level="검색하고 싶은 레벨ㅣThe level you want to know about")
async def level(interaction: discord.Interaction, level: int):
    await interaction.response.defer()
    user = DB.worksheet(sheet1).find(str(interaction.user.id), in_column=1)
    if not user:
        await interaction.followup.send("아직 등록되지 않았습니다. `/register`로 등록해주세요!\nYou are not registered in the server. `/register` to register!")
    elif level <= 0:
        await interaction.followup.send("잘못된 입력입니다. 다시 시도해주세요.\nWrong input. Please try again.")
    else:
        total = numpy.ceil(numpy.divide(numpy.power(1.2, level)-1.2, 0.012))
        difference = numpy.subtract(numpy.divide(numpy.power(1.2, level)-1.2, 0.012), int(DB.worksheet(sheet1).cell(user.row, 4).value))
        if difference >= 0:
            await interaction.followup.send(f"**{level} 레벨** 달성에 필요한 총 경험치는 **{total} EXP**, 현재 경험치보다 **{numpy.ceil(difference)}**만큼 높습니다.\n"
                                            f"The total EXP to reach **{level} level** is **{total} EXP**, **{numpy.ceil(difference)}** higher than your current EXP.")
        else:
            await interaction.followup.send(f"**{level} 레벨** 달성에 필요한 총 경험치는 **{total} EXP**, 현재 경험치보다 **{-1*numpy.ceil(difference)}**만큼 낮습니다.\n"
                                            f"The total EXP to reach **{level} level** is **{total} EXP**, **{-1*numpy.ceil(difference)}** lower than your current EXP.")


@bot.tree.command(name="questlist", description="퀘스트 목록을 보여줍니다ㅣShows the list of Quests")
@app_commands.describe(difficulty="난이도 선택ㅣDifficulty (1~5)")
async def questlist(interaction: discord.Interaction, difficulty: str):
    await interaction.response.defer()
    quest_arr = DB.worksheet(sheet2).get_all_values()
    if difficulty == '1':
        quest_embed = discord.Embed(
            title='퀘스트 목록ㅣQuest List',
            description='Difficulty : 1 Star\n⠀',
            colour=0xbfbfff
        )
        quest_embed.set_footer(text="/quest to see each quest")
        y = 0
        while quest_arr[y][0] != '1 star':
            y = y + 1
        while True:
            quest_numbers = int(quest_arr[y+3][0])
            quests = f'{quest_arr[y+1][1]} ({quest_arr[y+1][2]})'
            for i in range(y+2,y+quest_numbers+1):
                quests = quests + f'\n{quest_arr[i][1]} ({quest_arr[i][2]})'
            quest_embed.add_field(
                name=quest_arr[y+1][0],
                value=f'{quests}\n⠀',
                inline=False
            )
            y = y + quest_numbers
            if quest_arr[y+1][0] == '2 star':
                break
        await interaction.followup.send(embed=quest_embed)
    elif difficulty == '2':
        quest_embed = discord.Embed(
            title='퀘스트 목록ㅣQuest List',
            description='Difficulty : 2 Stars\n⠀',
            colour=0xbfffbf
        )
        quest_embed.set_footer(text="/quest to see each quest")
        y = 0
        while quest_arr[y][0] != '2 star':
            y = y + 1
        while True:
            quest_numbers = int(quest_arr[y+3][0])
            quests = f'{quest_arr[y+1][1]} ({quest_arr[y+1][2]})'
            for i in range(y+2,y+quest_numbers+1):
                quests = quests + f'\n{quest_arr[i][1]} ({quest_arr[i][2]})'
            quest_embed.add_field(
            name = quest_arr[y+1][0],
            value = f'{quests}\n⠀',
            inline = False
            )
            y = y + quest_numbers
            if quest_arr[y+1][0] == '3 star':
                break
        await interaction.followup.send(embed=quest_embed)
    elif difficulty == '3':
        quest_embed = discord.Embed(
            title='퀘스트 목록ㅣQuest List',
            description='Difficulty : 3 Stars\n⠀',
            colour=0xffffbf
        )
        quest_embed.set_footer(text="/quest to see each quest")
        y = 0
        while quest_arr[y][0] != '3 star':
            y = y + 1
        while True:
            quest_numbers = int(quest_arr[y+3][0])
            quests = f'{quest_arr[y+1][1]} ({quest_arr[y+1][2]})'
            for i in range(y+2,y+quest_numbers+1):
                quests = quests + f'\n{quest_arr[i][1]} ({quest_arr[i][2]})'
            quest_embed.add_field(
            name = quest_arr[y+1][0],
            value = f'{quests}\n⠀',
            inline = False
            )
            y = y + quest_numbers
            if quest_arr[y+1][0] == '4 star':
                break
        await interaction.followup.send(embed=quest_embed)
    elif difficulty == '4':
        quest_embed = discord.Embed(
            title='퀘스트 목록ㅣQuest List',
            description='Difficulty : 4 Stars\n⠀',
            colour=0xffdfbf
        )
        quest_embed.set_footer(text="/quest to see each quest")
        y = 0
        while quest_arr[y][0] != '4 star':
            y = y + 1
        while True:
            quest_numbers = int(quest_arr[y+3][0])
            quests = f'{quest_arr[y+1][1]} ({quest_arr[y+1][2]})'
            for i in range(y+2,y+quest_numbers+1):
                quests = quests + f'\n{quest_arr[i][1]} ({quest_arr[i][2]})'
            quest_embed.add_field(
            name = quest_arr[y+1][0],
            value = f'{quests}\n⠀',
            inline = False
            )
            y = y + quest_numbers
            if quest_arr[y+1][0] == '5 star':
                break
        await interaction.followup.send(embed=quest_embed)
    elif difficulty == '5':
        quest_embed = discord.Embed(
            title='퀘스트 목록ㅣQuest List',
            description='Difficulty : 5 Stars\n⠀',
            colour=0xffbfbf
        )
        quest_embed.set_footer(text="/quest to see each quest")
        y = 0
        while quest_arr[y][0] != '5 star':
            y = y + 1
        while True:
            quest_numbers = int(quest_arr[y+3][0])
            quests = f'{quest_arr[y+1][1]} ({quest_arr[y+1][2]})'
            for i in range(y+2,y+quest_numbers+1):
                quests = quests + f'\n{quest_arr[i][1]} ({quest_arr[i][2]})'
            quest_embed.add_field(
            name = quest_arr[y+1][0],
            value = f'{quests}\n⠀',
            inline = False
            )
            y = y + quest_numbers
            if y+3 > len(quest_arr):
                break
        await interaction.followup.send(embed=quest_embed)
    else:
        await interaction.followup.send("잘못된 입력입니다. 다시 시도해주세요.\nWrong input. Please try again.")


@bot.tree.command(name="quest", description="퀘스트 정보를 보여줍니다ㅣShow the info of Quest")
@app_commands.describe(quest = "퀘스트 이름ㅣQuest name")
async def quest(interaction: discord.Interaction, quest: str):
    await interaction.response.defer()
    quest_arr = DB.worksheet(sheet3).get_all_values()
    y = 0
    if quest in col_only(quest_arr, 0):
        while quest_arr[y][0] != quest:
            y = y + 1
        ac_exp = quest_arr[y][1]
        req = quest_arr[y][4]
        if quest_arr[y][3] == 'Collab':
            quests = f'#1 {quest_arr[y + 1][0]} ({quest_arr[y + 1][1]})'
            for i in range(1, int(quest_arr[y][2])):
                quests = quests + f'\n#{i+1} {quest_arr[2*i + y + 1][0]} ({quest_arr[2*i + y + 1][1]})'
            while quest_arr[y][0] not in ['1 star', '2 star', '3 star', '4 star', '5 star']:
                y = y - 1
            quest_embed = discord.Embed(
                title=quest,
                description=f'Difficulty: {text2star(quest_arr[y][0])} (Collab)\n⠀',
                colour=diff2colour(quest_arr[y][0])
            )
            quest_embed.set_footer(text="Please visit OHPS Info sheet for more details")
            progress_arr = quest_arr
            y = 0
            while progress_arr[y][0] != quest:
                y = y + 1
            tmp = progress_arr[y+1]
            del tmp[0:4]
            tmp = list(filter(None, tmp))
            timeframe = ' / '.join(tmp)
            tmp = progress_arr[y+2]
            del tmp[0:4]
            tmp = list(filter(None, tmp))
            timeframe = timeframe + '\n\n' + ' / '.join(tmp)
            progress = [f'⠀\n**Level #1 : {progress_arr[y+1][0]}**\n\n{timeframe}\n⠀']
            for i in range(1, int(progress_arr[y][2])):
                tmp = progress_arr[2*i + y + 1]
                del tmp[0:4]
                tmp = list(filter(None, tmp))
                timeframe = ' / '.join(tmp)
                tmp = progress_arr[2*i + y + 2]
                del tmp[0:4]
                tmp = list(filter(None, tmp))
                timeframe = timeframe + '\n\n' + ' / '.join(tmp)
                progress.append(f'\n\n\n**Level #{i + 1} : {progress_arr[2*i + y + 1][0]}**\n\n{timeframe}\n⠀')
            quest_embed.add_field(
                name='설명ㅣDescription',
                value=f'{req}\n⠀',
                inline=False
            )
            quest_embed.add_field(
                name='레벨ㅣLevels',
                value=f'{quests}\n⠀',
                inline=False
            )
            quest_embed.add_field(
                name='올클리어 보상ㅣAll Clear Reward',
                value=f'{ac_exp}\n⠀',
                inline=False
            )
            quest_embed.add_field(
                name="- 진행도ㅣProgress -",
                value=" ",
                inline=False
            )
            for q in progress:
                quest_embed.add_field(
                    name=" ",
                    value=q,
                    inline=False
                )
            await interaction.followup.send(embed=quest_embed)
        else:
            quests = f'#1 {quest_arr[y + 1][0]} ({quest_arr[y + 1][1]})'
            for i in range(2, int(quest_arr[y][2])+1):
                quests = quests + f'\n#{i} {quest_arr[y + i][0]} ({quest_arr[y + i][1]})'
            while quest_arr[y][0] not in ['1 star', '2 star', '3 star', '4 star', '5 star']:
                y = y - 1
            quest_embed = discord.Embed(
                title=quest,
                description=f'Difficulty: {text2star(quest_arr[y][0])}\n⠀',
                colour=diff2colour(quest_arr[y][0])
            )
            quest_embed.set_footer(text="Please visit OHPS Info sheet for more details")
            clear_arr = DB.worksheet(sheet2).get_all_values()
            y = 0
            while clear_arr[y][0] != quest:
                y = y + 1
            clear = f'Level #1 : {clear_arr[y][3]}'
            for i in range(1, int(clear_arr[y+2][0])):
                clear = clear + f'\nLevel #{i+1} : {clear_arr[y + i][3]}'
            clear = clear + f'\nAll Clear : {clear_arr[y][4]}'
            quest_embed.add_field(
                name='조건ㅣRequirement',
                value=f'{req}\n⠀',
                inline=False
            )
            quest_embed.add_field(
                name=f'레벨ㅣLevels',
                value=f'{quests}\n⠀',
                inline=False
            )
            quest_embed.add_field(
                name='올클리어 보상ㅣAll Clear Reward',
                value=f'{ac_exp}\n⠀',
                inline=False
            )
            quest_embed.add_field(
                name="최근 클리어자 목록ㅣRecent Clear List",
                value=f'{clear}',
                inline=False
            )
            await interaction.followup.send(embed=quest_embed)
    else:
        await interaction.followup.send("퀘스트가 존재하지 않습니다. 다시 시도해주세요.\nThe quest doesn't exist. Please try again.")


@bot.tree.command(name="event", description="이벤트 퀘스트 정보를 보여줍니다ㅣShow the info of Event Quest")
async def event_quest(interaction: discord.Interaction):
    quest_arr = DB.worksheet(sheet4).get_all_values()
    quest_arr = list(filter(None, quest_arr[1][10:]))
    event_embed = discord.Embed(
        title=quest_arr[0],
        description=f'Difficulty: {text2star(quest_arr[1])}\n⠀',
        colour=0xffa0ff
    )
    event_embed.set_footer(text="Please visit OHPS Info sheet for more details")
    event_embed.add_field(
        name='이벤트 기간ㅣEvent Period',
        value=f'{quest_arr[2]}\n⠀',
        inline=False
    )
    event_embed.add_field(
        name='설명ㅣDescription',
        value=f'{quest_arr[3]}\n⠀',
        inline=False
    )
    event_embed.add_field(
        name='조건ㅣRequirement',
        value=f'{quest_arr[4]}\n⠀',
        inline=False
    )
    event_embed.add_field(
        name='레벨ㅣLevel',
        value=f'{quest_arr[5]} ({quest_arr[6]})\n⠀',
        inline=False
    )
    joined_list = '\n'.join(quest_arr[7:])
    event_embed.add_field(
        name='최근 클리어자 목록ㅣRecent Clear List',
        value=f'{joined_list}\n⠀',
        inline=False
    )
    await interaction.response.send_message(embed=event_embed)


@bot.tree.command(name="sheet", description="OHPS Info 시트 링크를 제공합니다ㅣGive you OHPS Info sheet link")
async def sheet(interaction: discord.Interaction):
    await interaction.response.send_message('[여기를 클릭하세요!ㅣClick Here!](https://docs.google.com/spreadsheets/d/11swc3daTDK7USlzFbhBRBDC4nMbqsanlyThaA9lvloA/edit?usp=sharing)')


bot.run(token)