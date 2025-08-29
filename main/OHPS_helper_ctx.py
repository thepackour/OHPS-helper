import gspread
import discord
from discord import app_commands
from discord.ext import commands
import numpy
import datetime
import os
from dotenv import load_dotenv

import main.db as db
import main.msgformat as msgformat
import main.calc as calc
from main.calc.WordSimilarity import most_similar
import main.debug as debug

load_dotenv()
token = os.getenv("OHPS_TOKEN")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 위치
json_path = os.path.join(BASE_DIR, 'credentials', 'service_account.json')
gc = gspread.service_account(filename=json_path)
DB = gc.open("OHPS Server DB")

sheet1 = "User_Profile"
sheet2 = "Quest_List"
sht1 = "퀘스트ㅣQuest"
sheet3 = "Quest_List_Details"
sheet4 = "Event_Quest"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="o!",intents=intents)
bot.help_command = None


class WrongInput(Exception):
    def __str__(self):
        return "Client provided wrong input"

def timestamp(): return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@bot.event
async def on_ready():
    print("Hello world")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)\n")
        await bot.change_presence(activity=discord.CustomActivity(type=discord.ActivityType.custom,
                                                                  name='under development'))
        # f'Running {len(synced)} commands with one hand'
    except Exception as e:
        print(e)


@bot.event
async def on_app_command_completion(interaction: discord.Interaction, command):
    log_interaction = interaction
    log_command = command
    log_interaction_option = " "
    if 'options' in log_interaction.data:
        for values in log_interaction.data['options']:
            log_interaction_option += f"{values['name']} : {values['value']} ({type(values['value'])})\n"
    print(f"[{timestamp()} | Command] /{log_command.name}\n<{log_interaction.user.name} ({log_interaction.id})> /{log_command.name} \n{log_interaction_option}")


@bot.event
async def on_member_join(member):
    print(f"[{timestamp()} | New User] {member.name} ({member.id})\n")


