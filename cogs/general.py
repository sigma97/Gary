import discord
from discord.ext import commands
import random


class GeneralCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, *args):
        channel = ctx.message.author.dm_channel
        if (channel == None):
            channel = await ctx.message.author.create_dm()
        await channel.trigger_typing()

        gen = """ `%help`\n Displays this message!\n
`%quote [id (optional)]`\n Displays the quote with the specified ID. If none is given, a random quote is returned.\n
`%echo [string]`\n Repeats the text inputted by the user.\n
`%vote`\n Initiates a vote using the 👍, 👎, and 🤔 reactions.\n
`%roll [# sides (optional)]`\n Displays a random number in the given range (six by default).\n
`%flip`\n Returns "Heads" or "Tails" at random.\n
`%oracle`\n Magic 8-Ball.\n
`%ud [word or phrase (optional)]`\n Returns Urban Dictionary definition of supplied word. If no word is supplied, returns a random word and definition.\n
`%e621 [query]`\n Returns the top e621 image of the given query. Can only be used in #bot_spam (SFW) and #nsfw_pics (NSFW).\n\u200b"""

        db = """ `%add [user] [quote]`\n Auxiliary only. Adds a new quote to Gary's list.\n
`%delete [id]`\n Auxiliary only. Deletes a quote from Gary's list.\n
`%ids`\n DMs the user a list of quotes and their IDs.\n\u200b"""

        sprites = """`%pmd [pokedex #]`\n Displays the PMD icon of the given Pokemon.\n
`%[pokemon game] [pokemon]`\n Displays the sprite of the given pokemon from the specified game. Valid commands are:
`%rb`, `%yellow`, `%gold`, `%silver`, `%crystal`, `%rse`, `%frlg`, `%dppt`, `%hgss`, `%bw`, `%xy`, `%sm`.\n\u200b"""

        users = """`%[user]`\n Displays the pokemon commonly associated with the specified user.
If your name does not yet have a command, DM Sigma with the pokemon you want.\n\u200b"""

        msg = discord.Embed(description="The following is a list of commands that can be used with Gary.", colour=0x33B5E5)
        msg.set_footer(text="For any additional inquiries, please DM Sigma#0472.")
        msg.set_author(name="Gary Help Menu", icon_url="https://i.neoseeker.com/mgv/297579/579/118/lord_garyVJPHT_display.png")
        msg.add_field(name="General Commands", value=gen, inline=False)
        msg.add_field(name="Admin Commands", value=db, inline=False)
        msg.add_field(name="Sprite Commands", value=sprites, inline=False)
        msg.add_field(name="User Commands", value=users, inline=False)
        await channel.send(embed = msg)

    @staticmethod
    async def _err_catch(ctx, err, format, desc):
        channel = ctx.message.author.dm_channel
        if channel == None:
            channel = await ctx.message.author.create_dm()
        x = discord.Embed(colour=0x33B5E5, title=err, description='`' + format + '`\n')
        x.add_field(name=desc, value="\u200b")
        x.set_author(name="Gary Command Error", icon_url="https://i.neoseeker.com/mgv/297579/579/118/lord_garyVJPHT_display.png")
        x.set_footer(text="Please use %help or DM Sigma#0472 with any further questions.")
        await channel.send(embed = x)

    @commands.command()
    async def roll(self, ctx, *args):
        if (len(args) == 0):
            await ctx.send(random.randint(1,6))
        else:
            try:
                await ctx.send(random.randint(1,int(args[0])))
            except ValueError:
                err = "Invalid argument type."
                format = "%roll [# sides (optional)]"
                desc = "The %roll command displays a random number in the given range (six by default)."
                await self._err_catch(ctx, err, format, desc)

    @commands.command()
    async def flip(self, ctx):
        await ctx.send(random.choice(["Heads", "Tails"]))

    @commands.command()
    async def oracle(self, ctx):
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes, definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful"]
        await ctx.send(random.choice(responses))

    @commands.command()
    async def echo(self, ctx, *args):
        channel = self.bot.get_channel(427941608428797954)
        arg = " ".join(args)
        echo_log = "**" + ctx.author.name + ":** " + arg
        try:
            await ctx.send(arg)
            await channel.send(echo_log)
            await ctx.message.delete()
        except discord.errors.HTTPException:
            err = "Missing required argument."
            format = "%echo [string]"
            desc = "The %echo command repeats the text inputted by the user.."
            await self._err_catch(ctx, err, format, desc)

    @commands.command()
    async def vote(self, ctx, *args):
        channel = self.bot.get_channel(427941608428797954)
        arg = " ".join(args)
        echo_log = "**" + ctx.author.name + ":** " + arg
        try:
            msg = await ctx.send(arg)
            await channel.send(echo_log)
            await ctx.message.delete()
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')
            await msg.add_reaction('🤔')
        except discord.errors.HTTPException:
            err = "Missing required argument."
            format = "%vote [string]"
            desc = "The %vote command initiates a vote using the 👍, 👎, and 🤔 reactions."
            await self._err_catch(ctx, err, format, desc)

    @commands.command(hidden=True)
    async def nuke(self, ctx):
        is_mod = False
        for x in ctx.author.roles:
            if (x.name == "Auxiliary"):
                is_mod = True
        if (ctx.channel.name == "the_wall" and is_mod):
            await ctx.channel.purge();


def setup(bot):
    bot.add_cog(GeneralCog(bot))
