'''
Cog that defines Gary's in-depth help menu system.
'''

import discord
from discord.ext import commands

import config

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.menus = ["last.fm", "gameinfo", "imgur", "quotes", "sprites"]

    # Help menu having to do with the Last.fm cog
    @staticmethod
    async def _lastfm_help(channel):

        lfm = """ `%artist [artist name]`\nDisplays information on the given artist.\n
`%top_albums [artist name]`\nDisplays the top five albums by the given artist.\n
`%top_tracks [artist name]`\nDisplays the top five tracks by the given artist.\n
`%album [album name] - [artist name]`\nDisplays information on the given album as well as a tracklist.\n
`%track [track name] - [artist name]`\nDisplays a playable Spotify link to the given track.\n\u200b"""

        msg = discord.Embed(description="*The following is a list of Last.fm commands that can be used with Gary.*", colour=config.emb_color)
        msg.set_footer(text="For any additional inquiries, please DM Sigma#0472.")
        msg.set_author(name="Gary Help Menu", icon_url=config.emb_icon)
        msg.add_field(name="Last.fm Commands", value=lfm, inline=True)

        await channel.send(embed=msg)


    # Help menu having to do with the Gameinfo cog
    @staticmethod
    async def _gameinfo_help(channel):

        gi = """ `%gameinfo`\nDisplays all account names/friend codes of the user.\n
`%get [platform]`\nDisplays user's information on the given platform.\n
`%set [platform] [arg]`\nAdds the given arg as information on the given platform for the user.\n\u200b"""

        msg = discord.Embed(description="*The following is a list of game info commands that can be used with Gary.*", colour=config.emb_color)
        msg.set_footer(text="For any additional inquiries, please DM Sigma#0472.")
        msg.set_author(name="Gary Help Menu", icon_url=config.emb_icon)
        msg.add_field(name="Game Info Commands", value=gi, inline=True)
        msg.add_field(name="Valid Platforms", value="`psn`, `xblive`, `steam`, `switch`, `3ds`\n\u200b", inline=True)
        msg.add_field(name="__Note:__", value="Nintendo Switch and 3DS Friend Codes must be submitted with the following format: `XXXX-XXXX-XXXX`")
        
        await channel.send(embed=msg)


    # Help menu having to do with the Imgur cog
    @staticmethod
    async def _imgur_help(channel):

        im = """ `%baned`\nDisplays a random 'baned' image.\n
`%location` **or** `%loc`\nDisplays a location card from Pokemon FR/LG.\n
`%charizard` **or** `%zard`\nDisplays a random Charizard image.\n
`%gliscor` **or** `%glisc`, `%scor`\nDisplays a random Gliscor image.\n
`%escavalier` **or** `%esca`\nDisplays a random Escavalier image.\n
`%serperior` **or** `%serp`, `%snek`\nDisplays a random Serperior image.\n\u200b"""

        msg = discord.Embed(description="*The following is a list of Imgur commands that can be used with Gary.*", colour=config.emb_color)
        msg.set_footer(text="For any additional inquiries, please DM Sigma#0472.")
        msg.set_author(name="Gary Help Menu", icon_url=config.emb_icon)
        msg.add_field(name="Imgur Commands", value=im, inline=True)
        msg.add_field(name="__Note:__", value="To have an Imgur album added to Gary, ping or DM Sigma.")
        
        await channel.send(embed=msg)


    # Help menu having to do with the Quotes cog
    @staticmethod
    async def _quotes_help(channel):

        quotes = """ `%quote [id (optional)]`\nDisplays the quote with the specified ID. If none is given, a random quote is returned.\n
`%add [user] [quote]`\nAuxiliary only. Adds a new quote to Gary's list.\n
`%delete [id]`\nAuxiliary only. Deletes a quote from Gary's list.\n
`%ids`\nDMs the user a list of quotes and their IDs.\n
`%quotes [user]`\nDisplays all of the quotes and their IDs by the given user.\n\u200b"""

        msg = discord.Embed(description="*The following is a list of quote commands that can be used with Gary.*", colour=config.emb_color)
        msg.set_footer(text="For any additional inquiries, please DM Sigma#0472.")
        msg.set_author(name="Gary Help Menu", icon_url=config.emb_icon)
        msg.add_field(name="Quote Commands", value=quotes, inline=True)
        
        await channel.send(embed=msg)


    # Help menu having to do with the Sprites cog
    @staticmethod
    async def _sprite_help(channel):

        spr = """`%pmd [pokedex #]`\nDisplays the PMD icon of the given Pokemon.\n
`%[pokemon game] [pokemon]`\nDisplays the sprite of the given pokemon from the specified game. Valid commands are:
`%rb`, `%yellow`, `%gold`, `%silver`, `%crystal`, `%rse`, `%frlg`, `%dppt`, `%hgss`, `%bw`, `%xy`, `%sm`.\n
`%[user]`\nDisplays the pokemon commonly associated with the specified user.\n\u200b"""

        msg = discord.Embed(description="*The following is a list of sprite commands that can be used with Gary.*", colour=config.emb_color)
        msg.set_footer(text="For any additional inquiries, please DM Sigma#0472.")
        msg.set_author(name="Gary Help Menu", icon_url=config.emb_icon)
        msg.add_field(name="Sprite Commands", value=spr, inline=True)
        msg.add_field(name="__Note:__", value="If your name does not yet have a command and you would like one, DM Sigma with the pokemon you want.")
        
        await channel.send(embed=msg)


    # Routes to the appropriate help function
    async def _help_redirect(self, channel, args):
        if args[0] == 'last.fm':
            await self._lastfm_help(channel)
        elif args[0] == 'gameinfo':
            await self._gameinfo_help(channel)
        elif args[0] == 'imgur':
            await self._imgur_help(channel)
        elif args[0] == 'quotes':
            await self._quotes_help(channel)
        elif args[0] == 'sprites':
            await self._sprite_help(channel)
        else:
            return


    # Base command, given args redirects to the appropriate help menu
    @commands.command()
    async def help(self, ctx, *args):
        channel = ctx.message.author.dm_channel

        if (channel == None):
            channel = await ctx.message.author.create_dm()

        await channel.trigger_typing()

        if args:
            if args[0] in self.menus:
                await self._help_redirect(channel, args)
                return

        gen = """ `%help [string (optional)]`\nDisplays this message. If given an argument, displays information on the set of commands. Valid arguments are:\n`quotes`, `gameinfo`, `sprites`, `imgur`, `last.fm`.\n
`%userinfo [user (optional)]`\nDisplays information on the given user, or if none is supplied, the member using the command.\n
`%echo [string]`\nRepeats the text inputted by the user.\n
`%bigtext [string]`\nRepeats the inputted string in bigtext.\n
`%vote`\nInitiates a vote using the 👍, 👎, and 🤔 reactions.\n
`%roll [# sides (optional)]`\nDisplays a random number in the given range (six by default).\n
`%flip`\nReturns "Heads" or "Tails" at random.\n
`%feed_vap`\nFeeds Vap.\n
`%oracle`\nMagic 8-Ball.\n
`%ud [word or phrase (optional)]`\nReturns Urban Dictionary definition of supplied word. If no word is supplied, returns a random word and definition.\n
`%e621 [query]`\nReturns the top e621 image of the given query. Can only be used in #bot_spam (SFW) and #nsfw_pics (NSFW).\n\u200b"""

        msg = discord.Embed(description="*The following is a list of general commands that can be used with Gary.*", colour=config.emb_color)
        msg.set_footer(text="For any additional inquiries, please DM Sigma#0472.")
        msg.set_author(name="Gary Help Menu", icon_url=config.emb_icon)
        msg.add_field(name="General Commands", value=gen, inline=True)
        await channel.send(embed = msg)

def setup(bot):
    bot.add_cog(HelpCog(bot))

def teardown(bot):
    bot.remove_cog(HelpCog(bot))