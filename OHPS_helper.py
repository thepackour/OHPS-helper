import discord

TOKEN = 'MTE5MDcwNTU1NjY1MDk5MTc5Ng.GCDxUB.NpYbAU_wWJjnwGToxJt5sm7svlvJ05DIPWq270'
CHANNEL_ID = '1190856453771243711'


class MyClient(discord.Client):
    async def on_ready(self):
        channel = self.get_channel(int(CHANNEL_ID))
        # await self.change_presence(status=discord.Status.online, activity=discord.Activity("o!help"))
        print('Hello World')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == "o!help":
            embed = discord.Embed(
                title = '명령어ㅣCommands',
                description = 'OHPS Helper는 아래 명령어들을 지원합니다.\nOHPS Helper supports these commands below.',
                colour = 0x00e7ff
            )
            embed.add_field(
                name="o!register",
                value="자신의 타법과 관련된 정보를 등록합니다.\nRegisters the info about your play.",
                inline=False
            )
            embed.add_field(
                name="o!stats",
                value="등록된 타법들의 통계를 보여줍니다.\nShows the statistics of the registered plays",
                inline=False
            )
            embed.add_field(
                name="o!tier.p",
                value="티어 책정 등 티어 관련 명령어를 보여줍니다.\nShows the commands related to tier such as tier placement.",
                inline=False
            )
            await message.channel.send(embed=embed)

        # class register:
        #     def __init__(self, respondent, left_right, in_out, other):
        #         self.respondent = respondent
        #         self.left_right = left_right
        #         self.in_out = in_out
        #         self.other = other
        #     def query(self, author):
        #         respondent = author
        #         await message.channel.send("d")

        if message.content == "o!register":
            author = message.author
            message_id = message.id
            # register.query(author)
            await message.channel.send(content="asdf",reference=message,mention_author=False)

        if message.content == "o!test":
            discord.MessageReference()

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)