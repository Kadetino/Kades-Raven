import aiohttp  # Session for webhook
import discord  # Discord API wrapper
from discord.ext import commands  # Discord BOT
import sqlite3 as sl


class ChannelLoggingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_guild_channel_create')
    async def channel_created(self, channel):
        # General info
        embed = discord.Embed(title=f"New channel was created",
                              colour=discord.Colour.green(),
                              description=f"**`{channel.name}`** (<#{channel.id}>) was created.")

        # Id info
        embed.set_footer(text=f"Channel Id: {channel.id}")

        # Send Webhook
        sql_connection = sl.connect('Raven.db')
        try:
            hook_url = sql_connection.execute(
                f"SELECT WEBHOOK_URL FROM CHANNELS WHERE guild_id = {channel.guild.id}").fetchone()[0]
        except TypeError:
            return sql_connection.close()
        except sl.OperationalError:
            return sql_connection.close()
        sql_connection.close()

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=hook_url, session=session)
            await webhook.send(embed=embed, username='Raven - Channel created',
                               avatar_url=self.bot.user.display_avatar.url)

    @commands.Cog.listener('on_guild_channel_delete')
    async def channel_deleted(self, channel):
        # General info
        embed = discord.Embed(title=f"Channel was deleted",
                              colour=discord.Colour.red(),
                              description=f"**`{channel.name}`** was deleted.")

        # Id info
        embed.set_footer(text=f"Channel Id: {channel.id}")

        # Send Webhook
        sql_connection = sl.connect('Raven.db')
        try:
            hook_url = sql_connection.execute(
                f"SELECT WEBHOOK_URL FROM CHANNELS WHERE guild_id = {channel.guild.id}").fetchone()[0]
        except TypeError:
            return sql_connection.close()
        except sl.OperationalError:
            return sql_connection.close()
        sql_connection.close()

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=hook_url, session=session)
            await webhook.send(embed=embed, username='Raven - Channel deleted',
                               avatar_url=self.bot.user.display_avatar.url)

    @commands.Cog.listener('on_guild_channel_update')
    async def channel_updated(self, before, after):
        if (before.position == after.position and before.category == after.category) and before.name == after.name:
            return
        # General info
        elif before.position != after.position or before.category != after.category and before.name == after.name:
            embed = discord.Embed(title=f"Channel was moved",
                                  colour=discord.Colour.light_gray(),
                                  description=f"**{before.name}** (<#{after.id}>) was moved.\n"
                                              f"{before.category} -> {after.category}\n"
                                              f"{before.position} -> {after.position}")
        else:
            embed = discord.Embed(title=f"Channel was updated",
                                  colour=discord.Colour.yellow(),
                                  description=f"**{before.name}** (<#{after.id}>) was updated.")

        # Id info
        embed.set_footer(text=f"Channel Id: {after.id}")

        # Send Webhook
        sql_connection = sl.connect('Raven.db')
        try:
            hook_url = sql_connection.execute(
                f"SELECT WEBHOOK_URL FROM CHANNELS WHERE guild_id = {after.guild.id}").fetchone()[0]
        except TypeError:
            return sql_connection.close()
        except sl.OperationalError:
            return sql_connection.close()
        sql_connection.close()


        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=hook_url, session=session)
            await webhook.send(embed=embed, username='Raven - Channel updated',
                               avatar_url=self.bot.user.display_avatar.url)


async def setup(bot):
    sql_connection = sl.connect('Raven.db')
    sql_connection.execute(
        "CREATE TABLE IF NOT EXISTS CHANNELS (GUILD_ID int, WEBHOOK_URL str, IS_ACTIVE int, primary key (GUILD_ID))")
    sql_connection.commit()
    sql_connection.close()
    await bot.add_cog(ChannelLoggingCog(bot))
