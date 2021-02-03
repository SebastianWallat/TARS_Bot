import os
import random

import discord
from discord.ext import commands


class Adlersson(commands.Cog):
    MP3_DIR = os.path.join(os.getcwd(), './mp3/adlersson')

    def __init__(self, bot):
        self.bot = bot
        self._adlerson_mp3_files = os.listdir(self.MP3_DIR)

    @commands.group(aliases=['8i'])
    async def adlersson(self, ctx):
        if ctx.invoked_subcommand is None:
            self.soundboard.invoke()

    @adlersson.command(name='soundboard', aliases=['rnd'], help='random one')
    async def soundboard(self, ctx):
        # select file to play
        audio_file = random.choice(self._adlerson_mp3_files)
        path = os.path.join(self.MP3_DIR, audio_file)

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(path))
        # noinspection PyUnresolvedReferences
        try:
            ctx.voice_client.play(source)
        except Exception as e:
            raise commands.CommandError(f"Error playing voice: {repr(e)}")

    @adlersson.command(name='list', help='list soundboard options')
    async def list(self, ctx):
        msg = '```'
        for idx in range(0, len(self._adlerson_mp3_files)):
            msg += f"[{idx}]  {self._adlerson_mp3_files[idx].replace('_', ' ')}\n"
        msg += '```'
        await ctx.send(msg)

    @adlersson.command(name='play', help='play soundboard entry (index)')
    async def play(self, ctx, idx: int):
        # select file to play
        audio_file = self._adlerson_mp3_files[idx]
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

