bot = []
settings = {}
queue = []
gifs = {}
typing = False
interaction = 0


async def send_msg(ctx, msg=None, text=None):
    if msg:
        if msg.attachments:
            files = []
            for attachment in msg.attachments:
                files.append(await attachment.to_file())
            if text is None:
                text = msg.content
            await ctx.send(content=text, files=files)
            return
        if text is None:
            text = msg.content
        await ctx.send(text)
        return
    else:
        await ctx.send(text)
