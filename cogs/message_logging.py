import aiohttp  # Session for webhook
import discord  # Discord API wrapper
from discord.ext import commands  # Discord BOT
import sqlite3 as sl
from other import web_pfp_gen


class MessageLoggingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_message_edit')
    async def msg_edited(self, before: discord.message.Message, after: discord.message.Message):
        # Check if webhook or bot message
        if before.author.bot:
            return

        # Check if change actually happened (e.g creating threads)
        if before.content == after.content:
            return

        # General info
        embed = discord.Embed(description=f"[Message]({before.jump_url}) was edited",
                              colour=discord.Colour.yellow(), )

        # Remove ` symbols
        a_msg_content = after.content.replace("`", "'")
        b_msg_content = before.content.replace("`", "'")

        # Message contents
        embed.add_field(name=f"**Old message:**",
                        value=f"```{b_msg_content}```",
                        inline=False)
        embed.add_field(name=f"**New message:**",
                        value=f"```{a_msg_content}```",
                        inline=False)
        # Author info
        embed.set_author(name=before.author, icon_url=before.author.display_avatar.url)
        embed.add_field(name=f"**Author:**",
                        value=f"{after.author.display_name} (<@{after.author.id}>)",
                        inline=True)
        # Channel info
        embed.add_field(name=f"**Channel:**",
                        value=f"{after.channel.name} (<#{after.channel.id}>)", inline=True)

        # Id info
        embed.set_footer(text=f"Message Id: {before.id}")

        # Webhook image
        web_pfp = web_pfp_gen("thread", "red")
        web_pfp = discord.File(web_pfp,
                               filename=f"web_pfp.png")
        # embed.set_thumbnail(url=f"attachment://skand_frog.png")

        # Send Webhook
        sql_connection = sl.connect('Raven.db')
        try:
            hook_url = sql_connection.execute(
                f"SELECT WEBHOOK_URL FROM MESSAGES WHERE guild_id = {before.guild.id}").fetchone()[0]
        except TypeError:
            return sql_connection.close()
        except sl.OperationalError:
            return sql_connection.close()
        sql_connection.close()

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=hook_url, session=session)
            await webhook.send(embed=embed, username='Raven - Message edited',
                               avatar_url=web_pfp)#self.bot.user.display_avatar.url)

    @commands.Cog.listener('on_message_delete')
    async def msg_deleted(self, message: discord.message.Message):
        # Check if webhook or bot message
        if message.author.bot:
            return

        # General info
        embed = discord.Embed(description=f"Message was deleted",
                              colour=discord.Colour.red(), )

        # Remove ` symbols
        msg_content = message.content.replace("`", "'")

        # Message contents
        embed.add_field(name=f"**Deleted message:**",
                        value=f"```{msg_content}```",
                        inline=False)
        # Author info
        embed.set_author(name=message.author, icon_url=message.author.display_avatar.url)
        embed.add_field(name=f"**Author:**",
                        value=f"{message.author.display_name} (<@{message.author.id}>)",
                        inline=True)
        # Channel info
        embed.add_field(name=f"**Channel:**",
                        value=f"{message.channel.name} (<#{message.channel.id}>)", inline=True)

        # Id info
        embed.set_footer(text=f"Message Id: {message.id}")

        # Send Webhook
        sql_connection = sl.connect('Raven.db')
        try:
            hook_url = sql_connection.execute(
                f"SELECT WEBHOOK_URL FROM MESSAGES WHERE guild_id = {message.guild.id}").fetchone()[0]
        except TypeError:
            return sql_connection.close()
        except sl.OperationalError:
            return sql_connection.close()
        sql_connection.close()

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=hook_url, session=session)
            await webhook.send(embed=embed, username='Raven - Message deleted',
                               avatar_url=self.bot.user.display_avatar.url)

    @commands.Cog.listener('on_bulk_message_delete')
    async def msg_bulk_deleted(self, messages):
        # General info
        embed = discord.Embed(description=f"**Purge was detected**",
                              colour=discord.Colour.dark_red(), )
        # Message contents
        embed.add_field(name=f"**Number of messages:**",
                        value=f"{len(messages)} messages were bulk deleted.",
                        inline=False)

        # Send Webhook
        sql_connection = sl.connect('Raven.db')
        try:
            hook_url = sql_connection.execute(
                f"SELECT WEBHOOK_URL FROM MESSAGES WHERE guild_id = {messages[0].guild.id}").fetchone()[0]
        except TypeError:
            return sql_connection.close()
        except sl.OperationalError:
            return sql_connection.close()
        sql_connection.close()
        if hook_url is None:
            return

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=hook_url, session=session)
            await webhook.send(embed=embed, username='Raven - Purge',
                               avatar_url=self.bot.user.display_avatar.url)


async def setup(bot):
    sql_connection = sl.connect('Raven.db')
    sql_connection.execute(
        "CREATE TABLE IF NOT EXISTS MESSAGES (GUILD_ID int, WEBHOOK_URL str, IS_ACTIVE int, primary key (GUILD_ID))")
    sql_connection.commit()
    sql_connection.close()
    await bot.add_cog(MessageLoggingCog(bot))
