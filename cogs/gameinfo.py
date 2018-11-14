'''
Stores various game information on each user such as PSN IDs, XBL Gamertags,
Friend Codes, etc.
'''

import discord
from discord.ext import commands
import psycopg2
import re

# Initialize database
conn = psycopg2.connect(dbname="quotes")
cursor = conn.cursor()

class GameInfoCog:
    def __init__(self, bot):
        self.bot = bot
        self.platforms = {"psn": "psn_id",
                          "xblive": "gamertag",
                          "steam": "steam_acc",
                          "switch": "switch_fc",
                          "3ds": "ds_fc"}
        self.db_list = {"PSN ID": "psn",
                        "Xbox Live Gamertag": "xblive",
                        "Steam Account": "steam",
                        "Switch Friend Code": "switch",
                        "3DS Friend Code": "3ds"}
        # reverse of above
        self.rev_dblist = {y: x for x, y in self.db_list.items()}

    # Gameinfo not found in the database
    async def _notfound(self, ctx, emb, *arg):
        if not arg:
            emb.add_field(name="No Game Info Found.", value="To set gameinfo, use `%set [platform] [arg]`, " +
"where platform is one of the following: `psn`, `xblive`, `steam`, `switch`, `3ds`.")
        else:
            emb.add_field(name="No " + arg[0] + " Found.", value="To set one, use `%set " + self.db_list[arg[0]] + " [arg]`.")
            emb.set_footer(text="For help with game info commands, use %help gameinfo.")
        await ctx.send(embed=emb)
        

    # Gets all of the user's gameinfo
    @commands.command()
    async def gameinfo(self, ctx):
        emb = discord.Embed(colour=ctx.author.colour) 
        emb.set_author(name="Game Info for " + ctx.author.name + "#" + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
        emb.set_footer(text="For help with game info commands, use %help gameinfo.")
        keys = ["PSN ID", "Xbox Live Gamertag", "Steam Account", "Switch Friend Code", "3DS Friend Code"]
        cursor.execute("SELECT * FROM game_info WHERE member={};".format("'" + str(ctx.author.id) + "'"))
        rows = cursor.fetchall()
        if not rows:
            await self._notfound(ctx, emb)
            return
        row = rows[0]
        for i in range(len(keys)):
            if row[i+1]:
                emb.add_field(name=keys[i], value=row[i+1])
        await ctx.send(embed=emb)


    # Gets the gameinfo for a specific platform
    @commands.command()
    async def get(self, ctx, arg):
        emb = discord.Embed(colour=ctx.author.colour) 
        emb.set_author(name="Game Info for " + ctx.author.name + "#" + ctx.author.discriminator, icon_url=ctx.author.avatar_url)

        keys = list(self.db_list.keys())
        cursor.execute("SELECT * FROM game_info WHERE member={};".format("'" + str(ctx.author.id) + "'"))
        rows = cursor.fetchall()

        if not rows:
            await self._notfound(ctx, emb)
            return

        if arg in self.platforms.keys():
            for i in range(len(keys)):
                if self.db_list[keys[i]] == arg:
                    cursor.execute("SELECT " + self.platforms[arg] +" FROM game_info WHERE member={};".format("'" + str(ctx.author.id) + "'"))
                    row = cursor.fetchall()
                    if not row[0][0]:
                        await self._notfound(ctx, emb, keys[i])
                        return
                    emb.add_field(name=keys[i], value=row[0][0])
        else:
            emb.add_field(name="Invalid Platform", value="Please use a platform from the following list: `" + "`, `".join(self.platforms.keys()) + "`.")
            emb.set_footer(text="For help with game info commands, use %help gameinfo.")

        await ctx.send(embed=emb)


    # Checks if the given username/code to be added is the correct format
    async def _input_validator(self, ctx, *args):
        emb = discord.Embed(colour=ctx.author.colour)
        emb.set_author(name="Game Info for " + ctx.author.name + "#" + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
        emb.set_footer(text="For help with game info commands, use %help gameinfo.")

        # Regex matching to check input
        if args[0] == 'psn':
            if not re.match('^[0-9A-Za-z_-]{3,16}$', args[1]):
                emb.add_field(name="Invalid Playstation Network ID", value="Playstation Network IDs are 3-16 characters long and contain only `a-z`, `A-Z`, `0-9`, `_` or `-` characters.")
                await ctx.send(embed=emb)
                return False
        elif args[0] == 'xblive':
            if not re.match('^[A-Za-z][A-Za-z0-9 ]{0,13}[A-Za-z0-9]$', ' '.join(' '.join(args[1:]).split())):
                emb.add_field(name="Invalid Xbox Live Gamertag", value="Gamertags are up to 15 characters long and contain only `a-z`, `A-Z`, `0-9` characters and single spaces. They cannot start with a number or start or end with a space.")
                await ctx.send(embed=emb)
                return False
        elif args[0] == 'steam':
            if len(" ".join(args[1:])) > 64 or len(" ".join(args[1:])) < 3:
                emb.add_field(name="Invalid Steam Account", value="Steam account must be 3-64 characters long.")
                await ctx.send(embed=emb)
                return False
        else:
            if not re.match('^[0-9]{4}-[0-9]{4}-[0-9]{4}$', args[1]):
                emb.add_field(name="Invalid Friend Code", value="Please use the format `XXXX-XXXX-XXXX`.")
                await ctx.send(embed=emb)
                return False
        return True


    # Sets info for a specific platform
    @commands.command()
    async def set(self, ctx, *args):
        emb = discord.Embed(colour=ctx.author.colour)
        emb.set_author(name="Set Info for " + ctx.author.name + "#" + ctx.author.discriminator, icon_url=ctx.author.avatar_url)

        if args[0] not in self.platforms.keys():
            emb.add_field(name="Invalid Platform", value="Please use a platform from the following list: `" + "`, `".join(self.platforms.keys()) + "`.")
            emb.set_footer(text="For help with game info commands, use %help gameinfo.")
            await ctx.send(embed=emb)
            return

        is_valid = await self._input_validator(ctx, *args)

        if not is_valid:
            return

        info = args[1]
        if args[0] == 'xblive' or args[0] == 'steam':
            info = ' '.join(args[1:])

        cursor.execute("SELECT * FROM game_info WHERE member={};".format("'" + str(ctx.author.id) + "'"))
        rows = cursor.fetchall()

        if not rows:
            cursor.execute('INSERT INTO game_info (member, {}) VALUES ({}, {});'.format(self.platforms[args[0]], "'"+str(ctx.author.id)+"'", "'" + info + "'"))
        else:
            cursor.execute('UPDATE game_info SET {} = {} WHERE member = {};'.format(self.platforms[args[0]], "'" + info + "'", "'"+str(ctx.author.id)+"'"))

        emb.add_field(name="Successfully Added", value="{} successfully set as `{}`.".format(self.rev_dblist[args[0]], info))

        await ctx.send(embed=emb)

        conn.commit()


def setup(bot):
    bot.add_cog(GameInfoCog(bot))

def teardown(bot):
    bot.remove_cog(GameInfoCog(bot))