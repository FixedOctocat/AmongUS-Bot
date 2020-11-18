from discord.ext import commands
from config import TOKEN, BOT_PREFIX

bot = commands.Bot(command_prefix=BOT_PREFIX)
bot.remove_command('help')


@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name)
    bot.load_extension("cogs.Admin")
    bot.load_extension("cogs.GameHelper")
    bot.load_extension("cogs.MusicPlayer")

bot.run(TOKEN)
