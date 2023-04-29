import discord  # Discord API wrapper
from discord import app_commands  # Slash commands
from discord.ext import commands  # Discord BOT
import aiohttp  # For direct API requests and webhooks
import warnings  # For direct API requests and webhooks
import logging

from config import token, prefix, application_id, owners  # Global settings


# noinspection PyMethodMayBeStatic
class RavenBot(commands.Bot):
    def __init__(self):
        # Logging
        logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                            level=logging.DEBUG,
                            filename='RavenBot.log',
                            encoding='utf-8', )
        logger = logging.getLogger(__name__)
        logging.info(f'Bot launched')

        # Intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.emojis_and_stickers = True
        intents.invites = True

        # Constructor
        super().__init__(command_prefix=prefix,
                         intents=intents,
                         application_id=application_id,
                         owner_ids=set(owners))
        # Aiohttp
        self.session = aiohttp.ClientSession()

        # Cogs
        self.initial_extensions = [
            "cogs.misc",
            "cogs.logging_setup",
            "cogs.message_logging",
            "cogs.role_logging",
            "cogs.channel_logging",
            "cogs.thread_logging",
            "cogs.member_logging",
            "cogs.invite_logging"
        ]

        @self.tree.error
        async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
            """Error handler"""
            logging.error(str(error))
            return await interaction.response.send_message("Unknown error. It was reported.", ephemeral=True)

    async def setup_hook(self):
        # Cogs
        for ext in self.initial_extensions:
            await self.load_extension(ext)

        # Slash commands - Goose refuge
        self.tree.copy_global_to(guild=discord.Object(id=950688544433778689))
        await self.tree.sync(guild=discord.Object(id=950688544433778689))
        # # Slash commands
        # self.tree.copy_global_to(guild=discord.Object(id=664124313997148170))
        # await self.tree.sync(guild=discord.Object(id=664124313997148170))

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_ready(self):
        print('Logged on as {0.user}!'.format(bot))
        logging.info('Logged on as {0.user}!'.format(bot))


warnings.filterwarnings("ignore", category=DeprecationWarning)
bot = RavenBot()
bot.remove_command('help')

bot.run(token)
