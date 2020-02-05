import os
import random

import aiohttp
import discord
import sys
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

TOKEN = os.getenv('DISCORD_TOKEN')

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
    embed = discord.Embed(title=f'Taming Stats for {creature.capitalize()} Lvl {level}', url=url, description='')
    await ctx.send(embed=embed)


@bot.command(name='cat', help='meow')
async def cat(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://aws.random.cat/meow') as r:
            if r.status == 200:
                js = await r.json()
                await ctx.send(js['file'])


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
