import discord
from discord.ext import commands
import esto as e
from pybooru import Danbooru


class LewdCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(enabled=False, hidden=True, aliases=["dan"])
    async def danbooru(self, ctx, *, args):
        client = Danbooru('danbooru')
        post = client.post_list(tags=args, limit=1)
        pic = post[0]
        if (pic['file_url'] == None):
            await ctx.send("An image matching this query could not be found on E621.")
        else:
            x = discord.Embed(title="#" + str(pic['id']) + ": " + pic['uploader_name'], url=pic['file_url'], colour=0x453399)
            x.set_image(url=pic['file_url'])
            x.set_footer(text="http://danbooru.donmai.us/posts/" + str(pic['id']) + "/")
            # if (len(pic['artist']) != 0):
            #     artist = pic['artist']
            #     x.add_field(name="Artist", value=artist)
            x.add_field(name="Score", value=pic['score'])
            x.add_field(name="URL", value=pic['file_url'])
            await ctx.send(embed = x)

    @staticmethod
    async def _e6_nsfw(ctx, args):
        if "random" in args:
            args = args.replace("random ", "")
            args = args.replace(" random", "")
            if (len(args.split(" ")) == 4):
                pic = e.getdata(args + " order:random" + " -rating:s")
            else:
                pic = e.getdata(args + " order:random" + " -rating:s -scat")
        else:
            if (len(args.split(" ")) == 5):
                pic = e.getdata(args + " -rating:s")
            else:
                pic = e.getdata(args + " -rating:s -scat")
        return pic

    @staticmethod
    async def _e6_sfw(ctx, args):
        if "random" in args:
            args = args.replace("random", "")
            pic = e.getdata(args + " order:random" + " rating:s")
        else:
            pic = e.getdata(args + " rating:s")
        return pic

    @commands.command(aliases=["e6"])
    async def e621(self, ctx, *, args):
        await ctx.channel.trigger_typing()
        if ((isinstance(ctx.channel, discord.TextChannel) and ctx.channel.is_nsfw()) or isinstance(ctx.channel, discord.abc.PrivateChannel)):
            pic = await self._e6_nsfw(ctx, args)
        elif (ctx.channel.name == "bot_spam" or ctx.channel.name == "spam"):
            pic = await self._e6_sfw(ctx, args)

        if (pic.file_url == None):
            await ctx.send("An image matching this query could not be found on E621.")
        else:
            x = discord.Embed(title="#" + pic.id + ": " + pic.author, url="https://e621.net/post/show/" + pic.id + "/", colour=0x453399)
            x.set_author(name="e621", icon_url="http://i0.kym-cdn.com/entries/icons/original/000/016/852/e621_logo.png")
            x.set_image(url=pic.file_url)
            x.set_footer(text="https://e621.net/post/show/" + pic.id + "/")
            if (len(pic.artists) != 0):
                artists = ", ".join(pic.artists)
                x.add_field(name="Artist(s)", value=artists)
            x.add_field(name="Score", value=pic.score)
            x.add_field(name="URL", value=pic.file_url)
            await ctx.send(embed = x)


def setup(bot):
    bot.add_cog(LewdCog(bot))
