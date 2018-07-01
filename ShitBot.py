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
              'cogs.imgur',
              'cogs.gameinfo',
              'cogs.help']

if __name__ == '__main__':
    for e in extensions:
        bot.load_extension(e)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user)
    print('------')
    await bot.change_presence(activity=discord.Game(name='%help'))

@bot.command()
async def load_cog(ctx, arg):
    if ctx.author.id == 304980605207183370:
        cog = 'cogs.' + arg
        if cog in extensions:
            bot.load_extension(cog)
            await ctx.send("Cog successfully loaded.")
        else:
            await ctx.send("The cog `" + arg + "` does not exist.")
    else:
        await ctx.send("You do not have the correct permissions to use this command.")

@bot.command()
async def unload_cog(ctx, arg):
    if ctx.author.id == 304980605207183370:
        cog = 'cogs.' + arg
        if cog in extensions:
            bot.unload_extension(cog)
            await ctx.send("Cog successfully unloaded.")
        else:
            await ctx.send("The cog `" + arg + "` does not exist.")
    else:
        await ctx.send("You do not have the correct permissions to use this command.")


bot.run(key.key)
