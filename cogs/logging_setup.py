import discord  # Discord API wrapper
from discord import app_commands
from discord.ext import commands  # Discord BOT
import sqlite3 as sl


class setupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @app_commands.command(name="setup", description="Setup logging channels")
    # async def setup_logging(self, ctx: discord.Interaction):
    #     await create_category()
    #     return await ctx.response.send_message("All done", ephemeral=True)
    @commands.command()
    @commands.is_owner()
    async def setuplogging(self, ctx: commands.Context):
        corner = await ctx.guild.create_category(name="Ravens-corner")
        await corner.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False, connect=False)

        channels = await corner.create_text_channel(name="logs-channels")
        channels_url = (await channels.create_webhook(name="Raven-logging")).url

        messages = await corner.create_text_channel(name="logs-messages")
        messages_url = (await messages.create_webhook(name="Raven-logging")).url

        roles = await corner.create_text_channel(name="logs-roles")
        roles_url = (await roles.create_webhook(name="Raven-logging")).url

        threads = channels  # await corner.create_text_channel(name="logs-threads")
        threads_url = (await threads.create_webhook(name="Raven-logging")).url

        members = await corner.create_text_channel(name="logs-members")
        members_url = (await members.create_webhook(name="Raven-logging")).url

        guild = await corner.create_text_channel(name="logs-guild")
        guild_url = (await guild.create_webhook(name="Raven-logging")).url


        sql_connection = sl.connect('Raven.db')
        sql_connection.execute(
            "INSERT OR IGNORE INTO CHANNELS (GUILD_ID, WEBHOOK_URL, IS_ACTIVE) VALUES (?,?,?)",
            (int(ctx.guild.id), str(channels_url), 1))
        sql_connection.execute(
            "INSERT OR IGNORE INTO MESSAGES (GUILD_ID, WEBHOOK_URL, IS_ACTIVE) VALUES (?,?,?)",
            (int(ctx.guild.id), str(messages_url), 1))
        sql_connection.execute(
            "INSERT OR IGNORE INTO ROLES (GUILD_ID, WEBHOOK_URL, IS_ACTIVE) VALUES (?,?,?)",
            (int(ctx.guild.id), str(roles_url), 1))
        sql_connection.execute(
            "INSERT OR IGNORE INTO THREADS (GUILD_ID, WEBHOOK_URL, IS_ACTIVE) VALUES (?,?,?)",
            (int(ctx.guild.id), str(threads_url), 1))
        sql_connection.execute(
            "INSERT OR IGNORE INTO MEMBERS (GUILD_ID, WEBHOOK_URL, IS_ACTIVE) VALUES (?,?,?)",
            (int(ctx.guild.id), str(members_url), 1))
        sql_connection.execute(
            "INSERT OR IGNORE INTO GUILDS (GUILD_ID, WEBHOOK_URL, IS_ACTIVE) VALUES (?,?,?)",
            (int(ctx.guild.id), str(guild_url), 1))

        sql_connection.commit()
        return sql_connection.close()


async def setup(bot):
    await bot.add_cog(setupCog(bot))