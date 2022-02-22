import globals as gl
import discord
import checks
import random
import json_work
import asyncio
import voice
from discord_components import Select, SelectOption


async def help(msg):
    title = "Hello. I'm " + gl.bot.user.name + ", that's what I can do for everyone:\n\n"
    pr = gl.settings['prefix']
    hlp = '**' + pr + 'play** - playing music in voice channels.\nFormat: `' + pr + 'play despacito` or `' + pr
    hlp += 'play <YT_URL>`\n'
    hlp += '**' + pr + 'pause** - pause music.\n'
    hlp += '**' + pr + 'resume** - resume music.\n'
    hlp += '**' + pr + 'loop** - toggle on/off looping tracks.\n'
    hlp += '**' + pr + 'skip** - skip current track.\n'
    hlp += '**' + pr + 'leave** - leave voice channel.\n'
    hlp += '**' + pr + 'queue** - show music queue.\n'
    hlp += '**' + pr + 'remove** - removes track from queue.\nFormat: `' + pr + 'remove <queue_num>`\n\n'
    hlp += '**' + pr + 'roll** - rolls a dice.\nFormat: `' + pr + 'roll d20` or `' + pr + 'roll 2d4`\n\n'
    hlp += "Also I can talk. Really. Ping me or DM me, and if I'm free, I'll answer.\n\n"
    hlp += '(If you are a mod - type `' + pr + 'mod_help` for another list)'
    embed = discord.Embed(title=title, description=hlp, url='https://www.youtube.com/watch?v=otoGYd_IFkM',
                          colour=0x8ac9db).set_thumbnail(url=str(gl.bot.user.avatar_url))
    await msg.channel.send(embed=embed)
    return


async def mod_help(msg):
    title = 'There are some mods commands:\n\n'
    pr = gl.settings['prefix']
    hlp = '**' + pr + 'pick** - picks random member from the Guild.\nFormat: `' + pr + 'pick #channel And then the '
    hlp += 'whole message, you want to post, and a @ somewhere.`\n'
    hlp += "Instead of `#channel`, you can put here channel ID ||(if you know where is it)||. It's the place, where "
    hlp += 'results of roll will post.\nEvery @ will change to a winner ping. Also you can '
    hlp += 'attach pictures)\n'
    hlp += '**' + pr + 'kick** - you know, what it does.\nFormat: `' + pr + 'kick @Douchebag`\n'
    hlp += '**' + pr + "prefix** - changes my prefix.\nFormat: `" + pr + 'prefix !@#$&? (i dunno)`\n\n'
    hlp += "If something wrong - ping or DM me. I'll fix as soon as I can."
    embed = discord.Embed(title=title, description=hlp, url='https://www.youtube.com/watch?v=FC0rsdJHkek',
                          colour=0x8ac9db).set_thumbnail(url=str(gl.bot.user.avatar_url))
    await msg.channel.send(embed=embed)
    return


async def own_help(msg):
    title = 'Это - хэлп.'
    pr = gl.settings['prefix']
    hlp = '**' + pr + "add_mod** - add moderator.\nFormat: `" + pr + "add_mod ID`\n"
    hlp += '**' + pr + "remove_mod** - remove moderator.\nFormat: `" + pr + "remove_mod ID`\n\n"
    hlp += "**" + pr + "map** - shows every channel in all Guilds and lets to choose one to listen.\n"
    hlp += "**" + pr + "memb** - shows every member in all Guilds and lets to choose one to DM.\n"
    hlp += "**" + pr + "dm/ch** - chooses what channel/DM listen/reply.\nFormat: `" + pr + "ch #channel` or `"
    hlp += pr + "dm @user`\n"
    hlp += "**" + pr + "reply** - replies to msg. If want to ping - `@@` anywhere.\nFormat: `" + pr
    hlp += "reply @@ msg_ID Text`\n"
    hlp += '**' + pr + "tp** - typing in listened channel/DM.\n"
    hlp += "**" + pr + "edit** - edits previous msg.\nFormat: `" + pr + "edit msg_ID @old @new in ch_ID`\n"
    hlp += '**' + pr + "delete** - delete message.\nFormat: `" + pr + "delete msg_ID in ch_ID`\n\n"
    hlp += '**' + pr + 'join** - join voice channel.\n\n'
    hlp += "**" + pr + "status** - shows what ID is now listening.\n\n"
    hlp += "**Also bot:**\nListens for every DM and copy msg to all owner's accounts\n"
    hlp += "Listens for links and DM them for checking (bot security)\n"
    hlp += "DM every mention of a bot.\n\n"
    hlp += "Hope I didn't forget anything."
    embed = discord.Embed(title=title, description=hlp, url='https://www.youtube.com/watch?v=baJL4bGX9m8',
                          colour=0x8ac9db).set_thumbnail(
        url='https://sun9-25.userapi.com/impg/D753fpIPO6LOJl6x40tDThtx3rccwLUnG7zWzA/w79Pr9YZQYo.jpg?size=165x179&quality=96&sign=49cb55f989e6cbf1a5a2231673a585b8&type=album')
    await msg.channel.send(embed=embed)
    return


