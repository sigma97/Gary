'''
Cog containing general/miscellaneous commands.
'''

import random
import subprocess
import inspect
import asyncio
from PIL import Image
import discord
from discord.ext import commands
import requests
import config
from cogs.utils import checks
from cogs.utils import converters

class ServerPermission(discord.DiscordException):
    '''Exception for use when user is not in a server'''

client = discord.Client()

class GeneralCog(commands.Cog):
    '''General commands for Gary'''

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    @client.event
    async def on_member_join(member):
        if member.guild.id != 484966083795746816:
            return
        
        channel = member.guild.get_channel(484966083795746819)
        rules = member.guild.get_channel(489271737788268584)
        server_feedback = member.guild.get_channel(484980453632114688)

        await channel.send(f'Welcome to the Bat Cave, {member.mention}! All self-assignable roles are listed in {rules.mention} and if you\'d like a custom role, you can request one by leaving a name and color in {server_feedback.mention}.')

    @commands.command()
    async def userinfo(self, ctx, *, author: discord.Member = None):
        '''Collects info on given member'''
        await ctx.channel.trigger_typing()

        if not author:
            author = ctx.author

        msg = discord.Embed(colour=author.color)
        msg.set_author(name=author.name + "#" + str(author.discriminator), \
        icon_url=author.avatar_url)
        msg.set_thumbnail(url=author.avatar_url)
        msg.add_field(name="Nickname", value=author.nick)
        msg.add_field(name="User ID", value=author.id)
        msg.set_footer(text="For help with Gary's commands, use %help.")
        msg.add_field(name="Join Date", value=str(author.joined_at)[:10])
        msg.add_field(name="Account Created", value=str(author.created_at)[:10])
        msg.add_field(name="Status", value=str(author.status).title(), inline=False)
        msg.add_field(name="Roles", value=", ".join(r.name for r in reversed(author.roles)))

        await ctx.send(embed=msg)

    @commands.command()
    async def info(self, ctx, *, item: converters.UnspecifiedConverter = None):
        '''Get information on something.'''
        if item is None:
            raise Exception("You did not specify an item")

        if isinstance(item, discord.Guild):
            embed = discord.Embed()
            embed.set_author(name=f"Information for {item.name}")
            embed.set_thumbnail(url=item.icon_url)

            embed.add_field(name="Guild ID", value=item.id)
            embed.add_field(name="Voice Region", value=item.region)
            embed.add_field(name="Member Count", value=item.member_count)

            embed.add_field(name="Created At", value=item.created_at)
            embed.add_field(name="Owner",
                            value=f"{item.owner.mention}")

        elif isinstance(item, discord.Role):
            embed = discord.Embed(colour=item.colour)
            embed.set_author(name=f"Information for {item.name} role")
            embed.add_field(name="Role ID", value=item.id)
            embed.add_field(name="Guild", value=item.guild)

            embed.add_field(name="Permissions",
                            value=f"[Permissions list](https://discordapi.com/permissions.html#{item.permissions.value})")

            embed.add_field(name="Is Mentionable", value=item.mentionable)
            embed.add_field(name="Created At", value=item.created_at)
            members = ", ".join([m.name for m in item.members])
            if len(item.members) < 10:
                embed.add_field(name="Members", value=(
                    (members[:1020] + '...') if len(members) > 1024 else members) or None, inline=False)
            else:
                embed.add_field(name="Members", value=len(
                    item.members), inline=False)

        elif isinstance(item, discord.CategoryChannel):
            embed = discord.Embed()
            embed.set_author(name=f"Information for #{item.name}")

            embed.add_field(name="Category ID", value=item.id)
            embed.add_field(name="Guild", value=item.guild)
            embed.add_field(name="Created At", value=item.created_at)

            embed.add_field(name="Is NSFW", value=item.is_nsfw())

            channels = ", ".join([c.name for c in item.channels])
            embed.add_field(name="Channels", value=(
                (channels[:1020] + '...') if len(channels) > 1024 else channels) or None, inline=False)

        elif isinstance(item, discord.TextChannel):
            embed = discord.Embed()
            embed.set_author(name=f"Information for #{item.name}")

            embed.add_field(name="Channel ID", value=item.id)
            embed.add_field(name="Guild", value=item.guild)
            embed.add_field(name="Created At", value=item.created_at)
            if item.category:
                embed.add_field(name="Category", value=item.category)

            embed.add_field(name="Channel Topic", value=item.topic)
            embed.add_field(name="Is NSFW", value=item.is_nsfw())

        elif isinstance(item, discord.VoiceChannel):
            embed = discord.Embed()
            embed.set_author(name=f"Information for {item.name}")

            embed.add_field(name="Channel ID", value=item.id)
            embed.add_field(name="Guild", value=item.guild)
            embed.add_field(name="Created At", value=item.created_at)
            if item.category:
                embed.add_field(name="Category", value=item.category)

            embed.add_field(name="User Limit", value=item.user_limit)
            embed.add_field(name="Members", value=", ".join(
                [m.name for m in item.members]) or "None", inline=False)

        elif isinstance(item, discord.User) or isinstance(item, discord.Member):
            if isinstance(item, discord.Member):
                colour = item.colour
            else:
                colour = discord.Colour.default()

            embed = discord.Embed(colour=colour)
            embed.set_author(name=f"Information for {item.name}")
            embed.set_thumbnail(url=item.avatar_url)

            embed.add_field(name="Mention String",
                            value=f"{item.name}#{item.discriminator}")
            embed.add_field(name="User ID", value=item.id)
            embed.add_field(name="Account Created", value=item.created_at)

            avatar_str = f"[Link]({item.avatar_url}) | [Google Image Search](https://www.googlembed.com/searchbyimage?&image_url={item.avatar_url})"
            embed.add_field(name="Avatar:", value=avatar_str)

            if isinstance(item, discord.Member):
                embed.add_field(name="Nickname", value=item.nick)
                embed.add_field(name="Joined Server", value=item.joined_at)
                embed.add_field(name="Roles", value=", ".join(
                    [str(r) for r in item.roles[1:]]) or "None", inline=False)

        elif isinstance(item, discord.Colour):
            embed = discord.Embed(colour=item)
            embed.set_author(name=f"Information on {hex(item.value)}")
            embed.add_field(name="RGB", value=f"{item.r}, {item.g}, {item.b}")
            embed.add_field(name="Int", value=item.value)
            embed.add_field(name="Hex", value=str(item))

            for name, command in inspect.getmembers(discord.Colour, predicate=inspect.ismethod):
                if command.__self__ is discord.Colour and command not in [discord.Colour.from_rgb, discord.Colour.from_hsv] and command() == item:
                    embed.add_field(name="Class Method", value=name)

            embed.set_thumbnail(
                url="attachment://{:0>6x}.png".format(item.value))

            # Generate the attachment
            image_dimensions = 80
            im = Image.new("RGB", (image_dimensions, image_dimensions))
            im.paste((item.r, item.g, item.b), [
                     0, 0, image_dimensions, image_dimensions])
            im.save("temp_colour.png", "PNG")

            await ctx.send(embed=embed, file=discord.File("temp_colour.png", "{:0>6x}.png".format(item.value)))
            return

        await ctx.send(embed=embed)


    @commands.command()
    async def roll(self, ctx, arg: int = 6):
        '''Rolls a die'''
        await ctx.send(random.randint(1, arg))

    @commands.command()
    async def flip(self, ctx):
        '''Flips a coin'''
        await ctx.send(random.choice(["Heads", "Tails"]))

    @commands.command(aliases=['8ball'])
    async def oracle(self, ctx):
        '''Magic 8-ball'''

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
        '''Returns the given string rewritten using big emojis and logs the user that sent it'''

        if ctx.guild.id == 342025948113272833:
            channel = self.bot.get_channel(427941608428797954)
        elif ctx.guild.id == 484966083795746816:
            channel = self.bot.get_channel(485964599401644045)
        elif ctx.guild.id == 557283224330436621:
            channel = self.bot.get_channel(558098383039102976)


        echo_log = discord.Embed(colour=config.emb_color)
        echo_log.set_author(name="Gary's Echo Log", icon_url=config.emb_icon)
        echo_log.add_field(name="Author", value=ctx.author.mention, inline=False)
        echo_log.add_field(name="Type", value="Big Text", inline=False)
        echo_log.add_field(name="Message", value=args)
        strng = []
        args = args.lower()

        misc = {'0': ":zero:", '1': ":one:", '2': ":two:", '3': ":three:",
                '4': ":four:", '5': ":five:", '6': ":six:", '7': ":seven:",
                '8': ":eight:", '9': ":nine:", ' ': "   ", '*': ":asterisk:",
                '#': ":hash:", '?': ":question:", '!': ":exclamation:"}

        for char in args:
            if char.isalpha():
                strng.append(":regional_indicator_{}:".format(char.lower()))
            elif char in misc:
                strng.append(misc[char])
            else:
                continue

        strng = "".join(strng)
        await ctx.send(strng)

        try:
            await channel.send(embed=echo_log)
        except discord.DiscordException:
            pass

        await ctx.message.delete()

    @commands.command()
    async def echo(self, ctx, *, args):
        '''Returns the string, deletes the message by the author, logs the author and string'''

        if ctx.guild.id == 342025948113272833:
            channel = self.bot.get_channel(427941608428797954)
        elif ctx.guild.id == 484966083795746816:
            channel = self.bot.get_channel(485964599401644045)
        elif ctx.guild.id == 557283224330436621:
            channel = self.bot.get_channel(558098383039102976)

        echo_log = discord.Embed(colour=config.emb_color)
        echo_log.set_author(name="Gary's Echo Log", icon_url=config.emb_icon)
        echo_log.add_field(name="Author", value=ctx.author.mention, inline=False)
        echo_log.add_field(name="Type", value="Echo", inline=False)
        echo_log.add_field(name="Message", value=args)

        await ctx.send(args)

        try:
            await channel.send(embed=echo_log)
        except discord.DiscordException:
            pass

        await ctx.message.delete()

    @commands.command()
    async def vote(self, ctx, *, args):
        '''Initiates a vote using 👍, 👎, and 🤔, deletes the user's message, then logs it'''

        if ctx.guild.id == 342025948113272833:
            channel = self.bot.get_channel(427941608428797954)
        elif ctx.guild.id == 484966083795746816:
            channel = self.bot.get_channel(485964599401644045)
        elif ctx.guild.id == 557283224330436621:
            channel = self.bot.get_channel(558098383039102976)

        echo_log = discord.Embed(colour=config.emb_color)
        echo_log.set_author(name="Gary's Echo Log", icon_url=config.emb_icon)
        echo_log.add_field(name="Author", value=ctx.author.mention, inline=False)
        echo_log.add_field(name="Type", value="Vote", inline=False)
        echo_log.add_field(name="Message", value=args)

        msg = await ctx.send(args)

        try:
            await channel.send(embed=echo_log)
        except discord.DiscordException:
            pass

        await ctx.message.delete()
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        await msg.add_reaction('🤔')

    @commands.command()
    async def clap(self, ctx, *, args):
        '''Returns the string, deletes the message by the author, logs the author and string'''

        if ctx.guild.id == 342025948113272833:
            channel = self.bot.get_channel(427941608428797954)
        elif ctx.guild.id == 484966083795746816:
            channel = self.bot.get_channel(485964599401644045)
        elif ctx.guild.id == 557283224330436621:
            channel = self.bot.get_channel(558098383039102976)

        echo_log = discord.Embed(colour=config.emb_color)
        echo_log.set_author(name="Gary's Echo Log", icon_url=config.emb_icon)
        echo_log.add_field(name="Author", value=ctx.author.mention, inline=False)
        echo_log.add_field(name="Type", value="Clap", inline=False)
        echo_log.add_field(name="Message", value=args)

        msg = " :clap: ".join(args.split(" "))

        msg = ":clap: " + msg + " :clap:"

        await ctx.message.delete()
        await ctx.send(msg)
        await channel.send(embed=echo_log)

    @commands.command(hidden=True, enabled=False)
    async def nuke(self, ctx):
        '''Deletes all of the message in a channel'''
        # TODO: Rewrite using checks
        is_mod = False
        for role in ctx.author.roles:
            if role.name == "Auxiliary":
                is_mod = True
        if (ctx.channel.name == "the_wall" and is_mod):
            await ctx.channel.purge()

    @checks.is_trh()
    @commands.command(enabled=False)
    async def clearthepins(self, ctx):
        '''Yells at Hecc'''
        # TODO: Rewrite using checks

        is_mod = False
        for role in ctx.author.roles:
            if (role.name == "Auxiliary" or role.name == "Sig"):
                is_mod = True
                break
        if is_mod:
            await ctx.send("<@!147488112770023424> CLEAR THE DAMN PINS")

    @commands.command()
    async def feed_tat(self, ctx):
        '''Random emoji'''
        await ctx.send(str(random.choice(self.bot.emojis)))

    @checks.is_trh()
    @commands.command()
    async def feed_nape(self, ctx):
        '''Banana'''
        await ctx.send(":banana:")

    @commands.command()
    async def cat(self, ctx):
        '''Random cat picture'''
        res = requests.get('http://aws.random.cat/meow')

        await ctx.send(res.json()['file'].replace("\\", ""))

    @commands.command()
    async def randfox(self, ctx):
        '''Random fox picture'''
        res = requests.get('https://randomfox.ca/floof/')

        await ctx.send(res.json()['image'].replace("\\", ""))

    @commands.command()
    async def role(self, ctx, *args):
        '''Adds/Removes a valid role from the user in TBC'''
        roles = ['nsfw', 'vc', 'splat', 'spoilers', 'kindalewd', 'smash']

        if not args:
            await ctx.send(f"Please use one of the following " \
                           f"arguments with this command: " \
                           f"`{'`, `'.join(roles)}`.")
            return

        if args[1].lower() not in roles:
            await ctx.send("This role cannot be added by Gary.")
            return

        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Please only use this command in DMs.")
            return

        guild = self.bot.get_guild(484966083795746816)

        if args[1].lower() == 'vc':
            assigned_role = 'vc losers'
        elif args[1].lower() == 'kindalewd':
            assigned_role = 'kinda lewd'
        else:
            assigned_role = args[1].lower()

        for role in guild.roles:
            if role.name.lower() == assigned_role:

                try:
                    user = guild.get_member(ctx.author.id)
                except ServerPermission:
                    await ctx.send("You are not currently in The Bat Cave.")
                    return

                if args[0] == 'add':

                    if assigned_role in ['kinda lewd', 'nsfw']:
                        msg = await ctx.send("This is an 18+ role. By adding this role, you agree to being 18 or older. If you are caught lying about this, you will be subject to a kick or ban from this server. Do you wish to continue?")
                        await msg.add_reaction("✅")
                        await msg.add_reaction("❎")

                        def check(reaction, user):
                            return user == ctx.message.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❎')

                        try:
                            reaction, _ = await self.bot.wait_for('reaction_add', timeout=20.0, check=check)
                        except asyncio.TimeoutError:
                            await ctx.send('Request timed out.')
                            return
                        else:
                            if str(reaction.emoji) == '✅':
                                await user.add_roles(role)
                                await ctx.send("The `{}` role has been added!".format(role.name))
                            elif str(reaction.emoji) == '❎':
                                await ctx.send("Request cancelled.")

                elif args[0] == 'remove':
                    await user.remove_roles(role)
                    await ctx.send("The `{}` role has been removed!".format(role.name))
                else:
                    await ctx.send("Invalid argument. Only `add` and `remove` may be used.")

    @commands.command()
    async def mash(self, ctx, *args):
        '''Returns a randomized string of characters with or without caps'''

        keys = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c']

        msg = []
        lng = random.randint(8, 25)

        for _ in range(lng):
            msg.append(random.choice(keys))

        if args:

            if args[0].lower() == 'caps':
                msg = "".join(msg).upper()

            elif args[0].lower() == 'random':

                for char in enumerate(msg):
                    case = random.choice(["msg[char].upper()", "msg[char].lower()"])
                    msg[char] = eval(case)

                msg = "".join(msg)

            else:
                msg = "".join(msg)

        else:
            msg = "".join(msg)

        await ctx.send(msg)

    @commands.command(aliases=['kill'])
    @checks.is_superuser()
    async def shutdown(self, ctx):
        '''Shuts down Gary'''

        await ctx.send("Shutting down...")
        await self.bot.logout()

    @commands.command()
    @checks.is_superuser()
    async def restart(self, ctx):
        '''Restarts Gary'''

        await ctx.send("Restarting...")
        self.bot.restart_process = True
        await self.bot.logout()

    @commands.command()
    @checks.is_superuser()
    async def fetch_log(self, ctx):
        '''Fetches the tail of Gary's log and DMs it to me'''

        await ctx.author.send("```css\n{}```".format(subprocess.run(['tail', 'gary.log'], \
            stdout=subprocess.PIPE, encoding='utf-8').stdout))


def setup(bot):
    '''Adds cog to Gary'''
    bot.add_cog(GeneralCog(bot))


def teardown(bot):
    '''Removes cog from Gary'''
    bot.remove_cog(GeneralCog(bot))
