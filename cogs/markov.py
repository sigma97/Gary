import discord
from discord.ext import commands
import markovify


class MarkovCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(enabled=False, hidden=True)
    async def usermarkov(self, ctx):
        await ctx.channel.trigger_typing()
        channels = [x for x in ctx.guild.channels if isinstance(x, discord.TextChannel)
                          and (x.category_id in [408786484238483466]
                          or x.id in [410905286778290176, 408761145252511764, 409788610594734080, 416377470967742474, 418883686620987392])]
        messages = []
        for c in channels:
            ctr = 0
            async for m in c.history(limit=500):
                if m.author == ctx.author:
                    messages.append(m.content)
                    ctr += 1
                    if ctr >= 50:

                      break
        lst = await ctx.author.history().flatten()
        messages = [x for x in lst if x.content != ""]
        msgs = [x.content for x in messages]
        msg = "\n".join(msgs)
        text_model = markovify.NewlineText(msg)
        x = text_model.make_sentence()
        await ctx.send(x)


def setup(bot):
    bot.add_cog(MarkovCog(bot))
