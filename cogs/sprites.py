import discord
from discord.ext import commands
from cogs.utils.pokemon import pokemon

class SpriteCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pmd(self, ctx, arg):
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

    @commands.command()
    async def rb(self, ctx, arg):
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

    @commands.command()
    async def yellow(self, ctx, arg):
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

    @commands.command()
    async def silver(self, ctx, arg):
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

    @commands.command()
    async def gold(self, ctx, arg):
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

    @commands.command()
    async def crystal(self, ctx, arg):
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

    @commands.command()
    async def rse(self, ctx, arg):
        arg = arg.lower()
        x = "https://img.pokemondb.net/sprites/ruby-sapphire/normal/" + arg + ".png"
        y = discord.Embed()
        y.set_image(url=x)
        await ctx.send(embed = y)

    @commands.command()
    async def frlg(self, ctx, arg):
        arg = arg.lower()
        x = "https://img.pokemondb.net/sprites/firered-leafgreen/normal/" + arg + ".png"
        y = discord.Embed()
        y.set_image(url=x)
        await ctx.send(embed = y)

    @commands.command()
    async def dppt(self, ctx, arg):
        arg = arg.lower()
        x = "https://img.pokemondb.net/sprites/diamond-pearl/normal/" + arg + ".png"
        y = discord.Embed()
        y.set_image(url=x)
        await ctx.send(embed = y)

    @commands.command()
    async def hgss(self, ctx, arg):
        arg = arg.lower()
        x = "https://img.pokemondb.net/sprites/heartgold-soulsilver/normal/" + arg + ".png"
        y = discord.Embed()
        y.set_image(url=x)
        await ctx.send(embed = y)

    @commands.command()
    async def bw(self, ctx, arg):
        arg = arg.lower()
        x = "https://img.pokemondb.net/sprites/black-white/anim/normal/" + arg + ".gif"
        y = discord.Embed()
        y.set_image(url=x)
        await ctx.send(embed = y)

    @commands.command()
    async def xy(self, ctx, arg):
        arg = arg.lower()
        if arg in pokemon:
            if (int(pokemon[arg]) > 721):
                await ctx.send("This Pokemon did not exist in X/Y.")
                return
        await self._xysm_helper(ctx, arg)

    @commands.command()
    async def sm(self, ctx, arg):
        arg = arg.lower()
        await self._xysm_helper(ctx, arg)

    @staticmethod
    async def _xysm_helper(ctx, arg):
        x = "https://play.pokemonshowdown.com/sprites/xyani/" + arg + ".gif"
        y = discord.Embed()
        y.set_image(url=x)
        await ctx.send(embed = y)

def setup(bot):
    bot.add_cog(SpriteCog(bot))

def teardown(bot):
    bot.remove_cog(SpriteCog(bot))