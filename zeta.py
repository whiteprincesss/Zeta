import discord
from discord.ext import commands

prefix = "%"
bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    # 'comment'라는 게임 중으로 설정합니다.
    game = discord.Game("%help")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print("Zeta가 준비되었습니다!")