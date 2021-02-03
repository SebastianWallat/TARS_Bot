import discord
import sys
from discord.ext import commands
from environs import Env

from cogs.Ark import Ark
from cogs.Adlersson import Adlersson
from cogs.Animals import Animals
from cogs.Memes import Memes
from cogs.Util import Util
from helper import Helper

env = Env()
env.read_env()

TOKEN: str = env.str('DISCORD_TOKEN')
CAT_TOKEN: str = env.str('CAT_API_TOKEN')
LOAD_OPUS: bool = env.bool('LOAD_OPUS', False)

if TOKEN is None or CAT_TOKEN is None:
    raise EnvironmentError("TOKEN or CAT_API_TOKEN not specified")

bot = commands.Bot(command_prefix='!')

# load modules
bot.add_cog(Adlersson(bot))
bot.add_cog(Animals(bot, CAT_TOKEN))
bot.add_cog(Ark(bot))
bot.add_cog(Memes(bot))
bot.add_cog(Util(bot))


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!help"))
    if LOAD_OPUS:
        Helper.load_opus()
    print('bot started')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send('Sorry, i don\'t know this command')
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f'Please enter argument for: {error.param}')


@bot.event
async def on_error(event, *args):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Exception | Type: {sys.exc_info()}  Message: {args[0]}\n')
        else:
            raise


# start bot
bot.run(TOKEN)
input()
