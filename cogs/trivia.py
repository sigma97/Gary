import discord
from discord.ext import commands
import requests
import json
import asyncio
import string

class TriviaCog:
    def __init__(self, bot):
        self.bot = bot

    # Prints out the answer after 30 seconds or after "done"
    async def _ans(self, ctx, data):

        # Define check for try/except
        def check(m):
            return m.content.lower() == 'done' and m.author == ctx.author

        try:
            await self.bot.wait_for('message', timeout=30.0, check=check)
            await ctx.channel.trigger_typing()
            embed = discord.Embed(colour=0x0070bc)
            embed.add_field(name="Answer", value=data[0]['answer'])
            embed.set_author(name="Trivia", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS0JfbhsC-kZOM8URtBLcqj08f8H3JtdbkEpBlCGemS5SqNhNay")
            await ctx.send(embed=embed)
        except asyncio.TimeoutError:
            await ctx.channel.trigger_typing()
            embed = discord.Embed(colour=0x0070bc)
            embed.add_field(name="Answer", value=data[0]['answer'])
            embed.set_author(name="Trivia", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS0JfbhsC-kZOM8URtBLcqj08f8H3JtdbkEpBlCGemS5SqNhNay")
            await ctx.send(embed=embed)

    # Connects to the API, sends a random question
    async def _conn(self, ctx):
        param = {"count": 1}
        response = requests.get("http://jservice.io/api/random", params=param)
        raw_data = response.content.decode("utf-8")
        data = json.loads(raw_data)

        # Recurse if NoneType
        if data[0]['value'] is None:
            await self._conn(ctx)
            return

        # Keeps searching until value <= 500
        while data[0]['value'] > 500:
            response = requests.get("http://jservice.io/api/random", params=param)
            raw_data = response.content.decode("utf-8")
            data = json.loads(raw_data)
            if data[0]['value'] is None:
                await self._conn(ctx)
                return

        # Create question embed
        embed = discord.Embed(colour=0x0070bc)
        embed.add_field(name="Value", value=str(data[0]['value']), inline=True)
        embed.add_field(name="Category", value=string.capwords(data[0]['category']['title']))
        embed.add_field(name="Question", value=data[0]['question'])
        embed.set_author(name="Trivia", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS0JfbhsC-kZOM8URtBLcqj08f8H3JtdbkEpBlCGemS5SqNhNay")
        await ctx.send(embed=embed)
        await self._ans(ctx, data)

    # Displays a random question then posts an answer 30 seconds later
    @commands.command(hidden=True)
    async def trivia(self, ctx):
        await ctx.channel.trigger_typing()
        await self._conn(ctx)

def setup(bot):
    bot.add_cog(TriviaCog(bot))
