import discord
from discord.ext import commands
import psycopg2
import random


conn = psycopg2.connect(dbname="quotes")
cursor = conn.cursor()

class QuoteCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def quote(self, ctx, *args):
        if (len(args) == 0):
            cursor.execute("""SELECT * FROM quotes""")
            rows = cursor.fetchall()
            x = random.choice(rows)
        else:
            cursor.execute("SELECT * FROM quotes WHERE id={};".format(int(args[0])))
            rows = cursor.fetchall()
            x = rows[0]
        await ctx.send('"' + x[1] + '" - ' + x[0])

    @commands.command()
    async def add(self, ctx, arg1, arg2):
        is_mod = False
        for x in ctx.author.roles:
            if (x.name == "Auxiliary"):
                is_mod = True
        if (is_mod):
            query = "INSERT INTO quotes (username, quote, id) VALUES (%s, %s, %s);"
            cursor.execute("""SELECT * from quotes""")
            rows = cursor.fetchall()
            data = (arg1, arg2, int(rows[len(rows)-1][2]) + 1)
            cursor.execute(query, data)
            conn.commit()
            await ctx.send("Quote added!")
        else:
            await ctx.send("You do not have the correct permissions to use this command.")

    @commands.command()
    async def delete(self, ctx, arg):
        is_mod = False
        for x in ctx.author.roles:
            if (x.name == "Auxiliary"):
                is_mod = True
        if (is_mod):
            cursor.execute("DELETE FROM quotes WHERE id={};".format(arg))
            conn.commit()
            await ctx.send("Quote deleted!")
        else:
            await ctx.send("You do not have the correct permissions to use this command.")

    @commands.command()
    async def ids(self, ctx):
        channel = ctx.message.author.dm_channel
        if (channel == None):
            await ctx.message.author.create_dm()
            channel = ctx.message.author.dm_channel
        await channel.trigger_typing()
        cursor.execute("""SELECT quote, id from quotes""")
        rows = cursor.fetchall()
        lst = []
        msgs = []
        for r in rows:
            t = str(r[1])
            x = "`" + t + "`" + ": " + r[0]
            if (sum(len(i) for i in lst) + len(x) >= 1000):
                msgs.append("\n".join(lst))
                lst = []
            lst.append(x)
        msgs.append("\n".join(lst))
        conn.commit()
        for y in msgs:
            emb = discord.Embed(colour=0x33B5E5)
            emb.set_author(name="Gary's Quote IDs", icon_url="https://i.neoseeker.com/mgv/297579/579/118/lord_garyVJPHT_display.png")
            emb.add_field(name="IDs", value=y)
            await channel.send(embed = emb)

    ids.brief = "Lists the quote IDs."
    ids.help = "Lists the quote IDs from Gary's database."

def setup(bot):
    bot.add_cog(QuoteCog(bot))
