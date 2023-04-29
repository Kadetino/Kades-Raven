import aiohttp  # Session for webhook
import discord  # Discord API wrapper
from discord.ext import commands  # Discord BOT
import sqlite3 as sl


class RoleLoggingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_guild_role_create')
    async def role_created(self, role: discord.Role):
        # General info
        embed = discord.Embed(title=f"New role was created",
                              colour=discord.Colour.green(),
                              description=f"**{role.name}** (<@&{role.id}>) was created.")

        # Id info
        embed.set_footer(text=f"Role Id: {role.id}")

        # Send Webhook
        sql_connection = sl.connect('Raven.db')
        try:
            hook_url = sql_connection.execute(
                f"SELECT WEBHOOK_URL FROM ROLES WHERE guild_id = {role.guild.id}").fetchone()[0]
        except TypeError:
            return sql_connection.close()
        except sl.OperationalError:
            return sql_connection.close()
        sql_connection.close()

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=hook_url, session=session)
            await webhook.send(embed=embed, username='Raven - Role created',
                               avatar_url=self.bot.user.display_avatar.url)

    @commands.Cog.listener('on_guild_role_delete')
    async def role_deleted(self, role: discord.Role):
        # General info
        embed = discord.Embed(title=f"Role was deleted",
                              colour=discord.Colour.red(),
                              description=f"**`{role.name}`** was deleted.")

        # Id info
        embed.set_footer(text=f"Role Id: {role.id}")

        # Send Webhook
        sql_connection = sl.connect('Raven.db')
        try:
            hook_url = sql_connection.execute(
                f"SELECT WEBHOOK_URL FROM ROLES WHERE guild_id = {role.guild.id}").fetchone()[0]
        except TypeError:
            return sql_connection.close()
        except sl.OperationalError:
            return sql_connection.close()
        sql_connection.close()

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=hook_url, session=session)
            await webhook.send(embed=embed, username='Raven - Role deleted',
                               avatar_url=self.bot.user.display_avatar.url)

    @commands.Cog.listener('on_guild_role_update')
    async def role_updated(self, before: discord.Role, after: discord.Role):
        if before.position == after.position and before.permissions.value == after.permissions.value and before.name == after.name:
            return
        # General info
        elif before.position != after.position and before.permissions.value == after.permissions.value:
            embed = discord.Embed(title=f"Role was moved",
                                  colour=discord.Colour.light_gray(),
                                  description=f"**{before.name}** (<@&{after.id}>) was moved.\n"
                                              f"{before.position} -> {after.position}")
        else:
            embed = discord.Embed(title=f"Role was updated",
                                  colour=discord.Colour.yellow(),
                                  description=f"**{before.name}** (<@&{after.id}>) was updated.")

        # Id info
        embed.set_footer(text=f"Role Id: {after.id}")

        # Send Webhook
        sql_connection = sl.connect('Raven.db')
        try:
            hook_url = sql_connection.execute(
                f"SELECT WEBHOOK_URL FROM ROLES WHERE guild_id = {after.guild.id}").fetchone()[0]
        except TypeError:
            return sql_connection.close()
        except sl.OperationalError:
            return sql_connection.close()
        sql_connection.close()

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=hook_url, session=session)
            await webhook.send(embed=embed, username='Raven - Role updated',
                               avatar_url=self.bot.user.display_avatar.url)


async def setup(bot):
    sql_connection = sl.connect('Raven.db')
    sql_connection.execute(
        "CREATE TABLE IF NOT EXISTS ROLES (GUILD_ID int, WEBHOOK_URL str, IS_ACTIVE int, primary key (GUILD_ID))")
    sql_connection.commit()
    sql_connection.close()
    await bot.add_cog(RoleLoggingCog(bot))
