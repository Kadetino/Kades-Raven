import discord
from discord import app_commands
from discord.ext import commands
import sqlite3 as sl


class SetupModal(discord.ui.Modal, title="Setup Logging"):
    category_name = discord.ui.TextInput(
        label="Category Name",
        placeholder="Ravens-corner",
        default="Ravens-corner",
    )

    channel_prefix = discord.ui.TextInput(
        label="Channel Prefix",
        placeholder="logs",
        default="logs",
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)

        guild = interaction.guild
        if guild is None:
            return await interaction.followup.send("This command can only be used in a server.")

        prefix = (self.channel_prefix.value or "").strip().lower().replace(" ", "-")
        category_name = (self.category_name.value or "").strip() or "Ravens-corner"

        try:
            corner = await guild.create_category(name=category_name)
            await corner.set_permissions(
                guild.default_role,
                read_messages=False,
                send_messages=False,
                connect=False,
            )

            async def make_channel(name: str) -> str:
                ch = await corner.create_text_channel(name=f"{prefix}-{name}")
                webhook = await ch.create_webhook(name="Raven-logging")
                return webhook.url

            channels_url = await make_channel("channels")
            messages_url = await make_channel("messages")
            roles_url = await make_channel("roles")
            members_url = await make_channel("members")
            guild_url = await make_channel("guild")

            threads_channel = await corner.create_text_channel(name=f"{prefix}-threads")
            threads_url = (await threads_channel.create_webhook(name="Raven-logging")).url

            conn = sl.connect("Raven.db")
            try:
                conn.execute(
                    "INSERT OR IGNORE INTO CHANNELS VALUES (?,?,?)",
                    (guild.id, channels_url, 1),
                )
                conn.execute(
                    "INSERT OR IGNORE INTO MESSAGES VALUES (?,?,?)",
                    (guild.id, messages_url, 1),
                )
                conn.execute(
                    "INSERT OR IGNORE INTO ROLES VALUES (?,?,?)",
                    (guild.id, roles_url, 1),
                )
                conn.execute(
                    "INSERT OR IGNORE INTO THREADS VALUES (?,?,?)",
                    (guild.id, threads_url, 1),
                )
                conn.execute(
                    "INSERT OR IGNORE INTO MEMBERS VALUES (?,?,?)",
                    (guild.id, members_url, 1),
                )
                conn.execute(
                    "INSERT OR IGNORE INTO GUILDS VALUES (?,?,?)",
                    (guild.id, guild_url, 1),
                )
                conn.commit()
            finally:
                conn.close()

        except discord.Forbidden:
            return await interaction.followup.send(
                "Missing permissions to create categories/channels/webhooks. "
                "Grant Manage Channels + Manage Webhooks and try again."
            )
        except discord.HTTPException as e:
            return await interaction.followup.send(f"Setup failed: {e}")
        except sl.Error as e:
            return await interaction.followup.send(f"Database error: {e}")

        await interaction.followup.send("Logging setup complete.")


class SetupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup", description="Setup logging system")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction):
        await interaction.response.send_modal(SetupModal())


async def setup(bot):
    await bot.add_cog(SetupCog(bot))