async def processing(msg):
    # Отрез префикса, далее работа со строкой
    s = msg.content
    s = s[len(gl.settings['prefix']):]

    # OWNER КОММАНДЫ
    if checks.own_check(msg):
        # Добавление/удаление модеров (для owners)
        if s.startswith('add_mod'):
            if not checks.is_num(s[len('add_mod'):]):
                return 'No mod T_T'
            id = int(s[len('add mod'):])
            await gl.send_msg(msg.author, text=json_work.add_mod(id))
            return
        if s.startswith('remove_mod') and checks.own_check(msg):
            if not checks.is_num(s[len('remove_mod'):]):
                return 'No mod T_T'
            id = int(s[len('remove_mod'):])
            await gl.send_msg(msg.author, text=json_work.remove_mod(id))
            return

        # ЛС команды
        if checks.DM_check(msg):
            # Смена ЛС
            if s.startswith('dm'):
                embed = await dm_change(msg, s[3:])
                await msg.author.send(embed=embed)
                return
            # Смена канала
            if s.startswith('ch'):
                embed = await ch_change(msg, s[3:])
                await msg.author.send(embed=embed)
                return
            # Очистка ID
            if s.startswith('clear'):
                embed = discord.Embed(description=json_work.ID_clear(), colour=0x8ac9db)
                await msg.author.send(embed=embed)
                return
            # Карта серверов (для owner)
            if s.startswith('map'):
                for id in gl.settings['guilds']:
                    guild = gl.bot.get_guild(id)
                    embed, sels = channel_map(guild)
                    await msg.author.send(embed=embed, components=[sels])
                gl.interaction = await gl.bot.wait_for("select_option", check=lambda i: i.custom_id == "select0")
                embed = await ch_change(msg, gl.interaction.values[0])
                await gl.interaction.send(embed=embed)
                return
            # Карта участников (для owner)
            if s.startswith('memb'):
                for id in gl.settings['guilds']:
                    guild = gl.bot.get_guild(id)
                    embed, sels = member_map(guild)
                    await msg.author.send(embed=embed, components=[sels])
                gl.interaction = await gl.bot.wait_for("select_option", check=lambda i: i.custom_id == "select1")
                embed = await dm_change(msg, gl.interaction.values[0])
                await gl.interaction.send(embed=embed)
                return
            # Проверка статуса
            if s.startswith('status'):
                ans = 'Channel ID: **<#' + str(gl.settings['channel']) + '>**\nDM ID: **<@!' + str(
                    gl.settings['DM']) + '>**'
                ans += '\nTyping: **' + str(gl.typing) + '**'
                embed = discord.Embed(title='Status', description=ans, colour=0x8ac9db)
                await msg.author.send(embed=embed)
                return
            # Редактирование сообщений
            if s.startswith('edit'):
                msg_id = s[5:s.find('@') - 1]
                old = s[s.find('@') + 1:s.rfind('@') - 1]
                new = s[s.rfind('@') + 1:s.find(' in ')]
                ch_id = s[s.rfind(' ') + 1:]
                channel = await gl.bot.fetch_channel(ch_id)
                old_msg = await channel.fetch_message(msg_id)
                string = old_msg.content.replace(old, new)
                await old_msg.edit(content=string)
                return
            # Ответ на сообщение
            if s.startswith('reply'):
                if gl.settings['channel'] == 0:
                    embed = discord.Embed(title='Not listening to channel.', colour=0x8ac9db)
                    await msg.author.send(embed=embed)
                    return
                ping = False
                if s.find('@@') != -1:
                    s = s.replace('@@', '')
                    ping = True
                s = s[6:]
                msg_id = s[:s.find(' ')]
                print(msg_id)
                channel = await gl.bot.fetch_channel(gl.settings['channel'])
                r_msg = await channel.fetch_message(msg_id)
                print(s[s.find(' ') + 1:])
                await r_msg.reply(s[s.find(' '):], mention_author=ping)
                return
            # Удаление сообщений
            if s.startswith('delete'):
                msg_id = s[7:s.find('in') - 1]
                ch_id = s[s.find('in') + 3:]
                channel = await gl.bot.fetch_channel(ch_id)
                del_msg = await channel.fetch_message(msg_id)
                await del_msg.delete()
                return
            # "Печатает"
            if s.startswith('tp'):
                if gl.settings['DM'] == 0 and gl.settings['channel'] == 0:
                    await msg.author.send('Not listening to anyone.')
                    return
                elif gl.typing:
                    gl.typing = False
                    embed = discord.Embed(title='Stop typing...', colour=0x8ac9db)
                    await msg.author.send(embed=embed)
                    return
                elif gl.settings['DM'] != 0:
                    user = await gl.bot.fetch_user(gl.settings['DM'])
                    embed = discord.Embed(title='Typing...', colour=0x8ac9db)
                    await msg.author.send(embed=embed)
                    await typing(user)
                    return
                elif gl.settings['channel'] != 0:
                    ch = await gl.bot.fetch_channel(gl.settings['channel'])
                    embed = discord.Embed(title='Typing...', colour=0x8ac9db)
                    await msg.author.send(embed=embed)
                    await typing(ch)
                    return

    # MODS КОММАНДЫ
    if checks.mod_check(msg):
        # Выбор случайного с объявлением (для mods)
        if s.startswith('pick'):
            await random_pick(s[5:], msg)
            return
        # В каналах
        if not checks.DM_check(msg):
            # Кик
            if s.startswith('kick'):
                text = s[5:]
                for user in msg.mentions:
                    if user.id == gl.bot.user.id or user.id in gl.settings['owners'] or user.id in gl.settings['mods']:
                        await gl.send_msg(msg.channel, text=gl.gifs['what'])
                        return
                    reason = text[len('<@!' + str(user.id) + '> '):]
                    await user.kick(reason=reason)
            # Замена префикса
            if s.startswith('prefix'):
                pr = s[len('prefix '):]
                embed = discord.Embed(title='Prefix', description=json_work.prefix_change(pr), colour=0x8ac9db)
                await msg.channel.send(embed=embed)
                return

    # Дайсролл
    if s.startswith('roll'):
        s = s.lower()
        await gl.send_msg(msg.channel, text=dice_game(s[5:]))
        return

    # Helps
    if s.startswith('help'):
        await help(msg)
        return
    if s.startswith('mod_help') and checks.mod_check(msg):
        await mod_help(msg)
        return
    if s.startswith('own_help') and checks.own_check(msg):
        await own_help(msg)
        return

    # Голос
    vc = msg.guild.voice_client
    if s.startswith('join') and checks.own_check(msg):
        await voice.join(msg)
        return
    if s.startswith('play'):
        if vc and (not msg.author.voice or vc.channel != msg.author.voice.channel) and len(vc.channel.members) > 1:
            await msg.channel.send('You are not listening.')
            return
        await voice.play(msg, s[s.find(' ') + 1:])
        return
    if s.startswith('skip'):
        if vc and (not msg.author.voice or vc.channel != msg.author.voice.channel):
            await msg.channel.send('You are not listening.')
            return
        await voice.skip(msg)
        return
    if s.startswith('loop'):
        if vc and (not msg.author.voice or vc.channel != msg.author.voice.channel):
            await msg.channel.send('You are not listening.')
            return
        await voice.loop(msg)
        return
    if s.startswith('pause'):
        if vc and (not msg.author.voice or vc.channel != msg.author.voice.channel):
            await msg.channel.send('You are not listening.')
            return
        await voice.pause(msg)
        return
    if s.startswith('resume'):
        if vc and (not msg.author.voice or vc.channel != msg.author.voice.channel):
            await msg.channel.send('You are not listening.')
            return
        await voice.resume(msg)
        return
    if s.startswith('leave'):
        if vc and (not msg.author.voice or vc.channel != msg.author.voice.channel):
            await msg.channel.send('You are not listening.')
            return
        await voice.leave(msg)
        return
    if s.startswith('queue'):
        async with msg.channel.typing():
            list = await voice.queue(msg)
            embed = discord.Embed(title='Queue', description=list, colour=0x8ac9db)
            await msg.channel.send(embed=embed)
        return
    if s.startswith('remove '):
        if vc and (not msg.author.voice or vc.channel != msg.author.voice.channel):
            await msg.channel.send('You are not listening.')
            return
        num = s[s.find(' ') + 1:]
        max = len(gl.queue[str(msg.guild.id)]['tracks'])
        if checks.is_num(num) and 0 < int(num) <= max:
            async with msg.channel.typing():
                await voice.remove(msg, int(num))
                list = await voice.queue(msg)
                embed = discord.Embed(title='Queue', description=list, colour=0x8ac9db)
                await msg.channel.send('New queue:', embed=embed)
        else:
            await msg.channel.send('Wrong number.')
        return


