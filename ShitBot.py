import discord
import asyncio
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
              'cogs.ud',
              'cogs.lewd',
              'cogs.trivia',
              'cogs.lastfm',
              'cogs.imgur',
              'cogs.gameinfo',
              'cogs.help']

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user)
    print('------')
    await bot.change_presence(activity=discord.Game(name='%help'))

@bot.event
async def on_command_error(ctx, error):

    emb = discord.Embed(colour=0x33B5E5)
    emb.set_author(name="Gary Error", icon_url="https://i.neoseeker.com/mgv/297579/579/118/lord_garyVJPHT_display.png")

    if isinstance(error, commands.NoPrivateMessage):
        er = "Server Only"
        st = "This command cannot be used in private messages."
    elif isinstance(error, commands.DisabledCommand):
        er = "Disabled Command"
        st = "This command has been disabled; it cannot currently be used."
    elif isinstance(error, commands.CheckFailure):
        er = "Check Failure"
        st = ("You cannot use this command. Either you lack the "
              "correct permissions or this command is disabled in this channel/server.")
    elif isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        er = "Missing Arguments"
        st = "Your command invocation is missing required arguments."
    else:
        er = "Error"
        st = "`{}`".format(error)

    emb.add_field(name=er, value=st)
    emb.set_footer(text="If you believe you should not be getting this error, ping or DM Sigma#0472.")

    await ctx.send(embed=emb)

@bot.event
async def on_member_join(member):

    role = None

    for r in member.guild.roles:
        if r.id == 408834566950748160:
            role = r
            break
        elif r.id == 484969010266374144:
            role = r
            break

    if role:
        await member.add_roles(role)

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


if __name__ == '__main__':
    for e in extensions:
        bot.load_extension(e)


bot.run(key.key)
