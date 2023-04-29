from discord.ext import commands  # Discord BOT


class utilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx: commands.Context):
        await self.bot.session.close()
        return await ctx.bot.close()


async def setup(bot):
    await bot.add_cog(utilityCog(bot))
