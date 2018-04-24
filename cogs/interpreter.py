import discord
from discord.ext import commands


class InterpreterCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(enabled=False, hidden=True)
    async def bf(self, ctx, *, args):
        inp = args[args.find("(")+1:args.find(")")]
        "".join(inp.split())
        args = args.split()
        arr = [0] * 30000
        index = 0
        res = ""
        await helper(inp, arr, index, args[1:], ctx, res)

    @staticmethod
    async def __bf_helper(inp, cells, index, args, ctx, res):
        if not inp:
            if (res == ""):
                return
            await ctx.send(res)
            return
        elif (inp[0] == '+'):
            cells[index] += 1
            await helper(inp[1:], cells, index, args, ctx, res)
        elif (inp[0] == '-'):
            cells[index] -= 1
            await helper(inp[1:], cells, index, args, ctx, res)
        elif (inp[0] == '>'):
            await helper(inp[1:], cells, index+1, args, ctx, res)
        elif (inp[0] == '<'):
            await helper(inp[1:], cells, index-1, args, ctx, res)
        elif (inp[0] == '.'):
            res += chr(cells[index])
            await helper(inp[1:], cells, index, args, ctx, res)
        elif (inp[0] == ','):
            if (args == []):
                await ctx.send("Too few arguments supplied.")
                return
            cells[index] = ord(args[0])
            await helper(inp[1:], cells, index, args[1:], ctx, res)
        elif (inp[0] == '['):
            new_str = inp[1:inp.find("]")]
            for i in range(int(cells[index])):
                await helper(new_str, cells, index, args, ctx, res)
            await helper(inp[inp.find("]")+1:], cells, index, args, ctx, res)
        else:
            await ctx.send("BrainFuck code not recognized.")
            return


def setup(bot):
    bot.add_cog(InterpreterCog(bot))