# @bot.event
# async def on_message(message):
#     developer = [608914438640369676, 433224189194010654]
#     channel = bot.get_channel(1199387197963513887)
#     dev_channel = [1195221597003456642, 1195037894402908291]
#     isDev = (message.author.id in developer) and (message.channel.id in dev_channel)
#     segment = message.content.split("/./")
#     # [0]: one/all
#     # [1]: submit_date
#     # [2]: user_id
#     # [3]: quest_name
#     # [4]: reward_exp
#     # [5]: level_name
#
#     if isDev and (message.content == "help"):
#         await message.channel.send("one/./[submit_date]/./[user_id]/./[quest_name]/./[reward_EXP]/./[level_name]\n"
#                            "all/./[submit_date]/./[user_id]/./[quest_name]/./[reward_EXP]")
#
#     if isDev and (segment[0] == "one"):
#         db_arr = DB.worksheet(sheet1).get_all_values()
#         clear_arr = DB.worksheet(sheet2).get_all_values()
#         print(f"[{timestamp()} | Admin_command] /one")
#         for i in segment:
#             print(i, end=" / ")
#         y = 0
#         while str(segment[2]) != db_arr[y][0]:
#             y = y + 1
#         before_exp = db_arr[y][3]
#         before_level = db_arr[y][2]
#         DB.worksheet(sheet1).update_cell(y + 1,4,int(before_exp)+int(segment[4]))
#         after_exp = DB.worksheet(sheet1).cell(y + 1, 4).value
#         after_level = DB.worksheet(sheet1).cell(y + 1, 3).value
#         DB.worksheet(sheet1).update_cell(y + 1, 7, f"{segment[3]}ㅣ{segment[5]}")
#         yy = 0
#         while str(segment[3]) != clear_arr[yy][0]:
#             yy = yy + 1
#         for i in range(0, int(clear_arr[yy+2][0])):
#             if segment[5] == clear_arr[yy+i][1]:
#                 DB.worksheet(sheet2).update_cell(yy+i+1,4,f'{db_arr[y][1]} ({segment[1]})')
#                 break
#         quest_history = DB.worksheet(sheet1).cell(y+1, 12).value
#         if quest_history == 'none':
#             quest_history = f'{segment[3]}ㅣ{segment[5]}\n'
#         else:
#             quest_history = quest_history + f'{segment[3]}ㅣ{segment[5]}\n'
#         DB.worksheet(sheet1).update_cell(y+1, 12, quest_history)
#         levelup = f"({before_level} Level → {after_level} Level)" if after_level > before_level else f"({after_level} Level)"
#         embed = discord.Embed(title="퀘스트 완료ㅣQuest Complete",
#                               description=f"Submitted on {segment[1]}",
#                               colour=0xffffcf)
#         embed.add_field(
#             name="플레이어 이름ㅣPlayer name",
#             value=db_arr[y][1],
#             inline=True
#         )
#         embed.add_field(
#             name="경험치 & 레벨ㅣEXP & Level",
#             value=f"{before_exp}EXP → {after_exp}EXP (+{segment[4]})\n{levelup}",
#             inline=True
#         )
#         embed.add_field(
#             name="퀘스트 이름ㅣQuest name",
#             value=segment[3],
#             inline=True
#         )
#         embed.add_field(
#             name="플레이한 레벨ㅣPlayed level",
#             value=segment[5],
#             inline=True
#         )
#         await channel.send(f"<@{int(segment[2])}>")
#         await channel.send(embed=embed)
#
#     if isDev and (segment[0] == "all"):
#         db_arr = DB.worksheet(sheet1).get_all_values()
#         clear_arr = DB.worksheet(sheet2).get_all_values()
#         print(f"[{timestamp()} | Admin_command] /all")
#         for i in segment:
#             print(i, end=" / ")
#         y = 0
#         while str(segment[2]) != db_arr[y][0]:
#             y = y + 1
#         before_exp = db_arr[y][3]
#         before_level = db_arr[y][2]
#         DB.worksheet(sheet1).update_cell(y + 1, 4, int(before_exp) + int(segment[4]))
#         after_exp = DB.worksheet(sheet1).cell(y + 1, 4).value
#         after_level = DB.worksheet(sheet1).cell(y + 1, 3).value
#         DB.worksheet(sheet1).update_cell(y + 1, 7, f"{segment[3]} - **All Clear**")
#         yy = 0
#         while str(segment[3]) != clear_arr[yy][0]:
#             yy = yy + 1
#         DB.worksheet(sheet2).update_cell(yy + 1, 5, f'{db_arr[y][1]} ({segment[1]})')
#         quest_history = DB.worksheet(sheet1).cell(y+1, 12).value
#         if quest_history == 'none':
#             quest_history = f'{segment[3]}ㅣAll Clear\n'
#         else:
#             quest_history = quest_history + f'{segment[3]}ㅣAll Clear\n'
#         DB.worksheet(sheet1).update_cell(y+1, 12, quest_history)
#         levelup = f"({before_level} Level → {after_level} Level)" if after_level > before_level else f"({after_level} Level)"
#         embed = discord.Embed(title="퀘스트 올클리어ㅣQuest All Clear",
#                               description=f"Submitted on {segment[1]}",
#                               colour=0xffff9f)
#         embed.add_field(
#             name="플레이어 이름ㅣPlayer name",
#             value=db_arr[y][1],
#             inline=True
#         )
#         embed.add_field(
#             name="경험치 & 레벨ㅣEXP & Level",
#             value=f"{before_exp}EXP → {after_exp}EXP (+{segment[4]})\n{levelup}",
#             inline=True
#         )
#         embed.add_field(
#             name="퀘스트 이름ㅣQuest name",
#             value=segment[3],
#             inline=True
#         )
#         await channel.send(f"<@{int(segment[2])}>")
#         await channel.send(embed=embed)
#
#     if (message.author.id in developer) and (segment[0] == 'del'):
#         channel.delete_messages()


