'''
Converters for method arguments
'''

import discord
from discord.ext import commands

class UnspecifiedConverter(commands.IDConverter):
    """Converts to one of the following"""
    async def convert(self, ctx: commands.Context, argument: str):
        converters = [
            commands.converter.RoleConverter,
            commands.converter.CategoryChannelConverter,
            commands.converter.TextChannelConverter,
            commands.converter.VoiceChannelConverter,
            commands.converter.MemberConverter,
            commands.converter.EmojiConverter,
            commands.converter.ColourConverter,
            commands.converter.InviteConverter,
        ]
        result = None

        for converter in converters:
            try:
                instance = converter()
                if isinstance(instance, commands.converter.MemberConverter) and isinstance(ctx.channel, discord.DMChannel):
                    continue
                result = await instance.convert(ctx, argument)
                break
            except (commands.BadArgument, commands.NoPrivateMessage):
                continue

        if result is None:
            raise commands.BadArgument(f'Item "{argument}" not found.')

        return result
