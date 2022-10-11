import asyncio
import discord
from discord.ext import commands
import sqlite3
import time
import random
from datetime import datetime, timedelta

#DB
conn = sqlite3.connect("userinfo.db", isolation_level=None)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS userinfo \
    (user_id, user_name, user_code, EXP, Level, money, next_get_time)")

# token = open('Token.txt', 'r').read()
token = 'MTAyOTA1ODY2MzIyODM3NTA3Mg.GmFv-A.GOQzneYfcKcJ_BHEEk3wvi6EAulMOnYoQUSLZA'
Intents = discord.Intents.all()
client = discord.Client(intents=Intents)

@client.event
async def on_ready():
    print(f'{client.user.name}:{client.user.id}')
    print("Zeta 준비 완료!")
    activity = discord.Game("!help")
    await client.change_presence(status=discord.Status.online, activity=activity)

@client.event
async def on_message(message):
    guild = message.guild
    if message.content == '!ping' or message.content == '!핑':
        latency = str(round(client.latency*1000))+'ms'
        await message.channel.send(':ping_pong: Pong! '+latency)
    elif message.content == '!누구니':
        await message.channel.send('저는 Zeta에요')
    #서버 정보
    elif message.content == '!서버 정보':
        pass
    #DM
    elif message.content.startswith('!DM') or message.content.startswith('!dm') or message.content.startswith('!ㄷㅇ'):
        msg = message.content[4:]
        to = message.guild.get_member(int(msg[2:21]))
        content = msg[23:]
        await message.channel.purge(limit=1)
        embed = discord.Embed(title="DM이 도착했습니다.", color=0x66edff)
        embed.add_field(name='내용', value=content, inline=False)
        embed.add_field(name='보낸 서버', value=guild.name)
        await to.send(embed=embed)
    #청소
    elif message.content.startswith('!청소'):
        count = int(message.content[4:])
        await message.channel.purge(limit=count)
    elif message.content == '!가입':
        c.execute("SELECT * FROM userinfo WHERE user_id=:Id", {"Id": str(message.author.id)})
        if c.fetchone() == None:
            author = str(message.author).split('#')
            c.execute(f"INSERT INTO userinfo \
                VALUES('{message.author.id}', '{author[0]}', '{author[1]}', 0, 0, 0, 0)")
            await message.channel.send('Zeta 서비스에 가입이 완료되었습니다.')
        else:
            await message.channel.send('이미 Zeta 서비스에 가입되어 있습니다.')
    # 개인 정보
    personal_info = ['!지갑', '!입금']
    for i in range(len(personal_info)):
        if personal_info[i] in message.content:
            author = str(message.author).split('#')
            c.execute("SELECT * FROM userinfo WHERE user_id=:Id", {"Id": str(message.author.id)})
            if c.fetchone() == None:
                await message.channel.send('Zeta 서비스에 먼저 가입해야 합니다.')
                await message.channel.send('`!가입`을 먼저 해주세요.')
            else:
                c.execute("SELECT * FROM userinfo WHERE user_id=:Id", {"Id": str(message.author.id)})
                user_data = c.fetchone()
                #지갑
                if message.content == '!지갑':
                    embed = discord.Embed(title=f"잔액:   {user_data[5]}원", color=0x66edff)
                    embed.set_footer(text=time.strftime("%Y/%m/%d %H:%M:%S"))
                    await message.channel.send(embed=embed)
                if message.content == '!입금':
                    if int(str(datetime.now()).replace('-','').replace(' ','').replace(':','').split('.')[0]) < int(user_data[6]):
                        embed = discord.Embed(title='알림', color=0x66edff)
                        next_time = str(user_data[6])
                        next_time = next_time[:4]+'/'+next_time[4:6]+'/'+next_time[6:8]+' '+next_time[8:10]+':'+next_time[10:12]+':'+next_time[12:14]
                        embed.add_field(name='아직 입금 대기시간입니다.', value=f"다음 입금 시간:   {next_time}")
                        await message.channel.send(embed=embed)
                    else:
                        now_money = int(user_data[5])
                        get_money = int(random.choice(range(1000, 10000)))
                        now_money = now_money + get_money
                        next_money = str(datetime.now()+timedelta(minutes=5)).split('.')[0]
                        next_get = next_money.replace('-','').replace(' ','').replace(':','')
                        c.execute("UPDATE userinfo SET money=? WHERE user_id=?", (now_money, str(message.author.id)))
                        c.execute("UPDATE userinfo SET next_get_time=? WHERE user_id=?", (next_get, str(message.author.id)))
                        embed = discord.Embed(title='입금 알림', color=0x66edff)
                        embed.add_field(name=f'입금된 돈:   {get_money}원', value=f'잔액:   {now_money}원')
                        embed.set_footer(text=f'다음 입금 시간:   {next_money}')
                        await message.channel.send(embed=embed)
                        
        
@client.event
async def on_member_join(member):
    msg = "안녕하세요! Zeta입니다. "
    await member.send(msg)

client.run(token)