import discord
from discord.ext import commands
import requests
import json
import asyncio

client = discord.Client()

class TriviaCog:
    def __init__(self, bot):
        self.bot = bot

    async def _ans(self, ctx, data):
        def check(m):
            return m.content == 'done' and m.author == ctx.author

        try:
            await self.bot.wait_for('message', timeout=30.0, check=check)
            await ctx.channel.trigger_typing()
            await ctx.send(data[0]['answer'])
        except asyncio.TimeoutError:
            await ctx.channel.trigger_typing()
            await ctx.send(data[0]['answer'])

    async def _conn(self, ctx):
        param = {"count": 1}
        response = requests.get("http://jservice.io/api/random", params=param)
        raw_data = response.content.decode("utf-8")
        data = json.loads(raw_data)

        while data[0]['value'] >= 500 or data[0]['value'] is None:
            response = requests.get("http://jservice.io/api/random", params=param)
            raw_data = response.content.decode("utf-8")
            data = json.loads(raw_data)
        await ctx.send(data[0]['question'])
        await self._ans(ctx, data)

    @commands.command(hidden=True)
    async def trivia(self, ctx):
        await ctx.channel.trigger_typing()
        await self._conn(ctx)

def setup(bot):
    bot.add_cog(TriviaCog(bot))
