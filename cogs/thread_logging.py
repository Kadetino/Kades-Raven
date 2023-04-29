import aiohttp  # Session for webhook
import discord  # Discord API wrapper
from discord.ext import commands  # Discord BOT
import sqlite3 as sl


class ThreadLoggingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_thread_join')
    async def thread_created(self, thread):
        # General info
        embed = discord.Embed(title=f"New thread was joined",
                              colour=discord.Colour.green(),
                              description=f"**`{thread.name}`** (<#{thread.id}>) was joined.")

        # Id info
        embed.set_footer(text=f"Thread Id: {thread.id}")

        # Send Webhook
        sql_connection = sl.connect('Raven.db')
        try:
            hook_url = sql_connection.execute(
                f"SELECT WEBHOOK_URL FROM THREADS WHERE guild_id = {thread.guild.id}").fetchone()[0]
        except TypeError:
            return sql_connection.close()
        except sl.OperationalError:
            return sql_connection.close()
        sql_connection.close()

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=hook_url, session=session)
            await webhook.send(embed=embed, username='Raven - Thread joined',
                               avatar_url=self.bot.user.display_avatar.url)

    @commands.Cog.listener('on_thread_create')
    async def thread_created(self, thread):
        # General info
        embed = discord.Embed(title=f"New thread was created",
                              colour=discord.Colour.dark_green(),
                              description=f"**`{thread.name}`** (<#{thread.id}>) was created.")

        # Id info
        embed.set_footer(text=f"Thread Id: {thread.id}")

        # Send Webhook
        sql_connection = sl.connect('Raven.db')
        try:
            hook_url = sql_connection.execute(
                f"SELECT WEBHOOK_URL FROM THREADS WHERE guild_id = {thread.guild.id}").fetchone()[0]
        except TypeError:
            return sql_connection.close()
        except sl.OperationalError:
            return sql_connection.close()
        sql_connection.close()

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=hook_url, session=session)
            await webhook.send(embed=embed, username='Raven - Thread created',
                               avatar_url=self.bot.user.display_avatar.url)

    @commands.Cog.listener('on_thread_remove')
    async def thread_removed(self, thread):
        # General info
        embed = discord.Embed(title=f"Thread was removed",
                              colour=discord.Colour.orange(),
                              description=f"**`{thread.name}`** was removed.")

        # Id info
        embed.set_footer(text=f"Thread Id: {thread.id}")

        # Send Webhook
        sql_connection = sl.connect('Raven.db')
        try:
            hook_url = sql_connection.execute(
                f"SELECT WEBHOOK_URL FROM THREADS WHERE guild_id = {thread.guild.id}").fetchone()[0]
        except TypeError:
            return sql_connection.close()
        except sl.OperationalError:
            return sql_connection.close()
        sql_connection.close()

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=hook_url, session=session)
            await webhook.send(embed=embed, username='Raven - Thread removed',
                               avatar_url=self.bot.user.display_avatar.url)

    @commands.Cog.listener('on_thread_delete')
    async def thread_deleted(self, thread):
        # General info
        embed = discord.Embed(title=f"Thread was deleted",
                              colour=discord.Colour.dark_red(),
                              description=f"**`{thread.name}`** was deleted.")

        # Id info
        embed.set_footer(text=f"Thread Id: {thread.id}")

        # Send Webhook
        sql_connection = sl.connect('Raven.db')
        try:
            hook_url = sql_connection.execute(
                f"SELECT WEBHOOK_URL FROM THREADS WHERE guild_id = {thread.guild.id}").fetchone()[0]
        except TypeError:
            return sql_connection.close()
        except sl.OperationalError:
            return sql_connection.close()
        sql_connection.close()

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=hook_url, session=session)
            await webhook.send(embed=embed, username='Raven - Thread deleted',
                               avatar_url=self.bot.user.display_avatar.url)


async def setup(bot):
    sql_connection = sl.connect('Raven.db')
    sql_connection.execute(
        "CREATE TABLE IF NOT EXISTS THREADS (GUILD_ID int, WEBHOOK_URL str, IS_ACTIVE int, primary key (GUILD_ID))")
    sql_connection.commit()
    sql_connection.close()
    await bot.add_cog(ThreadLoggingCog(bot))
