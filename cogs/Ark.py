import aiohttp
import discord
from discord.ext import commands


class Ark(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='tame', help='get ark taming stats')
    async def tame(self, ctx, creature, level):
        base = "https://www.dododex.com/taming/"
        url = base + creature.lower() + '/' + level
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    embed = discord.Embed(title=f'Taming stats for {creature} with lvl. {level}', url=url,
                                          description='')
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f'I found no stats for {creature}')

    @commands.command(name='wiki', help='search Ark wiki')
    async def wiki(self, ctx, search):
        base = 'https://ark.gamepedia.com/'
        if not search[0].isupper():
            search = search.capitalize()

        url = base + search
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    embed = discord.Embed(title=f'Wiki entry for {search}', url=url, description='')
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f'I found no wiki page for {search}')