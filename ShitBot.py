import discord
from discord.ext import commands
import urbandictionary as u
import esto as e
import markovify
# from pybooru import Danbooru

client = discord.Client()
bot = commands.Bot(command_prefix='%', pm_help=True)

bot.remove_command("help")

extensions = ['cogs.quotes',
              'cogs.sprites',
              'cogs.users',
              'cogs.general',
              'cogs.interpreter']

if __name__ == '__main__':
    for e in extensions:
        bot.load_extension(e)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user)
    print('------')
    await bot.change_presence(activity=discord.Game(name='%help'))

@bot.command()
async def ud(ctx, *args):
    await ctx.channel.trigger_typing()
    if (len(args) == 0):
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
    else:
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

@bot.command()
async def e621(ctx, *, args):
    await ctx.channel.trigger_typing()
    if ((isinstance(ctx.channel, discord.TextChannel) and ctx.channel.is_nsfw()) or isinstance(ctx.channel, discord.abc.PrivateChannel)):
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
    elif (ctx.channel.name == "bot_spam" or ctx.channel.name == "spam"):
        if "random" in args:
            args = args.replace("random", "")
            pic = e.getdata(args + " order:random" + " rating:s")
        else:
            pic = e.getdata(args + " rating:s")

    if (pic.file_url == None):
        await ctx.send("An image matching this query could not be found on E621.")
    else:
        x = discord.Embed(title="#" + pic.id + ": " + pic.author, url=pic.file_url, colour=0x453399)
        x.set_image(url=pic.file_url)
        x.set_footer(text="https://e621.net/post/show/" + pic.id + "/")
        if (len(pic.artists) != 0):
            artists = ", ".join(pic.artists)
            x.add_field(name="Artist(s)", value=artists)
        x.add_field(name="Score", value=pic.score)
        x.add_field(name="URL", value=pic.file_url)
        await ctx.send(embed = x)

# @bot.command()
# async def danbooru(ctx, *, args):
#     client = Danbooru('danbooru')
#     post = client.post_list(tags=args, limit=1)
#     pic = post[0]
#     if (pic['file_url'] == None):
#         await ctx.send("An image matching this query could not be found on E621.")
#     else:
#         x = discord.Embed(title="#" + str(pic['id']) + ": " + pic['uploader_name'], url=pic['file_url'], colour=0x453399)
#         x.set_image(url=pic['file_url'])
#         x.set_footer(text="http://danbooru.donmai.us/posts/" + str(pic['id']) + "/")
#         # if (len(pic['artist']) != 0):
#         #     artist = pic['artist']
#         #     x.add_field(name="Artist", value=artist)
#         x.add_field(name="Score", value=pic['score'])
#         x.add_field(name="URL", value=pic['file_url'])
#         await ctx.send(embed = x)

@bot.command()
async def nuke(ctx):
    is_mod = False
    for x in ctx.author.roles:
        if (x.name == "Auxiliary"):
            is_mod = True
    if (ctx.channel.name == "the_wall" and is_mod):
        await ctx.channel.purge();

# @bot.command()
# async def usermarkov(ctx):
#     await ctx.channel.trigger_typing()
    # channels = [x for x in ctx.guild.channels if isinstance(x, discord.TextChannel)
    #                   and (x.category_id in [408786484238483466]
    #                   or x.id in [410905286778290176, 408761145252511764, 409788610594734080, 416377470967742474, 418883686620987392])]
    # messages = []
    # for c in channels:
    #     ctr = 0
    #     async for m in c.history(limit=500):
    #         if m.author == ctx.author:
    #             messages.append(m.content)
    #             ctr += 1
    #             if ctr >= 50:
    #
    #               break
    # lst = await ctx.author.history().flatten()
    # messages = [x for x in lst if x.content != ""]
    # msgs = [x.content for x in messages]
    # msg = "\n".join(msgs)
    # text_model = markovify.NewlineText(msg)
    # x = text_model.make_sentence()
    # await ctx.send(x)


bot.run('NDEwMjM1NjgxMTA2MDM0Njg5.DVqNRA.5hICSESXedjhaue_vwXYu0JqVDY')
