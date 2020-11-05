from discord.ext import commands


class GameHelper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(GameHelper(bot))
