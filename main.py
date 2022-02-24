import globals as gl
import discord
from discord.ext import commands
import json
import json_work
import checks
import prefix_cmd
import random
from discord_components import DiscordComponents


with open('config.json', 'r') as j:
    gl.settings = json.load(j)

with open('stuff.json', 'r') as j:
    gl.gifs = json.load(j)

# activity = discord.Activity(type=discord.ActivityType.listening, name="some chill beats.")
description = '*' + gl.settings['prefix'] + 'help* for help)'
gl.bot = commands.Bot(command_prefix=gl.settings['prefix'],
                      # activity=activity,
                      # description=description,
                      status=discord.Status.online,
                      intents=discord.Intents.all())
DiscordComponents(gl.bot)
bot = gl.bot
bot.remove_command("help")

@bot.event
async def on_ready():
    await bot.user.edit(username=gl.settings['name'])
    print('Logged in as ' + bot.user.name)

    gl.settings['channel'] = 0
    gl.settings['DM'] = 0
    guilds = []
    for g in bot.guilds:
        guilds.append(g.id)
    gl.settings['guilds'] = guilds
    with open('config.json', 'w') as j:
        json.dump(gl.settings, j)

    json_work.queue_clear()

    print('------')
    print('Ready.\n')


@bot.event
async def on_member_join(member):
    for id in gl.settings['hello_ch']:
        ch = await bot.fetch_channel(id)
        if ch in member.guild.channels:
            message = 'HEY <@!' + str(member.id) + '>'
            await ch.send(message)
            await ch.send(random.choice(gl.gifs['in']))
            return


@bot.event
async def on_member_remove(member):
    for id in gl.settings['hello_ch']:
        ch = await bot.fetch_channel(id)
        if ch in member.guild.channels:
            message = 'BYE <@!' + str(member.id) + '>'
            await ch.send(message)
            await ch.send(random.choice(gl.gifs['out']))
            return


@bot.event
async def on_message(msg):
    # Игнор сам себя
    if msg.author == bot.user:
        return

    # Обработка префикс-команд (всех)
    if msg.content.startswith(gl.settings['prefix']):
        await prefix_cmd.processing(msg)

    # Парсинг ссылок в ЛС owners (проверка на ботов)
    if (msg.content.find('http') != -1 or msg.content.find('.com') != -1) and not checks.DM_check(msg) and msg.content.find('tenor.com') == -1 and  msg.content.find('youtube.com') == -1:
        if checks.own_check(msg):
            return
        for o in gl.settings['owners']:
            user = await bot.fetch_user(o)
            await user.send('New **link** in ' + str(msg.guild) + ', <#' + str(msg.channel.id) + '>:\n' + msg.content)

    # Парсинг ЛС для owners
    if checks.DM_check(msg) and not checks.own_check(msg):
        for o in gl.settings['owners']:
            user = await bot.fetch_user(o)
            text = 'DM from <@!' + str(msg.author.id) + '>:\n' + msg.content
            await gl.send_msg(user, msg, text)

    # Парсинг канала для owners
    if msg.channel.id == gl.settings['channel']:
        for o in gl.settings['owners']:
            user = await bot.fetch_user(o)
            text = '<@!'+str(msg.author.id) + '> says:\n' + msg.content
            await gl.send_msg(user, msg, text)

    # Отправка сообщений в выбранный ЛС (для owners)
    if gl.settings['DM'] != 0 and checks.own_check(msg) and checks.DM_check(msg):
        gl.typing = False
        user = await bot.fetch_user(gl.settings['DM'])
        if not msg.content.startswith(gl.settings['prefix']):
            await gl.send_msg(user, msg=msg)

    # Отправка сообщений в выбранный канал (для owners)
    if gl.settings['channel'] != 0 and checks.own_check(msg) and checks.DM_check(msg):
        gl.typing = False
        channel = await bot.fetch_channel(gl.settings['channel'])
        if not msg.content.startswith(gl.settings['prefix']):
            await gl.send_msg(channel, msg=msg)

    # Упоминание парсится в ЛС
    if bot.user in msg.mentions:
        for o in gl.settings['owners']:
            user = await bot.fetch_user(o)
            await user.send('New **mention** in ' + str(msg.guild) + ', <#' + str(msg.channel.id) + '>:\n' + msg.content)


bot.run(gl.settings['token'])
