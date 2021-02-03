import aiohttp
import discord
from discord.ext import commands


class Animals(commands.Cog):
    def __init__(self, bot, cat_token):
        self.bot = bot
        self._cat_api_token = cat_token

    @commands.command(name='cat-fact', help='cat facts')
    async def cat_fact(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://some-random-api.ml/facts/cat') as r:
                if r.status == 200:
                    js = await r.json()
                    desc = js['fact']
                    embed = discord.Embed(title='Cat Fact:', description=desc)
                    await ctx.send(embed=embed)

    @commands.command(name='fox', help='random fox image')
    async def fox(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://some-random-api.ml/img/fox') as r:
                if r.status == 200:
                    js = await r.json()
                    url = js['link']
                    embed = discord.Embed(title='Fox', url=url, description='')
                    embed.set_image(url=url)
                    await ctx.send(embed=embed)

    @commands.command(name='cat', help='meow')
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.thecatapi.com/v1/images/search?format=json?api_key={self._cat_api_token}') as r:
                if r.status == 200:
                    js = await r.json()
                    url = js[0]['url']
                    embed = discord.Embed(title='Meow', url=url, description='')
                    embed.set_image(url=url)
                    await ctx.send(embed=embed)