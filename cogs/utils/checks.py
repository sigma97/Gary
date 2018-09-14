import discord
from discord.ext import commands

def is_superuser():
    def check_id(ctx):
        return ctx.author.id in [304980605207183370]
    return commands.check(check_id)

def is_trh():
    def check_id(ctx):
        return ctx.guild.id == 342025948113272833
    return commands.check(check_id)

def is_batcave():
    def check_id(ctx):
        return ctx.guild.id == 484966083795746816
    return commands.check(check_id)