import os
import random

import aiohttp
import discord
from discord.ext import commands


class Ark(commands.Cog):
    MP3_DIR = os.path.join(os.getcwd(), './mp3/ark')

    def __init__(self, bot):
        self.bot = bot
        self._ark_mp3_files = os.listdir(self.MP3_DIR)

    @commands.group()
    async def ark(self, ctx):
        pass

    @ark.command(name='tame', help='get ark taming stats')
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

    @ark.command(name='wiki', help='search Ark wiki')
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

    @ark.command(name='soundboard', aliases=['rnd'], help='random one')
    async def soundboard(self, ctx):
        # select file to play
        audio_file = random.choice(self._ark_mp3_files)
        path = os.path.join(self.MP3_DIR, audio_file)

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(path))
        # noinspection PyUnresolvedReferences
        try:
            ctx.voice_client.play(source)
        except Exception as e:
            raise commands.CommandError(f"Error playing voice: {repr(e)}")

    @ark.command(name='list', help='list soundboard options')
    async def list(self, ctx):
        msg = '```'
        for idx in range(0, len(self._ark_mp3_files)):
            msg += f"[{idx}]  {self._ark_mp3_files[idx].replace('_', ' ')}\n"
        msg += '```'
        await ctx.send(msg)

    @ark.command(name='play', help='play soundboard entry (index)')
    async def play(self, ctx, idx: int):
        # select file to play
        audio_file = self._ark_mp3_files[idx]
        path = os.path.join(self.MP3_DIR, audio_file)

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(path))
        # noinspection PyUnresolvedReferences
        try:
            ctx.voice_client.play(source)
        except Exception as e:
            raise commands.CommandError(f"Error playing voice: {repr(e)}")

    @soundboard.before_invoke
    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()