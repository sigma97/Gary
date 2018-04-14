import discord
from discord.ext import commands

#################################################################
#                                                               #
#                                                               #
#                                                               #
#                                                               #
# This file contains all of the code for generating sprites.    #
#                                                               #
#                                                               #
#                                                               #
#                                                               #
#################################################################


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

ud.usage = "[PokeDex #]"
ud.brief = "Displays the given Pokemon's Mystery Dungeon icon."
ud.help = "Displays the given Pokemon's Mystery Dungeon icon."

@bot.command()
async def rb(ctx, arg):
    arg = arg.lower()
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

rb.usage = "[Pokemon]"
rb.brief = "Displays the given Pokemon's sprite from Red/Blue."
rb.help = "Displays the given Pokemon's sprite from Red/Blue."

@bot.command()
async def yellow(ctx, arg):
    arg = arg.lower()
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

yellow.usage = "[Pokemon]"
yellow.brief = "Displays the given Pokemon's sprite from Yellow."
yellow.help = "Displays the given Pokemon's sprite from Yellow."

@bot.command()
async def silver(ctx, arg):
    arg = arg.lower()
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

silver.usage = "[Pokemon]"
silver.brief = "Displays the given Pokemon's sprite from Silver."
silver.help = "Displays the given Pokemon's sprite from Silver."

@bot.command()
async def gold(ctx, arg):
    arg = arg.lower()
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

gold.usage = "[Pokemon]"
gold.brief = "Displays the given Pokemon's sprite from Gold."
gold.help = "Displays the given Pokemon's sprite from Gold."

@bot.command()
async def crystal(ctx, arg):
    arg = arg.lower()
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

crystal.usage = "[Pokemon]"
crystal.brief = "Displays the given Pokemon's sprite from Crystal."
crystal.help = "Displays the given Pokemon's sprite from Crystal."

@bot.command()
async def rse(ctx, arg):
    arg = arg.lower()
    x = "https://img.pokemondb.net/sprites/ruby-sapphire/normal/" + arg + ".png"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

rse.usage = "[Pokemon]"
rse.brief = "Displays the given Pokemon's sprite from R/S/E."
rse.help = "Displays the given Pokemon's sprite from Ruby/Sapphire/Emerald."

@bot.command()
async def frlg(ctx, arg):
    arg = arg.lower()
    x = "https://img.pokemondb.net/sprites/firered-leafgreen/normal/" + arg + ".png"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

frlg.usage = "[Pokemon]"
frlg.brief = "Displays the given Pokemon's sprite from FR/LG."
frlg.help = "Displays the given Pokemon's sprite from FireRed/LeafGreen."

@bot.command()
async def dppt(ctx, arg):
    arg = arg.lower()
    x = "https://img.pokemondb.net/sprites/diamond-pearl/normal/" + arg + ".png"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

dppt.usage = "[Pokemon]"
dppt.brief = "Displays the given Pokemon's sprite from D/P/Pt."
dppt.help = "Displays the given Pokemon's sprite from Diamond/Pearl/Platinum."

@bot.command()
async def hgss(ctx, arg):
    arg = arg.lower()
    x = "https://img.pokemondb.net/sprites/heartgold-soulsilver/normal/" + arg + ".png"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

hgss.usage = "[Pokemon]"
hgss.brief = "Displays the given Pokemon's sprite from HG/SS."
hgss.help = "Displays the given Pokemon's sprite from HeartGold/SoulSilver."

@bot.command()
async def bw(ctx, arg):
    arg = arg.lower()
    x = "https://img.pokemondb.net/sprites/black-white/anim/normal/" + arg + ".gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)

bw.usage = "[Pokemon]"
bw.brief = "Displays the given Pokemon's sprite from Black/White."
bw.help = "Displays the given Pokemon's sprite from Black/White."

@bot.command()
async def xy(ctx, arg):
    arg = arg.lower()
    if arg in pokemon:
        if (int(pokemon[arg]) > 721):
            await ctx.send("This Pokemon did not exist in X/Y.")
            return
    await xysm(ctx, arg)

xy.usage = "[Pokemon]"
xy.brief = "Displays the given Pokemon's sprite from X/Y."
xy.help = "Displays the given Pokemon's sprite from X/Y."

@bot.command()
async def sm(ctx, arg):
    arg = arg.lower()
    await xysm(ctx, arg)

sm.usage = "[Pokemon]"
sm.brief = "Displays the given Pokemon's sprite from Sun/Moon."
sm.help = "Displays the given Pokemon's sprite from Sun/Moon."

async def xysm(ctx, arg):
    x = "https://play.pokemonshowdown.com/sprites/xyani/" + arg + ".gif"
    y = discord.Embed()
    y.set_image(url=x)
    await ctx.send(embed = y)