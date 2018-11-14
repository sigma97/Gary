import discord
from discord.ext import commands
from imgurpython import ImgurClient
import random
import logging
from cogs.utils.imgur_key import client_id, client_key

log = logging.getLogger()

class ImgurCog:
    def __init__(self, bot):
        self.bot = bot
        self.client = ImgurClient(client_id, client_key)

    async def _images(self, ctx, id):

        try:
            album = self.client.get_album_images(id)
        except:
            log.error("'ImgurCog' - An error occurred while searching for the requested album.")
            return

        image = random.choice(album)
        await ctx.send(image.link)

    @commands.command()
    async def baned(self, ctx):
        await self._images(ctx, '72bJM')

    @commands.command(aliases=["loc"])
    async def location(self, ctx):
        await self._images(ctx, 'coJunoC')

    @commands.command(aliases=["zard"])
    async def charizard(self, ctx):
        await self._images(ctx, 'zlShR')

    @commands.command(aliases=["glisc", "scor"])
    async def gliscor(self, ctx):
        await self._images(ctx, 'EG51a5j')

    @commands.command(aliases=["esca"])
    async def escavalier(self, ctx):
        await self._images(ctx, 'WTWC33A')

    @commands.command(aliases=["serp", "snek"])
    async def serperior(self, ctx):
        await self._images(ctx, 'jRy06di')

    @commands.command(aliases=["puppo", "doggo", "pupper", "woofer", "pup"])
    async def dog(self, ctx):
        await self._images(ctx, 'vgW1p')

    @commands.command()
    async def zor(self, ctx):
        await self._images(ctx, 'keNO42K')

    @commands.command()
    async def heck(self, ctx):
        await self._images(ctx, 'FGa8rSl')

def setup(bot):
    bot.add_cog(ImgurCog(bot))

def teardown(bot):
    bot.remove_cog(ImgurCog(bot))