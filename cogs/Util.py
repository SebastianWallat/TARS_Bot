import random
import discord
from discord.ext import commands


class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hi', help='Say hi to the bot')
    async def hi(self, ctx):
        responses = [
            'Hi',
            'Hello!',
        ]

        response = random.choice(responses)
        await ctx.send(response)

    @commands.command(name='leave', aliases=['l'], help='leave your voice channel')
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            if ctx.author.voice:
                await ctx.author.voice.channel.disconnect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")