import json
import random

import aiohttp
import discord
import sys
from discord.ext import commands
from environs import Env

env = Env()
env.read_env()

TOKEN = env.str('DISCORD_TOKEN')
CAT_TOKEN = env.str('CAT_API_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='3D Schach'))
    print('bot started')


@bot.command(name='hi', help='Say hi to the bot')
async def hi(ctx):
    responses = [
        'Hi',
        'Hello!',
    ]

    response = random.choice(responses)
    await ctx.send(response)


@bot.command(name='tame', help='get ark taming stats')
async def tame(ctx, creature, level):
    base = "https://www.dododex.com/taming/"
    url = base + creature.lower() + '/' + level
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                embed = discord.Embed(title=f'Taming stats for {creature} with lvl. {level}', url=url, description='')
                await ctx.send(embed=embed)
            else:
                await ctx.send(f'I found no stats for {creature}')


@bot.command(name='cat', help='meow')
async def cat(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.thecatapi.com/v1/images/search?format=json?api_key={CAT_TOKEN}') as r:
            if r.status == 200:
                js = await r.json()
                url = js[0]["url"]
                embed = discord.Embed(title='Meow', url=url, description='')
                embed.set_image(url=url)
                await ctx.send(embed=embed)


@bot.command(name='wiki', help='search Ark wiki')
async def wiki(ctx, search):
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


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send('Sorry, i don\'t know this command')
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f'Please enter argument for: {error.param}')


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Exception | Type: {sys.exc_info()}  Message: {args[0]}\n')
        else:
            raise


# start bot
bot.run(TOKEN)
input()
