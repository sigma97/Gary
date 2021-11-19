'''
Defines various checks for Gary's use.
'''

from discord.ext import commands

def is_superuser():
    '''Checks if Gary admin'''
    def check_id(ctx):
        return ctx.author.id in [304980605207183370]
    return commands.check(check_id)

def is_trh():
    '''Checks if in TRH'''
    def check_id(ctx):
        return ctx.guild.id == 342025948113272833
    return commands.check(check_id)

def is_batcave():
    '''Checks if in TBC'''
    def check_id(ctx):
        return ctx.guild.id == 484966083795746816
    return commands.check(check_id)

def is_batcave_mod():
    '''Checks if in TBC'''
    def check_id(ctx):
        return ctx.author.id in [304980605207183370, 195404515711778817, 
                                 283785520042082305, 342025565878091776]
    return commands.check(check_id)

def is_darkestcave():
    '''Checks if in TDC'''
    def check_id(ctx):
        return ctx.guild.id == 557283224330436621
    return commands.check(check_id)
