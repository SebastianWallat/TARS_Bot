import ctypes

import discord


class Helper:
    def __init__(self):
        pass

    @staticmethod
    def load_opus():
        print("ctypes - Find opus:")
        a = ctypes.util.find_library('opus')
        print(a)

        print("Discord - Load Opus:")
        b = discord.opus.load_opus(a)
        print(b)

        print("Discord - Is loaded:")
        c = discord.opus.is_loaded()
        print(c)
        if not discord.opus.is_loaded():
            print("loading opus")
            discord.opus.load_opus('opus')