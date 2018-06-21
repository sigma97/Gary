import discord
import cogs.utils.key as key
from discord.ext import commands

client = discord.Client()
bot = commands.Bot(command_prefix='%', pm_help=True)

bot.remove_command("help")

extensions = ['cogs.quotes',
              'cogs.sprites',
              'cogs.users',
              'cogs.general',
              'cogs.interpreter',
              'cogs.markov',
              'cogs.ud',
              'cogs.lewd',
              'cogs.trivia',
              'cogs.lastfm',
              'cogs.imgur']

if __name__ == '__main__':
    for e in extensions:
        bot.load_extension(e)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user)
    print('------')
    await bot.change_presence(activity=discord.Game(name='%help'))

bot.run(key.key)
