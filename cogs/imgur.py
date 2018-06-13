import discord
from discord.ext import commands
from imgurpython import ImgurClient
import random
from .utils.imgur_key import client_id, client_key

class ImgurCog:
    def __init__(self, bot):
        self.bot = bot
        self.client = ImgurClient(client_id, client_key)

    @commands.command()
    async def baned(self, ctx):
        album = self.client.get_album_images('72bJM')
        image = random.choice(album)
        embed= discord.Embed()
        embed.set_image(url=image.link)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ImgurCog(bot))
