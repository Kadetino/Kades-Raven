import aiohttp  # Session for webhook
import discord  # Discord API wrapper
from discord.ext import commands  # Discord BOT
import sqlite3 as sl
testing = "https://discord.com/api/webhooks/1101441632806653983/pa2bm6zmeNXeaQ9l6ehn2prARPCeuCNA8M4MncvpfTyCjnoATPXnoN27EF_-cGM2SVpv"

# Todo ????
class IntegrationLoggingCog(commands.Cog):
    """All the events related to Bots and Webhooks"""
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener('on_integration_create')
    async def integration_created(self, integration):
        pass

    @commands.Cog.listener('on_raw_integration_delete')
    async def channel_deleted(self, integration):
        pass

    @commands.Cog.listener('on_guild_channel_update')
    async def integration_updated(self, before, after):
        pass





async def setup(bot):
    await bot.add_cog(IntegrationLoggingCog(bot))