@bot.tree.command(name="ping", description="현재 봇의 응답속도를 보여줍니다ㅣShows the current latency of the bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! `{bot.latency}ms`")


@bot.tree.command(name="rank", description="서버 내 레벨 순위를 보여줍니다ㅣShows the level leaderboard in the server")
async def rank(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = msgformat.leaderboard_embed()
    if embed is None:
        await interaction.followup.send("오류가 발생했습니다. 다시 시도해주세요.\n"
                                        "An error occurred. Plase try again.")
        debug.log("Cannot load leaderboard_embed", {'embed': embed})
    else: await interaction.followup.send(embed=embed)


@bot.tree.command(name="register", description="서버에 등록합니다ㅣRegisters for the server")
async def register(interaction: discord.Interaction):
    await interaction.response.defer()
    try:
        db.add_user(interaction.user.id)
        delta_tier = os.getenv('DELTA_TIER')
        delta_tier_role = interaction.guild.get_role(int(delta_tier))
        await interaction.user.add_roles(delta_tier_role)
        await interaction.followup.send("성공적으로 등록되었습니다! `/myprofile`로 프로필을 볼 수 있습니다!\n"
                                        "Successfully registered! You can view your profile with `/myprofile`!")
    except db.exceptions.ExistingUser():
        await interaction.followup.send("이미 등록된 유저입니다. `/myprofile`에서 프로필을 확인하세요.\n"
                                        "You've been already registered. See your profile with `/myprofile`.")


@bot.tree.command(name="details", description="타법의 세부사항을 등록 및 수정합니다.ㅣRegister or edit the detailed info about your play")
@app_commands.describe(
    leftright = "사용하는 손ㅣYour main hand (Left/Right)",
    keys= "사용하는 키ㅣKeys that you use",
    inout = "계단 방향ㅣMultiple input direction (L to R / R to L)",
    details = "기타 세부사항ㅣOther details")
async def details(interaction: discord.Interaction, leftright: str, keys: str, inout: str, details: str):
    await interaction.response.defer()

    try:
        details_dict = {
            'main_hand': leftright,
            'number_of_keys': keys,
            'multi_input_direction': inout,
            'details': details
        }
        db.add_details(str(interaction.user.id), details_dict)
        await interaction.followup.send("성공적으로 제출되었습니다! `/myprofile`로 프로필을 볼 수 있습니다!\n"
                                        "Successfully submitted! You can view your profile with `/myprofile`!")
    except db.NoSuchUser:
        await interaction.followup.send("아직 등록되지 않았습니다. `/register`로 등록해주세요!\n"
                                        "You are not registered in the server. `/register` to register!")
    except db.InvalidDict:
        await interaction.followup.send("오류가 발생했습니다. 다시 시도해주세요.\n"
                                        "An error occurred. Plase try again.")


@bot.tree.command(name="myprofile", description="당신의 프로필 정보를 보여줍니다ㅣShows your profile's info")
@app_commands.describe(range="표시 범위 선택ㅣRange to show (level/quest/play/all)")
async def myprofile(interaction: discord.Interaction, range: str):
    await interaction.response.defer()
    user_id = str(interaction.user.id)
    try:
        user = db.find_user({'id': user_id})
        user['image_url'] = interaction.user.avatar.url

        if range in ["level", "quest", "play", "all"]:
            embed = msgformat.profile_embed(range, user)
            await interaction.followup.send(embed=embed)
        else: raise WrongInput()

    except db.NoSuchUser:
        debug.log("No such user", {'user_id': user_id})
        await interaction.followup.send("아직 등록되지 않았습니다. `/register`로 등록해주세요!\n"
                                        "You are not registered in the server. `/register` to register!")
    except WrongInput:
        debug.log("Wrong input", {'range': range})
        await interaction.followup.send("잘못된 입력입니다. 다시 시도해주세요.\nWrong input. Please try again.")
    except Exception as e:
        print(e)
        await interaction.followup.send("오류가 발생했습니다. 다시 시도해주세요.\n"
                                        "An error occurred. Plase try again.")


@bot.tree.command(name="level", description="입력한 레벨에 관한 정보를 보여줍니다.ㅣShows the info about the level you typed")
@app_commands.describe(level="검색하고 싶은 레벨ㅣThe level you want to know about")
async def level(interaction: discord.Interaction, level: int):
    await interaction.response.defer()
    user = DB.worksheet(sheet1).find(str(interaction.user.id), in_column=1)
    if user is None:
        await interaction.followup.send("아직 등록되지 않았습니다. `/register`로 등록해주세요!\nYou are not registered in the server. `/register` to register!")
    elif level <= 0:
        await interaction.followup.send("잘못된 입력입니다. 다시 시도해주세요.\nWrong input. Please try again.")
    else:
        calc_exp = calc.minEXP(level)
        difference = numpy.subtract(calc_exp, user['exp'])
        if difference >= 0:
            await interaction.followup.send(f"**{level} 레벨** 달성에 필요한 총 경험치는 **{calc_exp} EXP**, 현재 경험치보다 **{difference}**만큼 높습니다.\n"
                                            f"The total EXP to reach **{level} level** is **{calc_exp} EXP**, **{difference}** higher than your current EXP.")
        else:
            await interaction.followup.send(f"**{level} 레벨** 달성에 필요한 총 경험치는 **{calc_exp} EXP**, 현재 경험치보다 **{-1*difference}**만큼 낮습니다.\n"
                                            f"The total EXP to reach **{level} level** is **{calc_exp} EXP**, **{-1*difference}** lower than your current EXP.")


@bot.tree.command(name="quest", description="퀘스트 정보를 보여줍니다ㅣShow the info of Quest")
@app_commands.describe(quest = "퀘스트 이름ㅣQuest name")
async def quest(interaction: discord.Interaction, quest: str):
    await interaction.response.defer()

    quest_list = db.get_quest_name_list()
    quest_name_list = [q['name'] for q in quest_list]
    query = most_similar(quest, quest_name_list)

    if query is None or type(query) is not str:
        await interaction.followup.send("퀘스트를 찾을 수 없습니다. 다시 시도해주세요.\nCan't find the quest. Please try again.")
    else:
        quest = db.find_quest_by_name(query)
        try:
            embed = msgformat.quest_embed(quest)
            await interaction.followup.send(embed=embed)
        except Exception as e:
            print(e)
            await interaction.followup.send("오류가 발생했습니다. 다시 시도해주세요.\n"
                                            "An error occurred. Plase try again.")


@bot.tree.command(name="event", description="이벤트 퀘스트 정보를 보여줍니다ㅣShow the info of Event Quest")
async def event_quest(interaction: discord.Interaction):
    quest = db.get_event_quest()
    if quest is None:
        channel_link = "https://discord.com/channels/1184912633548259418/1190695760547827883"
        await interaction.response.send_message(f"현재 진행 중인 이벤트가 없습니다. 이벤트 공지는 {channel_link} 에서 확인할 수 있습니다.\n"
                                        f"There's no events going on. Event announcement can be checked at {channel_link}.")
    else:
        event_embed = msgformat.quest_embed(quest)
        await interaction.response.send_message(embed=event_embed)


@bot.tree.command(name="sheet", description="OHPS Info 시트 링크를 제공합니다ㅣGive you OHPS Info sheet link")
async def sheet(interaction: discord.Interaction):
    await interaction.response.send_message('[여기를 클릭하세요!ㅣClick Here!](https://docs.google.com/spreadsheets/d/11swc3daTDK7USlzFbhBRBDC4nMbqsanlyThaA9lvloA/edit?usp=sharing)')


bot.run(token)