import aiohttp
import discord
from discord.ext import commands


class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='meme', help='random meme')
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://some-random-api.ml/meme') as r:
                if r.status == 200:
                    js = await r.json()
                    url = js['image']
                    caption = js['caption']
                    embed = discord.Embed(title=caption, url=url, description='')
                    embed.set_image(url=url)
                    await ctx.send(embed=embed)