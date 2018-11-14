'''
Cog containing general/miscellaneous commands.
'''

import discord
from discord.ext import commands
import random
import inspect
import subprocess
import cogs.utils.key as key
from cogs.utils import checks


class GeneralCog:
    def __init__(self, bot):
        self.bot = bot

    # Returns information on the member
    @commands.command()
    async def userinfo(self, ctx, *, author: discord.Member = None):
        await ctx.channel.trigger_typing()

        if not author:
            author = ctx.author

        msg = discord.Embed(colour=author.color)
        msg.set_author(name=author.name + "#" + str(author.discriminator), icon_url=author.avatar_url)
        msg.set_thumbnail(url=author.avatar_url)
        msg.add_field(name="Nickname", value=author.nick)
        msg.add_field(name="User ID", value=author.id)
        msg.set_footer(text="For help with Gary's commands, use %help.")
        msg.add_field(name="Join Date", value=str(author.joined_at)[:10])
        msg.add_field(name="Account Created", value=str(author.created_at)[:10])
        msg.add_field(name="Status", value=str(author.status).title(), inline=False)
        msg.add_field(name="Roles", value=", ".join(r.name for r in reversed(author.roles)))

        await ctx.send(embed=msg)

    # Rolls a die
    @commands.command()
    async def roll(self, ctx, arg: int = 6):
        await ctx.send(random.randint(1, arg))

    # Flips a coin
    @commands.command()
    async def flip(self, ctx):
        await ctx.send(random.choice(["Heads", "Tails"]))

    # Magic 8-ball
    @commands.command(aliases=['8ball'])
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

    # Returns the given string rewritten using big emojis and logs the user that sent it
    @commands.command()
    async def bigtext(self, ctx, *, args):

        if ctx.guild.id == 342025948113272833:
            channel = self.bot.get_channel(427941608428797954)
        elif ctx.guild.id == 484966083795746816:
            channel = self.bot.get_channel(485964599401644045)


        echo_log = discord.Embed(colour=0x33B5E5)
        echo_log.set_author(name="Gary's Echo Log", icon_url="https://i.neoseeker.com/mgv/297579/579/118/lord_garyVJPHT_display.png")
        echo_log.add_field(name="Author", value=ctx.author.mention, inline=False)
        echo_log.add_field(name="Type", value="Big Text", inline=False)
        echo_log.add_field(name="Message", value=args)
        str = []
        args = args.lower()

        misc = {'0': ":zero:", '1': ":one:",'2': ":two:", '3': ":three:",
                '4': ":four:",'5': ":five:", '6': ":six:", '7': ":seven:",
                '8': ":eight:", '9': ":nine:", ' ': "   ", '*': ":asterisk:",
                '#': ":hash:", '?': ":question:", '!': ":exclamation:"}

        for x in args:
            if (x.isalpha()):
                str.append(":regional_indicator_{}:".format(x.lower()))
            elif x in misc:
                str.append(misc[x])
            else:
                continue

        str = "".join(str)
        await ctx.send(str)

        try:
            await channel.send(embed=echo_log)
        except:
            pass

        await ctx.message.delete()

    # Returns the given string, deletes the message by the author, logs the author and string
    @commands.command()
    async def echo(self, ctx, *, args):
        if ctx.guild.id == 342025948113272833:
            channel = self.bot.get_channel(427941608428797954)
        elif ctx.guild.id == 484966083795746816:
            channel = self.bot.get_channel(485964599401644045)

        echo_log = discord.Embed(colour=0x33B5E5)
        echo_log.set_author(name="Gary's Echo Log", icon_url="https://i.neoseeker.com/mgv/297579/579/118/lord_garyVJPHT_display.png")
        echo_log.add_field(name="Author", value=ctx.author.mention, inline=False)
        echo_log.add_field(name="Type", value="Echo", inline=False)
        echo_log.add_field(name="Message", value=args)

        await ctx.send(args)

        try:
            await channel.send(embed=echo_log)
        except:
            pass

        await ctx.message.delete()

    # Initiates a vote using 👍, 👎, and 🤔, deletes the user's message, then logs it
    @commands.command()
    async def vote(self, ctx, *, args):
        if ctx.guild.id == 342025948113272833:
            channel = self.bot.get_channel(427941608428797954)
        elif ctx.guild.id == 484966083795746816:
            channel = self.bot.get_channel(485964599401644045)

        echo_log = discord.Embed(colour=0x33B5E5)
        echo_log.set_author(name="Gary's Echo Log", icon_url="https://i.neoseeker.com/mgv/297579/579/118/lord_garyVJPHT_display.png")
        echo_log.add_field(name="Author", value=ctx.author.mention, inline=False)
        echo_log.add_field(name="Type", value="Vote", inline=False)
        echo_log.add_field(name="Message", value=args)

        msg = await ctx.send(args)

        try:
            await channel.send(embed=echo_log)
        except:
            pass

        await ctx.message.delete()
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        await msg.add_reaction('🤔')

    # Deletes all of the message in a channel
    @commands.command(hidden=True)
    async def nuke(self, ctx):
        is_mod = False
        for x in ctx.author.roles:
            if (x.name == "Auxiliary"):
                is_mod = True
        if (ctx.channel.name == "the_wall" and is_mod):
            await ctx.channel.purge()

    # Yells at Mary
    @checks.is_trh()
    @commands.command()
    async def clearthepins(self, ctx):
        is_mod = False
        for x in ctx.author.roles:
            if (x.name == "Auxiliary" or x.name == "Sig"):
                is_mod = True
                break
        if (is_mod):
            await ctx.send("<@!147488112770023424> CLEAR THE DAMN PINS")

    # Random emoji
    @commands.command()
    async def feed_tat(self, ctx):
        await ctx.send(str(random.choice(self.bot.emojis)))

    # Banana
    @checks.is_trh()
    @commands.command()
    async def feed_nape(self, ctx):
        await ctx.send(":banana:")

    # Adds/Removes a valid role from the user in TBC
    @commands.command()
    async def role(self, ctx, *args):
        if args[1].lower() not in ['nsfw', 'vc', 'splat', 'spoilers']:
            await ctx.send("This role cannot be added by Gary.")
            return

        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Please only use this command in DMs.")
            return

        guild = self.bot.get_guild(484966083795746816)

        if args[1].lower() == 'vc':
            assigned_role = 'vc losers'
        else:
            assigned_role = args[1].lower()

        for r in guild.roles:
            if r.name.lower() == assigned_role:

                try:
                    user = guild.get_member(ctx.author.id)
                except:
                    await ctx.send("You are not currently in The Bat Cave.")
                    return

                if args[0] == 'add':
                    await user.add_roles(r)
                    await ctx.send("The `{}` role has been added!".format(r.name))

                elif args[0] == 'remove':
                    await user.remove_roles(r)
                    await ctx.send("The `{}` role has been removed!".format(r.name))
                else:
                    await ctx.send("Invalid argument. Only `add` and `remove` may be used.")

    # Returns a randomized string of characters with or without caps
    @commands.command()
    async def mash(self, ctx, *args):
        keys = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c']

        m = []
        lng = random.randint(8,25)

        for _ in range(lng):
            m.append(random.choice(keys))
        
        if args:

            if args[0].lower() == 'caps':
                m = "".join(m).upper()

            elif args[0].lower() == 'random':
                
                for x in range(len(m)):
                    case = random.choice(["m[x].upper()", "m[x].lower()"])
                    m[x] = eval(case)

                m = "".join(m)

            else:
                m = "".join(m)

        else: 
            m = "".join(m)
                
        await ctx.send(m)

    # Shuts down Gary
    @commands.command()
    @checks.is_superuser()
    async def shutdown(self, ctx):
        await ctx.send("Shutting down...")
        await self.bot.logout()

    # Fetches the tail of Gary's log and DMs it to me
    @commands.command()
    @checks.is_superuser()
    async def fetch_log(self, ctx):
        await ctx.author.send("```css\n{}```".format(subprocess.run(['tail', 'gary.log'], stdout=subprocess.PIPE, encoding='utf-8').stdout))


def setup(bot):
    bot.add_cog(GeneralCog(bot))

def teardown(bot):
    bot.remove_cog(GeneralCog(bot))