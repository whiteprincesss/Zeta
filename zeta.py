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
    (user_id, user_name, user_code, EXP, Level, money, next_get_time, percent)")

token = open('Token.txt', 'r').read()
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
    if message.author == client.user:
        return
    guild = message.guild
    if message.content == '!ping' or message.content == '!핑':
        latency = str(round(client.latency*1000))+'ms'
        await message.channel.send(':ping_pong: Pong! '+latency)
    elif message.content == '!누구니':
        await message.channel.send('저는 Zeta에요')
    #서버 정보
    elif message.content == '!서버 정보':
        embed = discord.Embed(title=f'{guild.name}의 정보', color=0x66edff)
        server_birth = str(guild.created_at).split()[0]
        embed.add_field(name='서버 주인', value=guild.owner, inline=True)
        embed.add_field(name='생성일', value=server_birth, inline=False)
        embed.add_field(name='멤버 수', value=guild.member_count, inline=True)
        embed.add_field(name='부스트 개수', value=guild.premium_subscription_count, inline=True)
        await message.channel.send(embed=embed)
        print(type(message.channel))
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
        await message.channel.purge(limit=count+1)
    elif message.content == '!가입':
        c.execute("SELECT * FROM userinfo WHERE user_id=:Id", {"Id": str(message.author.id)})
        if c.fetchone() == None:
            author = str(message.author).split('#')
            c.execute(f"INSERT INTO userinfo \
                VALUES('{message.author.id}', '{author[0]}', '{author[1]}', 0, 0, 0, 0, 50)")
            await message.channel.send('Zeta 서비스에 가입이 완료되었습니다.')
        else:
            await message.channel.send('이미 Zeta 서비스에 가입되어 있습니다.')
    #서버 관리자 전용
    elif message.content.startswith('!밴'):
        if message.author.id == '611959855330099230':
            msg = message.content[3:]
            user = message.guild.get_member(int(msg[2:21]))
            reason = msg[23:]
            await guild.ban(user=user, reason=reason)
            await message.channel.purge(limit=1)
            await message.channel.send(f'입국금지를 시켰습니다.\n사유:   {reason}')
        else:
            await message.channel.send('권한이 없습니다.')
    elif message.content.startswith('!킥'):
        if message.author.id == 611959855330099230:
            msg = message.content[3:]
            user = message.guild.get_member(int(msg[2:21]))
            reason = msg[23:]
            await guild.kick(user=user, reason=reason)
            await message.channel.purge(limit=1)
            await message.channel.send(f'추방 시켰습니다.\n사유:   {reason}')
        else:
            await message.channel.send('권한이 없습니다.')
    elif message.content.startswith('!정회원'):
        if message.author.id == 611959855330099230:
            msg = message.content[5:]
            user = message.guild.get_member(int(msg[2:21]))
            reason = msg[23:]
            already_role = user.roles[1].id
            if already_role == 1029426979268735046:
                await message.channel.purge(limit=1)
                await message.channel.send('이미 정회원입니다.')
            else:
                await user.remove_roles(client.get_guild(937304520671760404).get_role(already_role))
                await user.add_roles(client.get_guild(937304520671760404).get_role(1029426979268735046))
                await user.send(user.mention+'님은 이제 정회원 게시판을 이용할 수 있습니다.')
                await message.channel.purge(limit=1)
        else:
            await message.channel.send('권한이 없습니다.')
    elif message.content.startswith('!준회원'):
        if message.author.id == 611959855330099230:
            msg = message.content[5:]
            user = message.guild.get_member(int(msg[2:21]))
            reason = msg[23:]
            already_role = user.roles[1].id
            if already_role == 1029426679501828126:
                await message.channel.purge(limit=1)
                await message.channel.send('이미 준회원입니다.')
            else:
                await user.remove_roles(client.get_guild(937304520671760404).get_role(already_role))
                await user.add_roles(client.get_guild(937304520671760404).get_role(1029426679501828126))
                await user.send(user.mention+'님은 이제 준회원 게시판을 이용할 수 있습니다.')
                await message.channel.purge(limit=1)
        else:
            await message.channel.send('권한이 없습니다.')
        
    #금융
    personal_info = ['!통장', '!입금', '!확률', '!도박', '!ㄷㅂ', '!회생신청', '!ㅇㅇ', '!올인']
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
                if message.content == '!통장':
                    janak = int(user_data[5])
                    embed = discord.Embed(title=f"잔액:   {format(janak, ',')}원", color=0x66edff)
                    embed.set_footer(text=time.strftime("%Y/%m/%d %H:%M:%S"))
                    await message.channel.send(embed=embed)
                if message.content == '!확률':
                    embed = discord.Embed(title=f"도박 성공 확률:   {user_data[7]}%", color=0x66edff)
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
                        embed.add_field(name=f'입금된 돈:   {format(get_money, ",")}원', value=f'잔액:   {format(now_money, ",")}원')
                        embed.set_footer(text=f'다음 입금 시간:   {next_money}')
                        await message.channel.send(embed=embed)
                if message.content.startswith('!도박') or message.content.startswith('!ㄷㅂ') or message.content.startswith('!ㅇㅇ') or message.content.startswith('!ㅇㅇ'):
                    startwith = message.content[0:3]
                    if startwith == '!ㅇㅇ' or startwith == '!올인':
                        multiply = int(message.content[4:])
                        seed_money = int(user_data[5])
                    else:
                        msg = message.content[4:].split()
                        multiply = int(msg[0])
                        seed_money = int(msg[1])
                    if int(user_data[5]) < seed_money:
                        await message.channel.send('잔액이 부족합니다.')
                    else:
                        if multiply > 10:
                            await message.channel.send('최대 10배까지 할 수 있습니다.')
                        elif 0< multiply <= 10:
                            probability = float(user_data[7])
                            products = {0 : 100-probability, multiply : probability}
                            productrange = []
                            productresult = []
                            for product in products:
                                if not productrange:
                                    productresult.append(product)
                                    productrange.append(products[product])
                                else:
                                    productresult.append(product)
                                    productrange.append(productrange[-1] + products[product])
                            tempresult = random.randrange(1,productrange[-1]+1)
                            tempcnt = 0
                            for i in productrange:
                                if tempresult <= i:
                                    result = productresult[tempcnt]
                                    if result == 0:
                                        result_text = '실패'
                                        result_money = -seed_money*multiply
                                    else:
                                        result_text = '성공'
                                        result_money = seed_money*multiply
                                    break
                                else:
                                    tempcnt=tempcnt+1
                            end_money = int(user_data[5])+result_money
                            if result_text == '실패':
                                next_probability = float(user_data[7])+float(multiply*0.75)
                            else:
                                next_probability = float(user_data[7])-float(multiply*0.75)
                            embed = discord.Embed(title='도박 결과',description=result_text, color=0x66edff)
                            embed.add_field(name='투자금', value=format(seed_money, ','), inline=False)
                            embed.add_field(name='결과', value=f'{format(result_money, ",")}원')
                            embed.add_field(name='현재 잔액', value=format(end_money, ','))
                            embed.add_field(name='다음 확률', value=str(next_probability), inline=False)
                            c.execute("UPDATE userinfo SET money=? WHERE user_id=?", (end_money, str(message.author.id)))
                            c.execute("UPDATE userinfo SET percent=? WHERE user_id=?", (next_probability, str(message.author.id)))
                            await message.channel.send(embed=embed)
                        else:
                            await message.channel.send('1배부터 가능합니다.')
                if message.content.startswith('!회생신청'):
                    c.execute("DELETE FROM userinfo WHERE user_id=:id", {'id': str(message.author.id)})
                    author = str(message.author).split('#')
                    c.execute(f"INSERT INTO userinfo \
                        VALUES('{message.author.id}', '{author[0]}', '{author[1]}', 0, 0, 0, 0, 50)")
                    f = open('blacklist/blacklist.txt', 'a', encoding='utf-8')
                    f.write(f'ID: {message.author.id}, Name: {author[0]}, Tag: {author[1]}\n')
                    f.close()
                    await message.channel.send(message.author.mention +'님의 회생신청이 완료되었습니다.')

@client.event
async def on_member_join(member):
    if member == client.user:
        return
    channel = client.get_channel(1029059697753477180)
    await member.add_roles(client.get_guild(937304520671760404).get_role(1029426679501828126))
    await channel.send(member.mention+'님 만나서 반가워요!')
    await member.send('이제 준회원 게시판을 사용할 수 있습니다.')

client.run(token)