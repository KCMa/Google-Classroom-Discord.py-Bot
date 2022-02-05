# ============= imports =============

from datetime import datetime
import logging
import json
import os.path
import re
from tkinter import FALSE

import discord
from discord.ext import commands, tasks

import calculator

from timetable import getDayOfCycle, getLessonList

from env import fetchEnvData

configFile = open('config.json')
config = json.load(configFile)


# For debugging only ( can be excluded )

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# ============ Bot Config ============

activity = discord.Activity(
    type=discord.ActivityType.listening, name="$timetable today <class>")
intents = discord.Intents().all()  # Specify the bot intents
bot = commands.Bot(command_prefix='egg ',
                   intents=intents, activity=activity)  # Create the bot client
service = None  # Will be used to store Google Classroom API Service


# =========== Bot Events ===========

# @tasks.loop(minutes=10)  # Repeat every 10 minutes
# async def fetchAssignmentsTask(args):
#     await fetchAssignments(args)  # fetch Assignments


@bot.event  # On bot ready
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    # Authorize Google Classroom API and get the API Service
    # service = await authAndGetService()
    # Start fetching assignments every 10 minutes
    # fetchAssignmentsTask.start(service)


# ========== Bot Commands ==========
@bot.command()
async def hello(ctx):     #say hello
    await ctx.send(f"hello, {ctx.author.display_name}")

@bot.command()
async def joinvoice(ctx):
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    
@bot.command()
async def env(ctx):     #display environment data
    reply = await ctx.send('小英為你獲取資料中，請你稍等...')
    embedList=fetchEnvData()
    await reply.edit(content='環境資料如下：')
    for embed in embedList:
      await ctx.send(embed=embed)

@bot.command()
async def simeq(ctx,x1,y1,c1,x2,y2,c2):     #solve simutaneous equation
    solution=calculator.simultaneousEq(x1,y1,c1,x2,y2,c2)
    await ctx.send('x={} \n y={}'.format(*solution))

@bot.command()
async def quaeq(ctx,A,B,C):     #solve quadratic equation
    solution=calculator.quadraticEq(A,B,C)
    await ctx.send('x={} or \nx={}'.format(*solution))
      

@bot.command()
async def timetable(ctx, arg1='', arg2=''):  # Timetable Command
    reply = await ctx.send('獲取時間表資料中...')
    tomorrow = False
    day = ''
    if re.match(r'[A-H]', arg1):
        day = arg1
    if re.match(r'today|now', arg1) or not arg1:
        day = getDayOfCycle(False)
    if re.match(r'tomorrow|tmr', arg1):
        tomorrow = True
        day = getDayOfCycle(True)

    if not day:
        return await ctx.send('不存在 Day {}'.format(arg1))

    arg2 = arg2 or config["class"]

    if not day:  # Most likely won't happen
        return await ctx.send('發生了預期外的錯誤')

    if day == '/':  # Tells the user if it's school holiday
        return await ctx.send('{}是學校假期'.format('明天' if tomorrow else '今天'))

    param = {'day': day, 'class_': arg2,
             'date': datetime.now().strftime('%d %B, %Y')}
    # Get the lesson list
    lessons = getLessonList(param['class_'], param['day'])
    await reply.edit(content='載入中...')

    if lessons[0] == None:  # If lessons[0] is type Non, warn the user
        return await ctx.send('錯誤 : {}'.format(lessons[1]))

    embedFields = []
    i = 0

    for lesson in lessons:
        embedFields.append({'name': '第 {} 節'.format(
            i+1), 'value': '{}\n'.format(lesson), 'inline': False})
        i += 1

    timetableEmbed = discord.Embed(
        title='{class_}班時間表'.format(**param),
        description='{date} (Day {day})'.format(
            **param),
        color=0x03A4EC
    )

    for field in embedFields:
        timetableEmbed.add_field(**field)

    await reply.edit(content='\u2800', embed=timetableEmbed)

# ========= Run(start) the bot =========

import keep_alive
keep_alive.keep_alive()


# run the bot
bot.run(os.environ['token'])