async def ch_change(msg, s):
    if s.find('<#') != -1:
        id = s[s.find('#') + 1:s.find('>')]
    else:
        if not checks.is_num(s):
            await gl.send_msg(msg.author, text='Wrong ID.')
            return
        id = s
    embed = discord.Embed(description=json_work.channel_change(id), colour=0x8ac9db)
    return embed


async def dm_change(msg, s):
    if s.find('<@!') != -1:
        id = s[s.find('!') + 1:s.find('>')]
    else:
        if not checks.is_num(s):
            await gl.send_msg(msg.author, text='Wrong ID.')
            return
        id = s
    embed = discord.Embed(description=json_work.DM_change(id), colour=0x8ac9db)
    return embed


def channel_map(guild):
    list = []
    vals = []
    ans = 'Text Channels:\n'
    for ch in guild.channels:
        if checks.what_type(ch) == 'text':
            ans += '<#' + str(ch.id) + '>\n'
            list.append(ch.name)
            vals.append(ch.id)
    ans += '\nVoice Channels:\n'
    for ch in guild.channels:
        if checks.what_type(ch) == 'voice':
            ans += '<#' + str(ch.id) + '>\n'
    embed = discord.Embed(title=guild.name, description=ans, colour=0x8ac9db).set_thumbnail(
        url=str(guild.icon_url))
    sels = sel_tab(0, list, vals)
    return embed, sels


