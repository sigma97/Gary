'''
Credit to Rapptz for the majority of this cog.

Evaluates a given code snippet.
'''

import textwrap
import traceback
from discord.ext import commands
import io
import psycopg2
from cogs.utils import checks
from contextlib import redirect_stdout

# Properly crediting the author
__title__ = "eval"
__author__ = "Rapptz"
__copyright__ = "Copyright 2018 Rapptz"

conn = psycopg2.connect(dbname="quotes")
cursor = conn.cursor()

class Eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    # Apparently this is a thing in discord.py now
    async def __local_check(self, ctx):
        return await self.bot.is_owner(ctx.author)


    @checks.is_superuser()
    @commands.command(pass_context=True, hidden=True, name='eval')
    async def _eval(self, ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')
                

def setup(bot):
    bot.add_cog(Eval(bot))

def teardown(bot):
    bot.remove_cog(Eval(bot))