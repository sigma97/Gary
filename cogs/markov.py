import discord
from discord.ext import commands
import markovify
from os import path

client = discord.Client()

class MarkovCog:
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    @client.event
    async def on_message(message):
        if (message.guild.id == 342025948113272833 or message.guild.id == 410225794904883202):
            file_path = "../logs/" + str(message.author.id) + ".txt"
            f = open(path.relpath(file_path), "a+")
            f.write("".join([x for x in (' '.join(message.content.split())) if x.isalnum() or x == ' ']) + " ")
            f.close()

    @commands.command(enabled=False, hidden=True)
    async def usermarkov(self, ctx):
        await ctx.channel.trigger_typing()
        with open("../logs/" + str(ctx.author.id) + ".txt") as f:
            text = f.read()
        text_model = markovify.Text(text)
        x = text_model.make_sentence()
        await ctx.send(x)


def setup(bot):
    bot.add_cog(MarkovCog(bot))
