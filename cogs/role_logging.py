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
        # Color
        embed.add_field(name=f"**Color:**", value=f"`{role.color}`", inline=False)

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

        # Color
        embed.add_field(name=f"Color:", value=f"`{role.color}`", inline=False)
        # Permissions
        bool_convert = {
            False: f"❌",
            True: f"✅",
        }
        general_server_perms = [
            "administrator",
            "manage_messages",
            "manage_threads",
            "manage_events",
            "manage_channels",
            "manage_roles",
            "manage_emojis_and_stickers",
            "view_audit_log",
            "view_guild_insights",
            "manage_webhooks",
            "manage_guild",
            "manage_nicknames",
            "kick_members",
            "ban_members",
            "moderate_members",
            "create_instant_invite",
            "change_nickname",
        ]
        text_channel_server_perms = [
            "read_messages",
            "read_message_history",
            "send_messages",
            "send_messages_in_threads",
            "create_private_threads",
            "create_public_threads",
            "embed_links",
            "attach_files",
            "add_reactions",
            "use_external_emojis",
            "use_external_stickers",
            "mention_everyone",
            "send_tts_messages",
            "use_application_commands",
        ]
        voice_server_perms = [
            "connect",
            "speak",
            "stream",
            "use_voice_activation",
            "priority_speaker",
            "mute_members",
            "deafen_members",
            "move_members",
            "request_to_speak",
            "use_embedded_activities",
        ]
        # Admin and General
        perm_description = ""
        for permission_name in general_server_perms:
            before_value = getattr(role.permissions, permission_name)
            perm_description += f"`{permission_name.replace('_', ' ').capitalize()}`: {bool_convert[before_value]}\n"
        embed.add_field(name=f"**Guild permissions:**", value=perm_description, inline=True)
        # Text
        perm_description = ""
        for permission_name in text_channel_server_perms:
            before_value = getattr(role.permissions, permission_name)
            perm_description += f"`{permission_name.replace('_', ' ').capitalize()}`: {bool_convert[before_value]}\n"
        embed.add_field(name=f"**Text-chat permissions:**", value=perm_description, inline=True)
        # Voice
        perm_description = ""
        for permission_name in voice_server_perms:
            before_value = getattr(role.permissions, permission_name)
            perm_description += f"`{permission_name.replace('_', ' ').capitalize()}`: {bool_convert[before_value]}\n"
        embed.add_field(name=f"**Voice-chat permissions:**", value=perm_description, inline=True)

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
        if before.permissions.value == after.permissions.value and before.name == after.name \
                and before.color == after.color:
            return
        # General info
        bool_convert = {
            False: f"❌",
            True: f"✅",
        }
        embed = discord.Embed(title=f"Role was updated",
                              colour=discord.Colour.yellow(),
                              description=f"**{before.name}** (<@&{after.id}>) was updated.")
        if before.name != after.name:
            embed.add_field(name=f"**Role name:**", value=f"`{before.name}` -> `{after.name}`", inline=False)
        if before.color != after.color:
            embed.add_field(name=f"**Color:**", value=f"`{before.color}` -> `{after.color}`", inline=False)

        if before.permissions != after.permissions:
            general_server_perms = [
                "administrator",
                "manage_messages",
                "manage_threads",
                "manage_events",
                "manage_channels",
                "manage_roles",
                "manage_emojis_and_stickers",
                "view_audit_log",
                "view_guild_insights",
                "manage_webhooks",
                "manage_guild",
                "manage_nicknames",
                "kick_members",
                "ban_members",
                "moderate_members",
                "create_instant_invite",
                "change_nickname",
            ]
            text_channel_server_perms = [
                "read_messages",
                "read_message_history",
                "send_messages",
                "send_messages_in_threads",
                "create_private_threads",
                "create_public_threads",
                "embed_links",
                "attach_files",
                "add_reactions",
                "use_external_emojis",
                "use_external_stickers",
                "mention_everyone",
                "send_tts_messages",
                "use_application_commands",
            ]
            voice_server_perms = [
                "connect",
                "speak",
                "stream",
                "use_voice_activation",
                "priority_speaker",
                "mute_members",
                "deafen_members",
                "move_members",
                "request_to_speak",
                "use_embedded_activities",
            ]
            perm_description = ""
            text_description = ""
            voice_description = ""
            for permission_name in general_server_perms:
                before_value = getattr(before.permissions, permission_name)
                after_value = getattr(after.permissions, permission_name)
                if before_value != after_value:
                    perm_description += f"`{permission_name.replace('_', ' ').capitalize()}`: {bool_convert[before_value]} -> {bool_convert[after_value]}\n"

            for permission_name in text_channel_server_perms:
                before_value = getattr(before.permissions, permission_name)
                after_value = getattr(after.permissions, permission_name)
                if before_value != after_value:
                    text_description += f"`{permission_name.replace('_', ' ').capitalize()}`: {bool_convert[before_value]} -> {bool_convert[after_value]}\n"

            for permission_name in voice_server_perms:
                before_value = getattr(before.permissions, permission_name)
                after_value = getattr(after.permissions, permission_name)
                if before_value != after_value:
                    voice_description += f"`{permission_name.replace('_', ' ').capitalize()}`: {bool_convert[before_value]} -> {bool_convert[after_value]}\n"

            if perm_description != "":
                embed.add_field(name=f"**General Permissions:**", value=perm_description, inline=True)
            if text_description != "":
                embed.add_field(name=f"**Text Permissions:**", value=text_description, inline=True)
            if voice_description != "":
                embed.add_field(name=f"**VoicePermissions:**", value=voice_description, inline=True)
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
