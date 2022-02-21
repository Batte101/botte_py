import globals as gl
import discord


def own_check(msg):
    if msg.author.id in gl.settings['owners']:
        return True
    else:
        return False


def mod_check(msg):
    if msg.author.id in gl.settings['mods'] or msg.author.id in gl.settings['owners']:
        return True
    else:
        return False


def DM_check(msg):
    if msg.channel.type == discord.ChannelType.private:
        return True
    else:
        return False


def is_num(s):
    if s is None:
        return False
    try:
        int(s)
        return True
    except ValueError:
        return False


def what_type(ch):
    if ch.type == discord.ChannelType.text:
        return 'text'
    elif ch.type == discord.ChannelType.voice:
        return 'voice'
    else:
        return None


def hello_check(mbr):
    if mbr.guild.channel.id in gl.settings['owners']:
        return True
    else:
        return False
