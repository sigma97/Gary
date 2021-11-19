'''
Cog containing commands related to confessions
'''

import discord
from discord.ext import commands
import psycopg2
from cogs.utils import checks
import config as CONFIG

# Initialize database
conn = psycopg2.connect(dbname="quotes")
cursor = conn.cursor()

class ConfessionsCog(commands.Cog):
    '''Confessions commands for Gary'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["c"])
    async def confession(self, ctx, *, message):
        '''Posts an anonymous confession in TBC'''

        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Please use this command in DMs only.")
            return

        usr = str(ctx.author.id)
        usr = usr[::-1]

        cursor.execute(f"SELECT * FROM warnings WHERE user_id = '{usr}'")
        warn = cursor.fetchone()

        if warn:
            if warn[3]:
                await ctx.send("You have been blacklisted from Gary's Confessions. If you have any questions or concerns, DM Sigma#0472.")
                return

        cursor.execute("SELECT conf_id FROM confessions ORDER BY conf_id DESC LIMIT 1")
        rows = cursor.fetchone()

        if not rows:
            conf_id = 1
        else:
            conf_id = rows[0] + 1

        usr = str(ctx.author.id)

        user_id = usr[::-1]

        msg = message.replace("'", "''")

        cursor.execute(f"INSERT INTO confessions VALUES ({conf_id}, '{user_id}', '{msg}')")

        channel = self.bot.get_channel(547550104328863768)
        log = self.bot.get_channel(547548650574970890)

        emb = discord.Embed(description=message, color=CONFIG.emb_color)
        emb.set_author(name=f"Gary's Confession #{conf_id}", icon_url=CONFIG.emb_icon)

        await channel.send(embed=emb)

        emb.add_field(name="Author", value=ctx.author.mention)

        await log.send(embed=emb)

        await ctx.send("Confession sent!")
        
        conn.commit()


    @checks.is_superuser()
    @commands.command()
    async def get_author(self, ctx, conf_id):

        conf_id = int(conf_id)

        cursor.execute(f"SELECT user_id FROM confessions WHERE conf_id = {conf_id}")
        rows = cursor.fetchone()

        if not rows:
            await ctx.send("Confession not found.")
        else:
            usr = rows[0]

            user_id = usr[::-1]

            usr = await self.bot.get_user_info(int(user_id))
            await ctx.send(usr.mention)

    @checks.is_batcave_mod()
    @commands.command()
    async def warn(self, ctx, conf_id, *, msg):

        conf_id = int(conf_id)

        cursor.execute(f"SELECT user_id, confession FROM confessions WHERE conf_id = {conf_id}")

        rows = cursor.fetchone()

        if not rows:
            await ctx.send("Confession not found.")
            return

        cursor.execute(f"SELECT * FROM warnings WHERE user_id = '{rows[0]}'")

        warns = cursor.fetchone()

        user_id = rows[0][::-1]
        usr = await self.bot.get_user_info(int(user_id))

        emb = discord.Embed(color=CONFIG.emb_color)
        emb.set_author(name=f"Confessions Warning", icon_url=CONFIG.emb_icon)

        if not warns:
            cursor.execute(f"INSERT INTO warnings VALUES ('{rows[0]}', true, false, false)")
            emb.add_field(name="Warning #1", value=f"You are being issued a first warning for the following confession:\n```{rows[1]}```")
            emb.add_field(name="Mod Note", value=f"```{msg}```")
            await usr.send(embed=emb)
        elif warns[2] == False:
            cursor.execute("UPDATE warnings SET warn2 = true")
            emb.add_field(name="Warning #2", value=f"You are being issued a second warning for the following confession:\n```{rows[1]}```")
            emb.add_field(name="Mod Note", value=f"```{msg}```")
            await usr.send(embed=emb)
        elif warns[3] == False:
            cursor.execute("UPDATE warnings SET warn3 = true")
            emb.add_field(name="Blacklisted", value=f"You have been blacklisted from Gary's Confessions for the following confession:\n```{rows[1]}```")
            emb.add_field(name="Mod Note", value=f"```{msg}```")
            emb.set_footer(text="If you have any questions or concerns about this decision, DM Sigma#0472.")
            await usr.send(embed=emb)

            ch = self.bot.get_channel(484968129466859520)
            await ch.send(f"{usr.mention} has been blacklisted from Gary's Confessions.")
        else:
            await ctx.send("Error: User already has 3 warnings.")
            return

        conn.commit()

        await ctx.send(f"Issued warning to the author of confession #{conf_id}.")


def setup(bot):
    '''Adds cog to Gary'''
    bot.add_cog(ConfessionsCog(bot))


def teardown(bot):
    '''Removes cog from Gary'''
    bot.remove_cog(ConfessionsCog(bot))