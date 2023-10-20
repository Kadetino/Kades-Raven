import aiohttp  # Session for webhook
import discord  # Discord API wrapper
from discord.ext import commands  # Discord BOT
from PIL import Image  # Webhook icons
import sqlite3 as sl


class MemberLoggingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_member_join')
    async def member_joined(self, member: discord.Member):
        # General info
        embed = discord.Embed(title=f"New member",
                              colour=discord.Colour.green(),
                              description=f"<@{member.id}> has joined.")
        embed.set_author(name=member, icon_url=member.display_avatar.url)

        # Webhook image
        web_pfp = discord.File(f"gfx/skand_frog.png",
                               filename=f"skand_frog.png")
        embed.set_thumbnail(url=f"attachment://skand_frog.png")

        # Discord member since
        since = f"{member.created_at}"
        since = since[:since.find(" "):]
        embed.add_field(name=f"Discord user since:", value=since, inline=False)

        # Id info
        embed.set_footer(text=f"Member Id: {member.id}")

        # Send Webhook
        sql_connection = sl.connect('Raven.db')
        try:
            hook_url = \
                sql_connection.execute(
                    f"SELECT WEBHOOK_URL FROM MEMBERS WHERE guild_id = {member.guild.id}").fetchone()[0]
        except TypeError:
            return sql_connection.close()
        except sl.OperationalError:
            return sql_connection.close()
        sql_connection.close()

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=hook_url, session=session)
            await webhook.send(embed=embed, username='Raven - New member',
                               avatar_url=self.bot.user.display_avatar.url)

    @commands.Cog.listener('on_member_remove')
    async def member_left(self, member: discord.Member):
        # General info
        embed = discord.Embed(title=f"Member left",
                              colour=discord.Colour.greyple(),
                              description=f"<@{member.id}> has left.")
        embed.set_author(name=member, icon_url=member.display_avatar.url)

        # Id info
        embed.set_footer(text=f"Member Id: {member.id}")
        # Roles
        roles = []
        for role in member.roles:
            if role.name == "@everyone":
                continue
            roles.append(f"<@&{role.id}>")
        if roles:
            embed.add_field(name=f"Roles:",
                            value=f"{','.join(roles)}",
                            inline=True)
        # Send Webhook
        sql_connection = sl.connect('Raven.db')
        try:
            hook_url = \
                sql_connection.execute(
                    f"SELECT WEBHOOK_URL FROM MEMBERS WHERE guild_id = {member.guild.id}").fetchone()[0]
        except TypeError:
            return sql_connection.close()
        except sl.OperationalError:
            return sql_connection.close()
        sql_connection.close()

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=hook_url, session=session)
            await webhook.send(embed=embed, username='Raven - Member left',
                               avatar_url=self.bot.user.display_avatar.url)

    @commands.Cog.listener('on_member_update')
    async def member_update(self, before: discord.Member, after: discord.Member):
        # Get Webhook
        sql_connection = sl.connect('Raven.db')
        try:
            hook_url = \
                sql_connection.execute(
                    f"SELECT WEBHOOK_URL FROM MEMBERS WHERE guild_id = {after.guild.id}").fetchone()[0]
        except TypeError:
            return sql_connection.close()
        except sl.OperationalError:
            return sql_connection.close()
        sql_connection.close()

        # Nickname was changed
        if before.nick != after.nick:
            # General info
            embed = discord.Embed(title=f"Nickname changed",
                                  colour=discord.Colour.light_gray())
            embed.set_author(name=after, icon_url=after.display_avatar.url)

            # Old
            bnick = str(before.nick)
            if bnick == "None":
                bnick = "-"
            embed.add_field(name=f"Old:",
                            value=f"{bnick}",
                            inline=True)
            # New
            anick = str(after.nick)
            if anick == "None":
                anick = "-"
            embed.add_field(name=f"New:",
                            value=f"{anick}",
                            inline=True)

            # User info
            embed.add_field(name=f"**User affected:**",
                            value=f"<@{after.id}>",
                            inline=False)
            embed.set_footer(text=f"Member Id: {after.id}")
            # Send Webhook
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(url=hook_url, session=session)
                await webhook.send(embed=embed, username='Raven - Nickname changed',
                                   avatar_url=self.bot.user.display_avatar.url)
        if before.roles != after.roles:
            # General info
            embed = discord.Embed(title=f"Roles changed",
                                  colour=discord.Colour.yellow())
            embed.set_author(name=after, icon_url=after.display_avatar.url)
            # Id info
            embed.set_footer(text=f"Member Id: {after.id}")
            # Retrieve roles
            broles = []
            for role in before.roles:
                broles.append(f"<@&{role.id}>")
            aroles = []
            for role in after.roles:
                aroles.append(f"<@&{role.id}>")
            # Difference
            diff = list(set(broles).difference(aroles))
            added = []
            removed = []
            for role in diff:
                removed.append(role)
            diff = list(set(aroles).difference(broles))
            for role in diff:
                added.append(role)
            if len(added) > 0:
                embed.add_field(name=f"Added roles:",
                                value=f"{','.join(added)}",
                                inline=True)
            # Delete
            if len(removed) > 0:
                embed.add_field(name=f"Removed roles:",
                                value=f"{','.join(removed)}",
                                inline=True)
            # User info
            embed.add_field(name=f"**User affected:**",
                            value=f"<@{after.id}>",
                            inline=False)
            embed.set_footer(text=f"Member Id: {after.id}")

            # Send Webhook
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(url=hook_url, session=session)
                await webhook.send(embed=embed, username='Raven - Roles changed',
                                   avatar_url=self.bot.user.display_avatar.url)
        if before.timed_out_until != after.timed_out_until:
            # General info
            embed = discord.Embed(title=f"Timeout changed",
                                  colour=discord.Colour.dark_red())
            embed.set_author(name=after, icon_url=after.display_avatar.url)

            # Old
            until = f"{before.timed_out_until}"
            if until != "None":
                until = until[:until.find("."):]
            else:
                until = "-"
            embed.add_field(name=f"Old:",
                            value=f"{until}",
                            inline=True)
            # New
            until = f"{after.timed_out_until}"
            if until != "None":
                until = until[:until.find("."):]
            else:
                until = "-"
            embed.add_field(name=f"New:",
                            value=f"{until}",
                            inline=True)

            # User info
            embed.add_field(name=f"**User affected:**",
                            value=f"<@{after.id}>",
                            inline=False)
            embed.set_footer(text=f"Member Id: {after.id}")

            # Send Webhook
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(url=hook_url, session=session)
                await webhook.send(embed=embed, username='Raven - Timeout changed',
                                   avatar_url=self.bot.user.display_avatar.url)

        return

    @commands.Cog.listener('on_member_ban')
    async def member_banned(self, guild: discord.Guild, user: discord.Member):
        # General info
        embed = discord.Embed(title=f"Member banned",
                              colour=discord.Colour.red(),
                              description=f"<@{user.id}> has been banned.")
        embed.set_author(name=user, icon_url=user.display_avatar.url)

        # Id info
        embed.set_footer(text=f"Member Id: {user.id}")

        # Send Webhook
        sql_connection = sl.connect('Raven.db')
        try:
            hook_url = \
                sql_connection.execute(f"SELECT WEBHOOK_URL FROM MEMBERS WHERE guild_id = {guild.id}").fetchone()[0]
        except TypeError:
            return sql_connection.close()
        except sl.OperationalError:
            return sql_connection.close()
        sql_connection.close()

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=hook_url, session=session)
            await webhook.send(embed=embed, username='Raven - Member banned',
                               avatar_url=self.bot.user.display_avatar.url)

    @commands.Cog.listener('on_member_unban')
    async def member_unbanned(self, guild: discord.Guild, user: discord.Member):
        # General info
        embed = discord.Embed(title=f"Member unbanned",
                              colour=discord.Colour.green(),
                              description=f"<@{user.id}> has been unbanned.\n"
                                          f"")
        embed.set_author(name=user, icon_url=user.display_avatar.url)

        # Id info
        embed.set_footer(text=f"Member Id: {user.id}")

        # Send Webhook
        sql_connection = sl.connect('Raven.db')
        try:
            hook_url = \
                sql_connection.execute(f"SELECT WEBHOOK_URL FROM MEMBERS WHERE guild_id = {guild.id}").fetchone()[0]
        except TypeError:
            return sql_connection.close()
        except sl.OperationalError:
            return sql_connection.close()
        sql_connection.close()

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=hook_url, session=session)
            await webhook.send(embed=embed, username='Raven - Member unbanned',
                               avatar_url=self.bot.user.display_avatar.url)


async def setup(bot):
    sql_connection = sl.connect('Raven.db')
    sql_connection.execute(
        "CREATE TABLE IF NOT EXISTS MEMBERS (GUILD_ID int, WEBHOOK_URL str, IS_ACTIVE int, primary key (GUILD_ID))")
    sql_connection.commit()
    sql_connection.close()
    await bot.add_cog(MemberLoggingCog(bot))
