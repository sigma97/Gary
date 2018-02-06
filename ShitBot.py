import discord
import asyncio
import random
from quote import quotes

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='%quote'))

@client.event
async def on_message(message):
    if message.content.startswith('%quote'):
        x = random.choice(list(quotes.keys()))
        await client.send_message(message.channel, '"' + x + '" - ' + quotes[x])

client.run('NDEwMjM1NjgxMTA2MDM0Njg5.DVqNRA.5hICSESXedjhaue_vwXYu0JqVDY')
