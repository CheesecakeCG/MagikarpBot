import discord
from discord.ext import commands
import psutil
import config

bot = commands.Bot(command_prefix=config.prefix, case_insensitive=True)
bot.config = config
VERSION = "0.0.1"

@bot.event
async def on_ready():
    print('Logged in as '+bot.user.name+' (ID: '+str(bot.user.id)+') | '+str(len(bot.guilds))+' servers')
    print('-' * 20)

@bot.event
async def on_message(message):
    if (message.guild is None) or message.author.bot:
        return
    await bot.process_commands(message)

if __name__ == "__main__":
    for extension in bot.config.startup_extensions:
        bot.load_extension(f"Extensions."+extension)
    bot.run(bot.config.token)
