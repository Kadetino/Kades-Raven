import aiohttp  # Session for webhook
import discord  # Discord API wrapper
from discord.ext import commands  # Discord BOT
import sqlite3 as sl


class EmojiNStickersLoggingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_guild_stickers_update')
    async def stickers_updated(self, guild: discord.Guild, before, after):
        # Get Webhook
        sql_connection = sl.connect('Raven.db')
        try:
            hook_url = \
                sql_connection.execute(
                    f"SELECT WEBHOOK_URL FROM GUILDS WHERE guild_id = {guild.id}").fetchone()[0]
        except TypeError:
            return sql_connection.close()
        except sl.OperationalError:
            return sql_connection.close()
        sql_connection.close()

        # Send Webhook
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=hook_url, session=session)

            # Difference - Removed
            diff = list(set(before).difference(after))
            for sticker in diff:
                embed = discord.Embed(title=f"Sticker removed",
                                      colour=discord.Colour.red())
                embed.set_footer(text=f"Guild Id: {guild.id}")
                embed.add_field(name=f"**Name:**",
                                value=f"{sticker.name}",
                                inline=False)
                embed.add_field(name=f"**Format:**",
                                value=f"{str(sticker.format)[str(sticker.format).find('.')::]}",
                                inline=True)
                embed.add_field(name=f"**Unicode emoji:**",
                                value=f":{sticker.emoji}:",
                                inline=True)
                if sticker.description:
                    embed.add_field(name=f"**Description:**",
                                    value=f"{sticker.description}",
                                    inline=True)
                await webhook.send(embed=embed, username='Raven - Stickers updated',
                                   avatar_url=self.bot.user.display_avatar.url)

            # Difference - Added
            diff = list(set(after).difference(before))
            for sticker in diff:
                embed = discord.Embed(title=f"Sticker added",
                                      colour=discord.Colour.green())
                embed.set_footer(text=f"Guild Id: {guild.id}")
                embed.add_field(name=f"**Name:**",
                                value=f"{sticker.name}",
                                inline=False)
                embed.add_field(name=f"**Format:**",
                                value=f"{str(sticker.format)[str(sticker.format).find('.')::]}",
                                inline=True)
                embed.add_field(name=f"**Unicode emoji:**",
                                value=f":{sticker.emoji}:",
                                inline=True)
                if sticker.description:
                    embed.add_field(name=f"**Description:**",
                                    value=f"{sticker.description}",
                                    inline=True)
                await webhook.send(embed=embed, username='Raven - Stickers updated',
                                   avatar_url=self.bot.user.display_avatar.url)

            # Checking for namechanges
            for after_sticker in after:
                for before_sticker in before:
                    if before_sticker.id == after_sticker.id and after_sticker.name != before_sticker.name:
                        embed = discord.Embed(title=f"Sticker renamed",
                                              colour=discord.Colour.yellow(),)
                        embed.set_footer(text=f"Guild Id: {guild.id}")
                        embed.set_author(name=f"{before_sticker.name} -> {after_sticker.name}",
                                         icon_url=after_sticker.url)
                        temp = before_sticker.name.replace('`', "'")
                        embed.add_field(name=f"**Old name:**",
                                        value=f"```{temp}```",
                                        inline=False)
                        temp = after_sticker.name.replace('`', "'")
                        embed.add_field(name=f"**New name:**",
                                        value=f"```{temp}```",
                                        inline=False)
                        embed.add_field(name=f"**Format:**",
                                        value=f"{str(after_sticker.format)[str(after_sticker.format).find('.')::]}",
                                        inline=True)
                        embed.add_field(name=f"**Unicode emoji:**",
                                        value=f":{after_sticker.emoji}:",
                                        inline=True)
                        await webhook.send(embed=embed, username='Raven - Sticker updated',
                                           avatar_url=self.bot.user.display_avatar.url)

        return

    @commands.Cog.listener('on_guild_emojis_update')
    async def emojis_updated(self, guild: discord.Guild, before, after):
        # Get Webhook
        sql_connection = sl.connect('Raven.db')
        try:
            hook_url = \
                sql_connection.execute(
                    f"SELECT WEBHOOK_URL FROM GUILDS WHERE guild_id = {guild.id}").fetchone()[0]
        except TypeError:
            return sql_connection.close()
        except sl.OperationalError:
            return sql_connection.close()
        sql_connection.close()

        # Send Webhook
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=hook_url, session=session)

            # Difference - Removed
            diff = list(set(before).difference(after))
            for emoji in diff:
                embed = discord.Embed(title=f"Emoji removed",
                                      colour=discord.Colour.red())
                embed.set_footer(text=f"Guild Id: {guild.id}")
                embed.set_author(name=f"{emoji.name}", icon_url=emoji.url)
                embed.add_field(name=f"**Animated:**",
                                value=f"{emoji.animated}",
                                inline=True)
                embed.add_field(name=f"**Created at:**",
                                value=f"{str(emoji.created_at)[:str(emoji.created_at).find(' '):]}",
                                inline=True)
                embed.add_field(name=f"**Id:**",
                                value=f"{emoji.id}",
                                inline=False)
                await webhook.send(embed=embed, username='Raven - Emoji updated',
                                   avatar_url=self.bot.user.display_avatar.url)

            # Difference - Added
            diff = list(set(after).difference(before))
            for emoji in diff:
                embed = discord.Embed(title=f"Emoji added",
                                      colour=discord.Colour.green(),
                                      description=f"<:{emoji.name}:{emoji.id}>")
                embed.set_footer(text=f"Guild Id: {guild.id}")
                embed.set_author(name=f"{emoji.name}", icon_url=emoji.url)
                embed.add_field(name=f"**Animated:**",
                                value=f"{emoji.animated}",
                                inline=True)
                embed.add_field(name=f"**Id:**",
                                value=f"{emoji.id}",
                                inline=True)
                await webhook.send(embed=embed, username='Raven - Emoji updated',
                                   avatar_url=self.bot.user.display_avatar.url)

            # Checking for namechanges
            for after_emoji in after:
                for before_emoji in before:
                    if before_emoji.id == after_emoji.id and after_emoji.name != before_emoji.name:
                        embed = discord.Embed(title=f"Emoji renamed",
                                              colour=discord.Colour.yellow(),
                                              description=f"<:{after_emoji.name}:{after_emoji.id}>")
                        embed.set_footer(text=f"Guild Id: {guild.id}")
                        embed.set_author(name=f"{before_emoji.name} -> {after_emoji.name}", icon_url=after_emoji.url)
                        embed.add_field(name=f"**Old name:**",
                                        value=f"```{before_emoji.name}```",
                                        inline=False)
                        embed.add_field(name=f"**New name:**",
                                        value=f"```{after_emoji.name}```",
                                        inline=False)
                        embed.add_field(name=f"**Animated:**",
                                        value=f"{after_emoji.animated}",
                                        inline=True)
                        embed.add_field(name=f"**Id:**",
                                        value=f"{after_emoji.id}",
                                        inline=True)
                        await webhook.send(embed=embed, username='Raven - Emoji updated',
                                           avatar_url=self.bot.user.display_avatar.url)
        return


async def setup(bot):
    sql_connection = sl.connect('Raven.db')
    sql_connection.execute(
        "CREATE TABLE IF NOT EXISTS GUILDS (GUILD_ID int, WEBHOOK_URL str, IS_ACTIVE int, primary key (GUILD_ID))")
    sql_connection.commit()
    sql_connection.close()
    await bot.add_cog(EmojiNStickersLoggingCog(bot))
