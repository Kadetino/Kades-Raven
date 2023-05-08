import aiohttp  # Session for webhook
import discord  # Discord API wrapper
from discord.ext import commands  # Discord BOT
import sqlite3 as sl


class IntegrationLoggingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_integration_create')
    async def integration_created(self, integration: discord.Integration):
        # General info
        embed = discord.Embed(title=f"New {integration.type} integration",
                              colour=discord.Colour.green(),
                              description=f"**`{integration.name}`** was added to the server.")

        # Id info
        embed.set_footer(text=f"Integration Id: {integration.id}")

        # TODO check with Twitch, YT and other integrations?
        # Added by
        try:
            embed.add_field(name=f"**Integration account:**",
                            value=f"<@{integration.account.id}> (Id: {integration.account.id})", inline=False)
        except Exception:
            pass

        # Send Webhook
        sql_connection = sl.connect('Raven.db')
        try:
            hook_url = sql_connection.execute(
                f"SELECT WEBHOOK_URL FROM GUILDS WHERE guild_id = {integration.guild.id}").fetchone()[0]
        except TypeError:
            return sql_connection.close()
        except sl.OperationalError:
            return sql_connection.close()
        sql_connection.close()

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=hook_url, session=session)
            await webhook.send(embed=embed, username='Raven - Integration created',
                               avatar_url=self.bot.user.display_avatar.url)


    @commands.Cog.listener('on_raw_integration_delete')
    async def integration_deleted(self, payload: discord.RawIntegrationDeleteEvent):
        # General info
        embed = discord.Embed(title=f"Integration removed",
                              colour=discord.Colour.red(),
                              description=f"Integration with id `{payload.integration_id}` was removed from the server.")

        # Id info
        embed.set_footer(text=f"Integration Id: {payload.integration_id}")

        # Send Webhook
        sql_connection = sl.connect('Raven.db')
        try:
            hook_url = sql_connection.execute(
                f"SELECT WEBHOOK_URL FROM GUILDS WHERE guild_id = {payload.guild_id}").fetchone()[0]
        except TypeError:
            return sql_connection.close()
        except sl.OperationalError:
            return sql_connection.close()
        sql_connection.close()

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=hook_url, session=session)
            await webhook.send(embed=embed, username='Raven - Integration removed',
                               avatar_url=self.bot.user.display_avatar.url)

    # @commands.Cog.listener('on_guild_integrations_update')
    # async def integration_updated(self, guild: discord.Guild):
    #     pass

    # @commands.Cog.listener('on_webhooks_update')
    # async def webhooks_updated(self, channel):
    #     pass


async def setup(bot):
    sql_connection = sl.connect('Raven.db')
    sql_connection.execute(
        "CREATE TABLE IF NOT EXISTS GUILDS (GUILD_ID int, WEBHOOK_URL str, IS_ACTIVE int, primary key (GUILD_ID))")
    sql_connection.commit()
    sql_connection.close()
    await bot.add_cog(IntegrationLoggingCog(bot))
