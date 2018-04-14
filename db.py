import discord
from discord.ext import commands
import psycopg2

#################################################################
#                                                               #
#                                                               #
#                                                               #
#                                                               #
# This section contains all of the code for generating sprites. #
#                                                               #
#                                                               #
#                                                               #
#                                                               #
#################################################################


@bot.command()
async def add(ctx, arg1, arg2):
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

add.usage = '[User] "quote"'
add.brief = "Adds a quote to Gary."
add.help = "Adds a quote to Gary's database."

@bot.command()
async def delete(ctx, arg):
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

delete.usage = '[ID #]'
delete.brief = "Deletes a quote from Gary."
delete.help = "Deletes a quote from Gary's database."

@bot.command()
async def ids(ctx):
    channel = ctx.message.author.dm_channel
    if (channel == None):
        await ctx.message.author.create_dm()
        channel = ctx.message.author.dm_channel
    cursor.execute("""SELECT quote, id from quotes""")
    rows = cursor.fetchall()
    lst = []
    msgs = []
    for r in rows:
        t = str(r[1])
        x = "**" + t + "**" + ": " + r[0]
        if (sum(len(i) for i in lst) + len(x) >= 1900):
            msgs.append("\n".join(lst))
            lst = []
        lst.append(x)
    msgs.append("\n".join(lst))
    conn.commit()
    for y in msgs:
        await channel.send(y)

ids.brief = "Lists the quote IDs."
ids.help = "Lists the quote IDs from Gary's database."
