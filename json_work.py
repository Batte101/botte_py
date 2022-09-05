import globals as gl
import json


def DM_change(id):
    if id != gl.settings['DM']:
        gl.settings['DM'] = int(id)
        gl.settings['channel'] = 0
        with open('config.json', 'w') as j:
            json.dump(gl.settings, j)
        return '**DM <@!%s>**' % (id) 
    else:
        return 'Already listening.'


def channel_change(id):
    if id != gl.settings['channel']:
        gl.settings['channel'] = int(id)
        gl.settings['DM'] = 0
        with open('config.json', 'w') as j:
            json.dump(gl.settings, j)
        return '**Channel <#%s>**' % (id) 
    else:
        return 'Already listening.'


def ID_clear():
    gl.settings['channel'] = 0
    gl.settings['DM'] = 0
    with open('config.json', 'w') as j:
        json.dump(gl.settings, j)
    return '**ID cleared.**'


def add_mod(id):
    if id not in gl.settings['mods']:
        gl.settings['mods'].append(id)
        with open('config.json', 'w') as j:
            json.dump(gl.settings, j)
        return 'Added.'
    else:
        return 'Already there, chief.'


def remove_mod(id):
    if id in gl.settings['mods']:
        gl.settings['mods'].remove(id)
        with open('config.json', 'w') as j:
            json.dump(gl.settings, j)
        return 'Removed.'
    else:
        return 'There is no such ID in my database.'


def prefix_change(pr):
    if pr != gl.settings['prefix']:
        gl.settings['prefix'] = pr
        with open('config.json', 'w') as j:
            json.dump(gl.settings, j)
        return '**Prefix changed.**'
    else:
        return "'It's current prefix, dude.'"


def queue_add(guild_id, url):
    gl.queue[str(guild_id)]['tracks'].append(url)
    with open('queue.json', 'w') as j:
        json.dump(gl.queue, j)
    return 'Added.'


def queue_remove(guild_id, url):
    if url in gl.queue[str(guild_id)]['tracks']:
        gl.queue[str(guild_id)]['tracks'].remove(url)
        with open('config.json', 'w') as j:
            json.dump(gl.settings, j)
        return 'Removed.'
    else:
        return 'There is no such query in my database.'


def queue_clear():
    gl.queue = {}
    for guild in gl.bot.guilds:
        gl.queue[str(guild.id)] = {}
        gl.queue[str(guild.id)]['player'] = False
        gl.queue[str(guild.id)]['loop'] = False
        gl.queue[str(guild.id)]['tracks'] = []
    with open('queue.json', 'w') as j:
        json.dump(gl.queue, j)
    return '**Queue cleared**'
