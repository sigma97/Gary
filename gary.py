'''
Gary.py
Written By bshea03 (sigma97)

Started as a test bot for a private discord server but soon became a
multi-purpose bot used to help me develop my Python skills.
'''

import asyncio
import sys
import logging
import traceback
import subprocess
from io import StringIO

import discord
from discord.ext import commands
import config as CONFIG
from cogs.utils import checks

loop = asyncio.get_event_loop()

# Set up logging
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='gary.log', encoding='utf-8', mode='a')
formatter = logging.Formatter("{asctime} - [{levelname}]: {message}", style="{")
handler.setFormatter(formatter)
log.addHandler(handler)

log.info("Bot instance started.")

def log_exc(ctx, error):
    '''Formatting logs'''

    str_io = StringIO()
    if ctx.command:
        print(f"Command '%{ctx.command.qualified_name}':")
        log.error(f"Command '%{ctx.command.qualified_name}':")

    print('{0.__class__.__name__}: {0}'.format(error), file=sys.stderr)
    traceback.print_tb(error.__traceback__, file=sys.stderr)
    traceback.print_tb(error.__traceback__, file=str_io)

    log.exception('{0.__class__.__name__}: {0}'.format(error), exc_info=error)

    # DM me if I created the error
    if ctx.author.id == 304980605207183370:
        if isinstance(error, commands.CommandInvokeError):
            error = error.original
        exc_output = "The last command triggered an exception:\n```py\n{0.__class__.__name__}: {0}\n{1}```".format(
            error, str_io.getvalue() if len(str_io.getvalue()) < 2000 else "")
        ctx.bot.loop.create_task(ctx.message.author.send(exc_output))

# Client instance
client = discord.Client()
bot = commands.Bot(command_prefix=CONFIG.PREFIX, pm_help=True)

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
              'cogs.help',
              'cogs.eval',
              'cogs.wolframalpha',
              'cogs.pfp',
              'cogs.schedule',
              'cogs.confessions']

@bot.event
async def on_ready():
    '''When bot is ready'''
    print('Logged in as')
    print(bot.user)
    print('------')
    await bot.change_presence(activity=discord.Game(name='%help'))

@bot.event
async def on_command_error(ctx, error):
    '''Error handler'''

    emb = discord.Embed(colour=CONFIG.emb_color)
    emb.set_author(name="Gary Error", icon_url=CONFIG.emb_icon)

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
    elif isinstance(error, commands.BadArgument):
        er = "Invalid Argument"
        st = "You used an invalid argument in your command invocation."
    else:
        log_exc(ctx, error)
        return

    emb.add_field(name=er, value=st)
    emb.set_footer(text="If you believe you should not be getting this error, ping or DM Sigma#0472.")

    await ctx.send(embed=emb)

@bot.event
async def on_member_join(member):
    '''Adds designated base role on member join if there is one'''
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

@bot.listen()
async def timer_update(secs):
    '''Timer listener for time-sensitive events'''
    return secs

async def start_timer(bot):
    '''Creates timer using asyncio, dispatches timer_update event to all loaded cogs'''
    await bot.wait_until_ready()

    bot.seconds = 0
    seconds = 0

    # Infinite loop so timer constantly runs
    while True:
        bot.dispatch("timer_update", seconds)
        await timer_update(seconds)
        seconds += 1
        bot.seconds = seconds
        await asyncio.sleep(1)

@bot.command(aliases=['debug'])
@checks.is_superuser()
async def set_debug(ctx):
    '''Sets or unsets DEBUG mode for the logger'''
    if logging.getLogger().getEffectiveLevel() != logging.INFO:
        log.setLevel(logging.DEBUG)
        await ctx.send("Set debug mode.")
    else:
        log.setLevel(logging.INFO)
        await ctx.send("Unset debug mode.")

@bot.command()
@checks.is_superuser()
async def load_cog(ctx, arg):
    '''Loads up a cog'''
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
@checks.is_superuser()
async def unload_cog(ctx, arg):
    '''Unloads a currently loaded cog'''
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

    bot.loop.create_task(start_timer(bot))

    bot.restart_process = False

    bot.run(CONFIG.KEY)

    if bot.restart_process:
        subprocess.call("./restart.sh")
