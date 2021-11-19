'''
Cog containing profile picture manipulation commands.
'''

import discord
from discord.ext import commands
from PIL import Image, ImageFilter
import PIL.ImageOps
import requests
from io import BytesIO
import cv2
import numpy as np

class PFPCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def canada(self, ctx, *, author: discord.Member = None):

        await ctx.channel.trigger_typing()

        if author == None:
            author = ctx.author

        # Grab the user's pfp
        response = requests.get(author.avatar_url_as(format="png", size=128))
        background = Image.open(BytesIO(response.content))
        foreground = Image.open("img/canada.png")

        # Apply foreground to background and save
        background.paste(foreground, (0, 0), foreground)
        background.save("temp.png", format="PNG")

        await ctx.send(file=discord.File("temp.png"))

    @commands.command()
    async def straya(self, ctx, *, author: discord.Member = None):

        if ctx.author.id not in [172242379678416896, 304980605207183370, 223020048074145792]:
            return

        await ctx.channel.trigger_typing()

        if author == None:
            author = ctx.author

        # Grab the user's pfp
        response = requests.get(author.avatar_url_as(format="png", size=128))
        background = Image.open(BytesIO(response.content))
        foreground = Image.open("img/straya.png")

        # Apply foreground to background and save
        background.paste(foreground, (0, 0), foreground)
        background.save("temp.png", format="PNG")

        await ctx.send(file=discord.File("temp.png"))

    @commands.command()
    async def murica(self, ctx, *, author: discord.Member = None):
        await ctx.channel.trigger_typing()

        if author == None:
            author = ctx.author

        # Grab the user's pfp
        response = requests.get(author.avatar_url_as(format="png", size=128))
        background = Image.open(BytesIO(response.content))
        foreground = Image.open("img/murica.png")

        # Apply foreground to background and save
        background.paste(foreground, (0, 0), foreground)
        background.save("temp.png", format="PNG")

        await ctx.send(file=discord.File("temp.png"))

    @commands.command()
    async def gayify(self, ctx, *, author: discord.Member = None):
        await ctx.channel.trigger_typing()

        if author == None:
            author = ctx.author

        # Grab the user's pfp
        response = requests.get(author.avatar_url_as(format="png", size=128))
        background = Image.open(BytesIO(response.content))
        foreground = Image.open("img/gay.png")

        # Apply foreground to background and save
        background.paste(foreground, (0, 0), foreground)
        background.save("temp.png", format="PNG")

        await ctx.send(file=discord.File("temp.png"))


    @commands.command()
    async def triggered(self, ctx, *, author: discord.Member = None):
        await ctx.channel.trigger_typing()

        if author == None:
            author = ctx.author

        background = Image.new("RGB", (128, 150))

        response = requests.get(author.avatar_url_as(format="png", size=128))
        new_im = Image.open(BytesIO(response.content))

        background.paste(new_im, (0, 0), new_im)

        # Easier than converting manually
        background.save("temp.png", format="PNG")
        img = cv2.imread("temp.png")

        size = 10

        # Create the motion blur
        # Credit to packtpub.com's article on motion blur using kernel
        kernel_motion_blur = np.zeros((size, size))
        kernel_motion_blur[int((size-1)/2), :] = np.ones(size)
        kernel_motion_blur = kernel_motion_blur / size

        # Apply the motion blur and save
        img = cv2.filter2D(img, -1, kernel_motion_blur)

        cv2.imwrite('temp.png', img)

        # Read saved file into PIL Image (easier than converting manually)
        background = Image.open("temp.png")
        foreground = Image.open("img/new_triggered.png")

        # Apply foreground to background
        background.paste(foreground, (0, 0), foreground)

        background.save("temp.png", format="PNG")

        await ctx.send(file=discord.File("temp.png"))


    @commands.command(aliases=['invert'])
    async def negative(self, ctx):

        # Retrieves and opens the image
        response = requests.get(ctx.author.avatar_url_as(format="png", size=256))
        img = Image.open(BytesIO(response.content)).convert('RGBA')

        r, g, b, a = img.split()

        # Inversion function
        def invert(image):
            return image.point(lambda p: 255 - p)

        # Converts RGB to negative values
        r, g, b = map(invert, (r, g, b))

        # Adds alpha value back
        img2 = Image.merge(img.mode, (r, g, b, a))

        # Saves and sends
        img2.save("temp.png")

        await ctx.send(file=discord.File("temp.png"))


def setup(bot):
    bot.add_cog(PFPCog(bot))

def teardown(bot):
    bot.remove_cog(PFPCog(bot))