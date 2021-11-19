'''
Cog for saving funny/memorable quotes by users in the server in a database.
Returns one of these quotes at random when %quote is used, but users can also
find quotes using their IDs and the author.
'''

import psycopg2
import random

import discord
from discord.ext import commands
import config

conn = psycopg2.connect(dbname="quotes")
cursor = conn.cursor()

class QuoteCog(commands.Cog):
    '''Cog for anything and everything quote-related'''
    def __init__(self, bot):
        self.bot = bot

    # Finds quotes by the given user
    @commands.command()
    async def quotes(self, ctx, *args):
        '''Fetches all quotes for the given user in the server'''
        if ctx.guild.id == 342025948113272833 or ctx.guild.id == 410225794904883202:
            cursor.execute("SELECT * FROM quotes WHERE username={} ORDER BY id".format("'" + args[0].title() + "'"))
        elif ctx.guild.id == 484966083795746816:
            cursor.execute("SELECT * FROM tbc_quotes WHERE username={} ORDER BY id".format("'" + args[0].title() + "'"))
        elif ctx.guild.id == 557283224330436621:
            cursor.execute("SELECT * FROM tdc_quotes WHERE username={} ORDER BY id".format("'" + args[0].title() + "'"))
        else:
            return

        rows = cursor.fetchall()
        lst = []
        msgs = []

        for r in rows:
            x = "`" + str(r[2]) + "`" + ": "+ r[1]
            if (sum(len(i) for i in lst) + len(x) >= 1000):
                msgs.append("\n".join(lst))
                lst = []
            lst.append(x)

        msgs.append("\n".join(lst))
        conn.commit()

        if not rows:
            emb = discord.Embed(colour=config.emb_color)
            emb.set_author(name="Quote IDs for " + args[0].title(), icon_url=config.emb_icon)
            emb.add_field(name="IDs", value="No quotes were found for this user.")
            await ctx.send(embed = emb)
        else:
            for y in msgs:
                emb = discord.Embed(colour=config.emb_color)
                emb.set_author(name="Quote IDs for " + args[0].title(), icon_url=config.emb_icon)
                emb.add_field(name="IDs", value=y)
                await ctx.send(embed = emb)

    # Finds quote with a given ID. Returns one at random if no ID is given.
    @commands.command()
    async def quote(self, ctx, *args: int):
        '''Returns a random quote or quote with the given ID'''

        if ctx.guild.id == 342025948113272833 or ctx.guild.id == 410225794904883202:
            q = "quotes"
        elif ctx.guild.id == 484966083795746816:
            q = "tbc_quotes"
        elif ctx.guild.id == 557283224330436621:
            q = "tdc_quotes"
        else: 
            return
        
        if len(args) == 0:
            cursor.execute("SELECT * FROM {} ORDER BY id".format(q))
            rows = cursor.fetchall()
            x = random.choice(rows)
        else:
            cursor.execute("SELECT * FROM {} WHERE id={}".format(q, int(args[0])))
            rows = cursor.fetchall()
            if not rows:
                await ctx.send("No quote found with this ID.")
                return
            x = rows[0]
        await ctx.send('"' + x[1] + '" - ' + x[0])

    # Adds a quote given user and the quote surrounded by ""
    @commands.command()
    async def add(self, ctx, arg1, arg2):
        '''Adds a quote'''
        is_mod = False

        if ctx.guild.id == 342025948113272833:
            for x in ctx.author.roles:
                if (x.id == 408774803424673792):
                    is_mod = True
                    
            q = "quotes"

        elif ctx.guild.id == 484966083795746816:
            for x in ctx.author.roles:
                if (x.id == 484967354217005065):
                    is_mod = True

            q = "tbc_quotes"

        elif ctx.guild.id == 557283224330436621:
            for x in ctx.author.roles:
                if x.id == 558093373915791361:
                    is_mod = True
            
            q = "tdc_quotes"

        arg1 = arg1.replace("'", "''")
        arg2 = arg2.replace("'", "''")

        if (is_mod):
            cursor.execute("SELECT * from {} ORDER BY id DESC".format(q))
            rows = cursor.fetchall()[0]
            cursor.execute("INSERT INTO {} (username, quote, id) VALUES ('{}', '{}', {})".format(q, arg1, arg2, str(rows[2] + 1)))
            conn.commit()
            await ctx.send("Quote added!")
        else:
            await ctx.send("You do not have the correct permissions to use this command.")

    # Deletes a quote given the ID
    @commands.command()
    async def delete(self, ctx, arg):
        '''Removes a quote from Gary'''
        is_mod = False

        if ctx.guild.id == 342025948113272833:
            for x in ctx.author.roles:
                if (x.name == "Auxiliary"):
                    is_mod = True
                    
            q = "quotes"

        elif ctx.guild.id == 484966083795746816:
            for x in ctx.author.roles:
                if x.id == 484967354217005065:
                    is_mod = True

            q = "tbc_quotes"

        elif ctx.guild.id == 557283224330436621:
            for x in ctx.author.roles:
                if x.id == 558093373915791361:
                    is_mod = True
            
            q = "tdc_quotes"

        if (is_mod):
            cursor.execute("DELETE FROM {} WHERE id={}".format(q, arg))
            conn.commit()
            await ctx.send("Quote deleted!")
        else:
            await ctx.send("You do not have the correct permissions to use this command.")

    # DMs user all of the quotes and IDs (use sparingly, may produce a lot of messages)
    @commands.command()
    async def ids(self, ctx):
        '''Returns all quotes and IDs'''

        channel = ctx.message.author.dm_channel

        if channel is None:
            await ctx.message.author.create_dm()
            channel = ctx.message.author.dm_channel

        await channel.trigger_typing()

        if ctx.guild.id == 342025948113272833:
            q = "quotes"
        elif ctx.guild.id == 484966083795746816:
            q = "tbc_quotes"

        cursor.execute("SELECT quote, id, username FROM {} ORDER BY id".format(q))

        rows = cursor.fetchall()

        lst = []
        msgs = []

        for r in rows:

            t = str(r[1])
            x = "`" + t + "`" + ": "+ "**" + r[2] + "** - " + r[0]

            if sum(len(i) for i in lst) + len(x) >= 1000:
                msgs.append("\n".join(lst))
                lst = []

            lst.append(x)

        msgs.append("\n".join(lst))
        conn.commit()

        for y in msgs:
            emb = discord.Embed(colour=config.emb_color)
            emb.set_author(name="Gary's Quote IDs", icon_url=config.emb_icon)
            emb.add_field(name="IDs", value=y)
            await channel.send(embed = emb)


def setup(bot):
    '''Adds cog'''
    bot.add_cog(QuoteCog(bot))

def teardown(bot):
    '''Removes cog'''
    bot.remove_cog(QuoteCog(bot))
