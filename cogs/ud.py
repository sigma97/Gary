import discord
from discord.ext import commands
import urbandictionary as u


class UDCog:
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def _random_word(ctx):
        temp = u.random()[0]
        while (len(temp.definition) >= 1024):
            temp = u.random()[0]
        x = discord.Embed(colour=0xBBBBBB)
        x.set_author(name="Urban Dictionary", icon_url="https://d2gatte9o95jao.cloudfront.net/assets/apple-touch-icon-55f1ee4ebfd5444ef5f8d5ba836a2d41.png")
        x.set_footer(text="https://www.urbandictionary.com/define.php?term=" + temp.word.replace(" ", "%20"))
        x.set_thumbnail(url="https://d2gatte9o95jao.cloudfront.net/assets/apple-touch-icon-55f1ee4ebfd5444ef5f8d5ba836a2d41.png")
        x.add_field(name=temp.word, value=temp.definition, inline=False)
        x.add_field(name="Upvotes: ", value=temp.upvotes)
        x.add_field(name="Downvotes: ", value=temp.downvotes)
        await ctx.send(embed = x)

    @staticmethod
    async def _given_word(ctx, args):
        temp = u.define(args[0])
        if (len(temp) == 0):
            await ctx.send("This word or phrase could not be found on Urban Dictionary.")
        else:
            t = temp[0]
            for x in range(len(temp)):
                if (len(temp[x].definition) < 1024):
                    t = temp[x]
                    break
            if (len(t.definition) < 1024):
                x = discord.Embed(colour=0xBBBBBB)
                x.set_author(name="Urban Dictionary", icon_url="https://d2gatte9o95jao.cloudfront.net/assets/apple-touch-icon-55f1ee4ebfd5444ef5f8d5ba836a2d41.png")
                x.set_footer(text="https://www.urbandictionary.com/define.php?term=" + t.word.replace(" ", "%20"))
                x.set_thumbnail(url="https://d2gatte9o95jao.cloudfront.net/assets/apple-touch-icon-55f1ee4ebfd5444ef5f8d5ba836a2d41.png")
                x.add_field(name=t.word, value=t.definition, inline=False)
                x.add_field(name="Upvotes: ", value=t.upvotes)
                x.add_field(name="Downvotes: ", value=t.downvotes)
                await ctx.send(embed = x)
            else:
                await ctx.send("This word's definitions are too long for Discord.")

    @commands.command()
    async def ud(self, ctx, *args):
        await ctx.channel.trigger_typing()
        if (len(args) == 0):
            await self._random_word(ctx)
        else:
            await self._given_word(ctx, args)


def setup(bot):
    bot.add_cog(UDCog(bot))
