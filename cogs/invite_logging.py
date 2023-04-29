import aiohttp  # Session for webhook
import discord  # Discord API wrapper
from discord.ext import commands  # Discord BOT
import sqlite3 as sl


class InviteLoggingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_invite_create')
    async def invite_created(self, invite: discord.Invite):
        # General info
        embed = discord.Embed(title=f"New invite created",
                              colour=discord.Colour.dark_green(),)

        embed.add_field(name=f"**Url:**", value=f"{invite.url}", inline=True)
        embed.add_field(name=f"**Created by:**", value=f"{invite.inviter}", inline=True)
        embed.add_field(name=f"**Channel:**", value=f"<#{invite.channel.id}>", inline=True)
        embed.add_field(name=f"**Max age:**", value=f"{invite.max_age}", inline=True)

        # Id info
        embed.set_footer(text=f"Invite Id: {invite.id}")

        # Send Webhook
        sql_connection = sl.connect('Raven.db')
        try:
            hook_url = sql_connection.execute(
                f"SELECT WEBHOOK_URL FROM GUILDS WHERE guild_id = {invite.guild.id}").fetchone()[0]
        except TypeError:
            return sql_connection.close()
        except sl.OperationalError:
            return sql_connection.close()
        sql_connection.close()

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=hook_url, session=session)
            await webhook.send(embed=embed, username='Raven - New invite',
                               avatar_url=self.bot.user.display_avatar.url)

    @commands.Cog.listener('on_invite_delete')
    async def invite_deleted(self, invite: discord.Invite):
        # General info
        embed = discord.Embed(title=f"Invite manually deleted",
                              colour=discord.Colour.dark_red(), )

        embed.add_field(name=f"**Url:**", value=f"{invite.url}", inline=True)

        # Id info
        embed.set_footer(text=f"Invite Id: {invite.id}")

        # Send Webhook
        sql_connection = sl.connect('Raven.db')
        try:
            hook_url = sql_connection.execute(
                f"SELECT WEBHOOK_URL FROM GUILDS WHERE guild_id = {invite.guild.id}").fetchone()[0]
        except TypeError:
            return sql_connection.close()
        except sl.OperationalError:
            return sql_connection.close()
        sql_connection.close()

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=hook_url, session=session)
            await webhook.send(embed=embed, username='Raven - Invite deleted',
                               avatar_url=self.bot.user.display_avatar.url)


async def setup(bot):
    sql_connection = sl.connect('Raven.db')
    sql_connection.execute(
        "CREATE TABLE IF NOT EXISTS GUILDS (GUILD_ID int, WEBHOOK_URL str, IS_ACTIVE int, primary key (GUILD_ID))")
    sql_connection.commit()
    sql_connection.close()
    await bot.add_cog(InviteLoggingCog(bot))