def dice_game(dice):
    if dice.find('d') != -1:
        d = dice.index('d')
    else:
        return 'Umm, try again.'

    if checks.is_num(dice[d + 1:]):
        try:
            r = int(dice[:d])
        except ValueError:
            r = 1
        n = int(dice[d + 1:])
        print(r, 'd', n)
    else:
        return 'Umm, try again.'

    ans = 'Here you go: [ '
    for i in range(r):
        ans += str(random.randrange(1, n + 1)) + ' '
    ans += ']'
    return ans


async def random_pick(s, msg):
    if s.find(' ') == -1:
        return 'Wrong input. Try again.'
    else:
        if s.find('<#') != -1:
            ch_id = s[s.find('<#') + 2:s.find('>')]
        else:
            ch_id = s[:s.find(' ')]
        string = s[s.find(' ') + 1:]

        channel = await gl.bot.fetch_channel(int(ch_id))
        rndMbr = random.choice(channel.guild.members)
        ans = string.replace('@', '<@!' + str(rndMbr.id) + '>')
        await gl.send_msg(channel, msg, ans)
        return


async def typing(ch):
    gl.typing = True
    async with ch.typing():
        while gl.typing:
            await asyncio.sleep(1)
    return


def sel_tab(num, list, vals):
    opt_l = []
    for i in range(len(list)):
        opt = SelectOption(label=list[i], value=vals[i])
        opt_l.append(opt)

    ans = Select(
        placeholder="Select something!",
        options=opt_l,
        custom_id="select" + str(num),
    )
    return ans


def member_map(guild):
    list = []
    vals = []
    for mbr in guild.members:
        list.append(mbr.name)
        vals.append(mbr.id)
    embed = discord.Embed(title=guild.name, description="All of the members:", colour=0x8ac9db).set_thumbnail(
        url=str(guild.icon_url))
    sels = sel_tab(1, list, vals)
    return embed, sels
