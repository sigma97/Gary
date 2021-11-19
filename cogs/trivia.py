'''
Trivia cog utilizing a repository of over 150k Jeopardy questions. May be
turned into a server game in the future.
'''

import json
import asyncio
import string
import logging
import requests

import discord
from discord.ext import commands

log = logging.getLogger()

class TriviaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Prints out the answer after 30 seconds or after "done"
    async def _ans(self, ctx, data):

        # Define check for try/except
        def check(m):
            return m.content.lower() == '%done' and m.author == ctx.author

        # Times out after 30 seconds and posts answer
        try:
            await self.bot.wait_for('message', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            pass

        embed = discord.Embed(colour=0x0070bc)
        embed.add_field(name="Answer", value=data[0]['answer'])
        embed.set_author(name="Trivia", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS0JfbhsC-kZOM8URtBLcqj08f8H3JtdbkEpBlCGemS5SqNhNay")
        
        await ctx.send(embed=embed)

    # Connects to the API, sends a random question
    async def _conn(self, ctx):
        param = {"count": 1}

        try:
            response = requests.get("http://jservice.io/api/random", params=param)
            raw_data = response.content.decode("utf-8")
            data = json.loads(raw_data)
        except:
            log.error("'TriviaCog' - An error ocurred while fetching a trivia question.")

        # Recurse if NoneType
        if data[0]['value'] is None:
            await self._conn(ctx)
            return

        # Keeps searching until value <= 500
        while data[0]['value'] > 500:

            try:
                response = requests.get("http://jservice.io/api/random", params=param)
                raw_data = response.content.decode("utf-8")
                data = json.loads(raw_data)
            except:
                log.error("'TriviaCog' - An error ocurred while fetching a trivia question.")

            if data[0]['value'] is None:
                log.warning("'TriviaCog' - Unexpected null value in request response, recalling command.")

                await self._conn(ctx)
                return

        # Create question embed
        embed = discord.Embed(colour=0x0070bc)
        embed.add_field(name="Value", value=str(data[0]['value']), inline=True)
        embed.add_field(name="Category", value=string.capwords(data[0]['category']['title']))
        embed.add_field(name="Question", value=data[0]['question'], inline=False)
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

def teardown(bot):
    bot.remove_cog(TriviaCog(bot))