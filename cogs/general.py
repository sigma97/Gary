import discord
from discord.ext import commands
import random
import inspect
from cogs.utils import checks


class GeneralCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def userinfo(self, ctx, *args):
        await ctx.channel.trigger_typing()

        author = ctx.author

        if args:
            author = None
            if args[0][0:3] == "<@!":
                author = ctx.guild.get_member(int(args[0][3:len(args[0])-1]))
            elif args[0][0:2] == "<@":
                author = ctx.guild.get_member(int(args[0][2:len(args[0])-1]))
            else:
                args = " ".join(args)
                for m in ctx.guild.members:
                    if args == m.name + "#" + m.discriminator:
                        author = m
                        break
            if author == None:
                await ctx.send("User not found in this server.")
                return

        msg = discord.Embed(colour=author.color)
        msg.set_author(name=author.name, icon_url=author.avatar_url)
        msg.set_thumbnail(url=author.avatar_url)
        msg.add_field(name="User ID", value=author.name + "#" + str(author.discriminator))
        msg.set_footer(text="For help with Gary's commands, use %help.")
        msg.add_field(name="Nickname", value=author.nick)
        msg.add_field(name="Join Date", value=str(author.joined_at)[:10])
        msg.add_field(name="Account Created", value=str(author.created_at)[:10])
        msg.add_field(name="Status", value=str(author.status).title())
        msg.add_field(name="Roles", value=", ".join(r.name for r in reversed(author.roles)))

        await ctx.send(embed=msg)

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
    async def bigtext(self, ctx, *, args):
        if ctx.guild.id == 342025948113272833:
            channel = self.bot.get_channel(427941608428797954)
        elif ctx.guild.id == 484966083795746816:
            channel = self.bot.get_channel(485964599401644045)

        if not args:
            err = "Missing required argument."
            format = "%echo [string]"
            desc = "The %echo command repeats the text inputted by the user.."
            await self._err_catch(ctx, err, format, desc)
            return

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
        await channel.send(embed=echo_log)
        await ctx.message.delete()


    @commands.command()
    async def echo(self, ctx, *, args):
        if ctx.guild.id == 342025948113272833:
            channel = self.bot.get_channel(427941608428797954)
        elif ctx.guild.id == 484966083795746816:
            channel = self.bot.get_channel(485964599401644045)

        if not args:
            err = "Missing required argument."
            format = "%echo [string]"
            desc = "The %echo command repeats the text inputted by the user.."
            await self._err_catch(ctx, err, format, desc)
            return

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

    @commands.command()
    async def eval(self, ctx, *, code : str):
        is_mod = False
        for x in ctx.author.roles:
            if (x.name == "Auxiliary"):
                is_mod = True
                break
        if is_mod or ctx.author.id == 304980605207183370:

            # Credit to Rapptz for the majority of this block of code

            code = code.strip('` ')
            python = '```py\n{}\n```'
            result = None

            env = {
                'bot': self.bot,
                'ctx': ctx,
                'message': ctx.message,
                'guild': ctx.guild,
                'channel': ctx.channel,
                'author': ctx.author
            }

            env.update(globals())

            try:
                result = eval(code, env)
                if inspect.isawaitable(result):
                    result = await result
            except Exception as e:
                 await ctx.send(python.format(type(e).__name__ + ': ' + str(e)))
                 return

            if len(python.format(result)):
                await ctx.send("Output greater than 2000 characters.")
                return
            await ctx.send(python.format(result))

        else:
            await ctx.send("You do not have the correct permissions to use this command.")

    @commands.command()
    async def vote(self, ctx, *, args):
        if ctx.guild.id == 342025948113272833:
            channel = self.bot.get_channel(427941608428797954)
        elif ctx.guild.id == 484966083795746816:
            channel = self.bot.get_channel(485964599401644045)

        if not args:
            err = "Missing required argument."
            format = "%vote [string]"
            desc = "The %vote command initiates a vote using the 👍, 👎, and 🤔 reactions."
            await self._err_catch(ctx, err, format, desc)
            return

        echo_log = discord.Embed(colour=0x33B5E5)
        echo_log.set_author(name="Gary's Echo Log", icon_url="https://i.neoseeker.com/mgv/297579/579/118/lord_garyVJPHT_display.png")
        echo_log.add_field(name="Author", value=ctx.author.mention, inline=False)
        echo_log.add_field(name="Type", value="Vote", inline=False)
        echo_log.add_field(name="Message", value=args)
        msg = await ctx.send(args)
        await channel.send(embed=echo_log)
        await ctx.message.delete()
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        await msg.add_reaction('🤔')

    @commands.command(hidden=True)
    async def nuke(self, ctx):
        is_mod = False
        for x in ctx.author.roles:
            if (x.name == "Auxiliary"):
                is_mod = True
        if (ctx.channel.name == "the_wall" and is_mod):
            await ctx.channel.purge()

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

    @commands.command()
    async def feed_tat(self, ctx):
        await ctx.send(str(random.choice(self.bot.emojis)))

    @checks.is_trh()
    @commands.command()
    async def feed_nape(self, ctx):
        await ctx.send(":banana:")

    @commands.command()
    async def role(self, ctx, *args):
        if args[1].lower() not in ['nsfw']:
            await ctx.send("This role cannot be added by Gary.")
            return

        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Please only use this command in DMs.")
            return

        guild = self.bot.get_guild(484966083795746816)

        if args[0] == 'add':
            for r in guild.roles:
                if r.name.lower() == args[1].lower():

                    try:
                        user = guild.get_member(ctx.author.id)
                    except:
                        await ctx.send("You are not currently in The Bat Cave.")
                        return

                    await user.add_roles(r)
                    await ctx.send("The `{}` role as been added!".format(r.name))
                    return

        elif args[0] == 'remove':
            for r in guild.roles:
                if r.name.lower() == args[1].lower():

                    try:
                        user = guild.get_member(ctx.author.id)
                    except:
                        await ctx.send("You are not currently in The Bat Cave.")
                        return

                    await user.remove_roles(r)
                    await ctx.send("The `{}` role as been removed!".format(r.name))
                    return
        else:
            await ctx.send("The given role does not exist in The Bat Cave.")


def setup(bot):
    bot.add_cog(GeneralCog(bot))

def teardown(bot):
    bot.remove_cog(GeneralCog(bot))