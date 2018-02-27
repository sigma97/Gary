import discord
from discord.ext import commands
import random
from quote import quotes
from pokemon import pokemon
import psycopg2

client = discord.Client()
bot = commands.Bot(command_prefix='%')
conn = psycopg2.connect(dbname="quotes")
cursor = conn.cursor()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user)
    print('------')
    await bot.change_presence(game=discord.Game(name='%'))

@bot.command()
async def quote(ctx):
    cursor.execute("""SELECT * from quotes""")
    rows = cursor.fetchall()
    x = random.choice(rows)
    await ctx.send('"' + x[1] + '" - ' + x[0])

@bot.command()
async def echo(ctx, *, arg):
    await ctx.send(arg)


## This section contains all of the code for generating sprites.

@bot.command()
async def pmd(ctx, arg):
    if (int(arg) < 1 or int(arg) > 807):
        await ctx.send("Index out of bounds.")
        return
    elif (int(arg) == 721):
        await ctx.send("Volcanion has not appeared in a PMD game.")
        return
    elif (int(arg) > 721 and int(arg) < 808):
        await ctx.send("Gen VII Pokemon have not yet appeared in PMD games.")
        return
    elif (int(arg) < 10):
        arg = "00" + str(arg)
    elif (int(arg) < 100):
        arg = "0" + str(arg)
    x = "https://serebii.net/supermysterydungeon/pokemon/" + arg + ".png"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def rb(ctx, arg):
    x = "https://img.pokemondb.net/sprites/red-blue/normal/" + arg + ".png"
    y = discord.Embed()
    y.set_image(url=x)
    if arg in pokemon:
        if (int(pokemon[arg]) > 151):
            await ctx.send("This Pokemon did not exist in Red/Blue.")
            return
        await ctx.send(embed = y)
    else:
        await ctx.send("Your input is either not a Pokemon or not yet added to the list of Pokemon.")

@bot.command()
async def yellow(ctx, arg):
    x = "https://img.pokemondb.net/sprites/yellow/normal/" + arg + ".png"
    y = discord.Embed()
    y.set_image(url=x)
    if arg in pokemon:
        if (int(pokemon[arg]) > 151):
            await ctx.send("This Pokemon did not exist in Yellow.")
            return
        await ctx.send(embed = y)
    else:
        await ctx.send("Your input is either not a Pokemon or not yet added to the list of Pokemon.")

@bot.command()
async def silver(ctx, arg):
    x = "https://img.pokemondb.net/sprites/silver/normal/" + arg + ".png"
    y = discord.Embed()
    y.set_image(url=x)
    if arg in pokemon:
        if (int(pokemon[arg]) > 251):
            await ctx.send("This Pokemon did not exist in Silver.")
            return
        await ctx.send(embed = y)
    else:
        await ctx.send("Your input is either not a Pokemon or not yet added to the list of Pokemon.")


@bot.command()
async def gold(ctx, arg):
    x = "https://img.pokemondb.net/sprites/gold/normal/" + arg + ".png"
    y = discord.Embed()
    y.set_image(url=x)
    if arg in pokemon:
        if (int(pokemon[arg]) > 251):
            await ctx.send("This Pokemon did not exist in Gold.")
            return
        await ctx.send(embed = y)
    else:
        await ctx.send("Your input is either not a Pokemon or not yet added to the list of Pokemon.")


@bot.command()
async def crystal(ctx, arg):
    x = "https://img.pokemondb.net/sprites/crystal/normal/" + arg + ".png"
    y = discord.Embed()
    y.set_image(url=x)
    if arg in pokemon:
        if (int(pokemon[arg]) > 251):
            await ctx.send("This Pokemon did not exist in Crystal.")
            return
        await ctx.send(embed = y)
    else:
        await ctx.send("Your input is either not a Pokemon or not yet added to the list of Pokemon.")


@bot.command()
async def rse(ctx, arg):
    x = "https://img.pokemondb.net/sprites/ruby-sapphire/normal/" + arg + ".png"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def frlg(ctx, arg):
    x = "https://img.pokemondb.net/sprites/firered-leafgreen/normal/" + arg + ".png"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def dppt(ctx, arg):
    x = "https://img.pokemondb.net/sprites/diamond-pearl/normal/" + arg + ".png"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def hgss(ctx, arg):
    x = "https://img.pokemondb.net/sprites/heartgold-soulsilver/normal/" + arg + ".png"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def bw(ctx, arg):
    x = "https://img.pokemondb.net/sprites/black-white/anim/normal/" + arg + ".gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def xy(ctx, arg):
    if arg in pokemon:
        if (int(pokemon[arg]) > 721):
            await ctx.send("This Pokemon did not exist in X/Y.")
            return
        await xysm(ctx, arg)
    else:
        await ctx.send("Your input is either not a Pokemon or did not exist in X/Y.")

@bot.command()
async def sm(ctx, arg):
    await xysm(ctx, arg)

async def xysm(ctx, arg):
    x = "https://play.pokemonshowdown.com/sprites/xyani/" + arg + ".gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)


# The following section contains commands for each individual user

@bot.command()
async def sig(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/gliscor.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def flames(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/lopunny.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def diamond(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/glaceon.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def odd(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/slowpoke.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def hecc(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/gourgeist.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def fluffy(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/leafeon.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def surv(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/luxray.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def dom(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/charizard.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def psych(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/slaking.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def ama(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/amaura.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def bounty(ctx):
    x = "http://play.pokemonshowdown.com/sprites/xyani-shiny/porygon-z.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def mako(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/primarina.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def timo(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/shaymin-sky.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def cell(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/gengar.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def dragon(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/latios.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def gex(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/treecko.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def tallow(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/zangoose.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def frogger(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/leafeon.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def alaska(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/lurantis.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def minty(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/archen.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def meth(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/mawile.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def hayden(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/infernape.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def nas(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/leafeon.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def nathan(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/goodra.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def zytomic(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/lurantis.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def testin(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/serperior.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def gary(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/gyarados.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def ivee(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/sylveon.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def patrician(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/bronzong.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def drag(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/sylveon.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def curtis(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/reuniclus.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def seymour(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/altaria.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def fooni(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/froslass.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def ace(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/suicune.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def cones(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/vanillite.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

@bot.command()
async def coco(ctx):
    x = "https://play.pokemonshowdown.com/sprites/xyani/plusle.gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

bot.run('NDEwMjM1NjgxMTA2MDM0Njg5.DVqNRA.5hICSESXedjhaue_vwXYu0JqVDY')
