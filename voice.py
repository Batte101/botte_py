import globals as gl
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL, utils
import requests
import json
import time
import json_work
import asyncio
import threading


yt_conf = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
    }


ffmpeg_conf = {
    'before_options': '-nostdin -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
    }


async def join(msg):
    if msg.author.voice:
        channel = msg.author.voice.channel
        vc = msg.guild.voice_client
        if vc and vc.is_connected():
            await vc.move_to(channel)
        else:
            await channel.connect()
    else:
        await gl.send_msg(msg.channel, text='You are not in any VC currently.')


def search(arg):
    with YoutubeDL(yt_conf) as ydl:
        try:
            requests.get(arg)
        except:
            info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
        else:
            info = ydl.extract_info(arg, download=False)
    return info, info['formats'][0]['url']


async def play(ctx, query):
    vc = ctx.guild.voice_client
    if vc and vc.is_connected():
        if len(vc.channel.members) > 1 and vc.channel != ctx.author.voice.channel:
            await gl.send_msg(ctx.channel, text="I'm busy now.")
            return

        json_work.queue_clear()
        await gl.send_msg(ctx.channel, text='One sec...')
    await join(ctx)
    vc = ctx.guild.voice_client

    json_work.queue_add(vc.guild.id, query)
    await gl.send_msg(ctx.channel, text='Added to queue.')
    print(gl.queue[str(ctx.guild.id)]['player'])
    if gl.queue[str(ctx.guild.id)]['player']:
        return
    else:
        print('Player made.')
        await player(ctx)


async def player(ctx):
    vc = ctx.guild.voice_client
    gl.queue[str(ctx.guild.id)]['player'] = True
    while gl.queue[str(ctx.guild.id)]['player']:
        print('In loop.')
        try:
            try:
                print('Try source.')
                video, source = search(gl.queue[str(ctx.guild.id)]['tracks'][0])
                print('Source got.')
            except utils.DownloadError:
                await gl.send_msg(ctx.channel, text="I am not playing this. I'm 0 years old!")
                json_work.queue_remove(vc.guild.id, gl.queue[str(ctx.guild.id)]['tracks'][0])
            else:
                await ctx.channel.send('Now playing: ``' + video['title'] + '``\n' + video['webpage_url'])
                vc.play(FFmpegPCMAudio(source, **ffmpeg_conf))
                json_work.queue_remove(vc.guild.id, gl.queue[str(ctx.guild.id)]['tracks'][0])

                while vc.is_playing() or vc.is_paused():
                    await asyncio.sleep(1)
                    print('Loop')
        except Exception:
            print('List is over')
            gl.queue[str(ctx.guild.id)]['player'] = False
    return


async def pause(msg):
    vc = msg.guild.voice_client
    if vc.is_playing():
        vc.pause()
        await gl.send_msg(msg.channel, text="K, I'll wait.")
    else:
        await gl.send_msg(msg.channel, text='I am not playing anything rn.')


async def resume(msg):
    vc = msg.guild.voice_client
    if vc.is_paused():
        vc.resume()
        await gl.send_msg(msg.channel, text="Here you are.")
    else:
        await gl.send_msg(msg.channel, text='I am not paused rn.')


async def skip(msg):
    vc = msg.guild.voice_client
    if vc.is_playing():
        vc.stop()
        await gl.send_msg(msg.channel, text='OK')
    else:
        await gl.send_msg(msg.channel, text='I am not playing anything rn.')


async def leave(msg):
    vc = msg.guild.voice_client
    if vc:
        await vc.disconnect()
        json_work.queue_clear()
        await gl.send_msg(msg.channel, text='Alright.')
    else:
        await gl.send_msg(msg.channel, text='I am not in any VC currently.')


async def queue(msg):
    list = ''
    for i in range(len(gl.queue[str(msg.guild.id)]['tracks'])):
        video, source = search(gl.queue[str(msg.guild.id)]['tracks'][i])
        dur = time.strftime("%M:%S", time.gmtime(video['duration']))
        list += '``' + str(i + 1) + '.`` ``' + str(dur) + '`` **' + video['title'] + '**\n'
        print(video)
    if list == '':
        list = '**Queue is empty.**'
    return list


async def remove(msg, num):
    gl.queue[str(msg.guild.id)]['tracks'].pop(num - 1)
    with open('queue.json', 'w') as j:
        json.dump(gl.queue, j)
    await gl.send_msg(msg.channel, text='New queue:')
    await queue(msg)
    return


async def idle_check(vc):
    # vc = await gl.bot.fetch_guild(guild_id).voice_client
    Flag = True
    while vc and Flag:
        await asyncio.sleep(20)
        print('Idle check.')
        if vc.channel and len(vc.channel.members) == 1:
            Flag = False
    await vc.disconnect()
    json_work.queue_clear()
    print('Idle dc.')
    return
