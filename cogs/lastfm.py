import discord
from discord.ext import commands
import requests
import json
import pylast
from cogs.utils.spotify_key import client_id, API_KEY, API_SECRET

class LastfmCog:
    def __init__(self, bot):
        self.bot = bot
        token = requests.post(
            'https://accounts.spotify.com/api/token',
            data={'grant_type': 'client_credentials'},
            auth=client_id)
        self.token = token.json()

    @commands.command()
    async def artist(self, ctx, *args):
        await ctx.channel.trigger_typing()

        # Set up the connection
        network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
        args = " ".join(args)
        artist = network.get_artist(args)
        artist_tags = artist.get_top_tags()
        artist_summary = artist.get_bio_summary().split('<a')[0].rstrip()
        artist_url = artist.get_url()
        tag_list = []

        for i in range(len(artist_tags)):
            if i > 3:
                break
            tag_list.append(artist_tags[i].item.get_name())

        tag_str = ", ".join(tag_list)

        # Build the embed
        embed = discord.Embed(colour=0xd51007)
        embed.set_author(name="Last.fm", icon_url="http://icons.iconarchive.com/icons/sicons/basic-round-social/512/last.fm-icon.png")
        embed.add_field(name="Artist", value=artist.get_name().title())
        embed.add_field(name="Description", value=artist_summary + "\n[Read more on Last.fm!]({})".format(artist_url + "/+wiki/"))
        embed.add_field(name="Genre(s)", value=tag_str.title(), inline=False)
        if artist.get_cover_image():
            embed.set_thumbnail(url=artist.get_cover_image())
        embed.add_field(name="Listeners", value=format(artist.get_listener_count(), ',d'))
        embed.add_field(name="Plays", value=format(artist.get_playcount(), ',d'))
        embed.add_field(name="Last.fm URL", value=artist_url, inline=False)
        embed.set_footer(text="For help with Last.fm commands, use %help last.fm.")
        await ctx.send(embed=embed)

    @commands.command()
    async def top_albums(self, ctx, *args):
        await ctx.channel.trigger_typing()

        # Set up connection
        network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
        args = " ".join(args)
        artist = network.get_artist(args)
        albums = artist.get_top_albums(limit=5)

        # Build the embed
        embed = discord.Embed(title="__Top albums by " + args.title() + "__", colour=0xd51007)
        if artist.get_cover_image():
            embed.set_thumbnail(url=artist.get_cover_image())
        embed.set_author(name="Last.fm", icon_url="http://icons.iconarchive.com/icons/sicons/basic-round-social/512/last.fm-icon.png")
        for i in range(len(albums)):
            if i > 4:
                break
            embed.add_field(name=str(i+1) + ". " + albums[i].item.get_name(),
            value="[{}]({})".format("View on Last.fm!", albums[i].item.get_url()), inline=False)
        embed.set_footer(text="For help with Last.fm commands, use %help last.fm.")
        await ctx.send(embed=embed)

    @commands.command()
    async def top_tracks(self, ctx, *args):
        await ctx.channel.trigger_typing()

        # Set up connection
        network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
        args = " ".join(args)
        artist = network.get_artist(args)
        tracks = artist.get_top_tracks(limit=5)

        # Build the embed
        embed = discord.Embed(title="__Top tracks by " + args.title() + "__", colour=0xd51007)
        if artist.get_cover_image():
            embed.set_thumbnail(url=artist.get_cover_image())
        embed.set_author(name="Last.fm", icon_url="http://icons.iconarchive.com/icons/sicons/basic-round-social/512/last.fm-icon.png")
        for i in range(len(tracks)):
            if i > 4:
                break
            embed.add_field(name=str(i+1) + ". " + tracks[i].item.get_name(),
            value="[{}]({})".format("View on Last.fm!", tracks[i].item.get_url()), inline=False)
        embed.set_footer(text="For help with Last.fm commands, use %help last.fm.")
        await ctx.send(embed=embed)

    @commands.command()
    async def album(self, ctx, *, args):
        await ctx.channel.trigger_typing()

        if "-" not in args:
            return

        args = args.split(" - ")

        if len(args) != 2:
            return

        # Set up connecton
        network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
        album = network.get_album(args[1], args[0])

        # Build the embed
        embed = discord.Embed(colour=0xd51007)
        embed.set_author(name="Last.fm", icon_url="http://icons.iconarchive.com/icons/sicons/basic-round-social/512/last.fm-icon.png")
        embed.add_field(name="Album", value=args[0].title(), inline=False)
        if album.get_cover_image():
            embed.set_thumbnail(url=album.get_cover_image())
        embed.add_field(name="Artist", value=args[1].title(), inline=False)
        embed.add_field(name="Listeners", value=format(album.get_listener_count(), ',d'))
        embed.add_field(name="Playcount", value=format(album.get_playcount(), ',d'))
        embed.add_field(name="Last.fm URL", value=album.get_url() + " \n\u200b", inline=False)
        embed.add_field(name="__Track Listing__", value="\u200b", inline=False)
        tracks = album.get_tracks()

        # Add tracks to embed
        i = 0
        for t in tracks:
            duration = t.get_duration()
            m = int(duration/60000)
            s = int((duration/1000)%60)
            embed.add_field(name=str(i+1) + ". " + t.get_name(), value="**Length:** `{}:{}`".format(m,str(s).zfill(2)), inline=False)
            i += 1
        embed.set_footer(text="For help with Last.fm commands, use %help last.fm.")
        await ctx.send(embed=embed)

    @commands.command()
    async def track(self, ctx, *, args):
        await ctx.channel.trigger_typing()

        if "-" not in args:
            return

        args = args.split(" - ")

        if len(args) != 2:
            return

        # Set up connection
        network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
        track = network.get_track(args[1], args[0])
        album = track.get_album()
        summary = track.get_wiki_summary()
        duration = track.get_duration()
        m = int(duration/60000)
        s = int((duration/1000)%60)

        # Grab the Spotify link
        q_str = 'https://api.spotify.com/v1/search?q=track:{}%20artist:{}&type=track&limit=10&access_token={}'.format(args[0], args[1], self.token['access_token'])
        results = requests.get(q_str)
        results = results.json()
        if len(results) > 0:
            track_link = "http://open.spotify.com/track/" + results['tracks']['items'][0]['id']

        # Build the embed
        embed = discord.Embed(colour=0xd51007)
        embed.set_author(name="Last.fm", icon_url="http://icons.iconarchive.com/icons/sicons/basic-round-social/512/last.fm-icon.png")
        embed.add_field(name="Track", value=args[0].title(), inline=False)
        embed.add_field(name="Artist", value=track.get_artist().get_name().title(), inline=False)
        embed.add_field(name="Album", value=track.get_album().get_title(), inline=False)
        if album:
            embed.set_thumbnail(url=album.get_cover_image())
        embed.add_field(name="Duration", value="`{}:{}`".format(m,str(s).zfill(2)), inline=False)
        if summary:
            embed.add_field(name="Description", value=summary.split('<a')[0].rstrip() + "\n[Read More on Last.fm!]({})".format(track.get_url() + '/+wiki'), inline=False)

        embed.set_footer(text="For help with Last.fm commands, use %help last.fm.")
        await ctx.send(embed=embed)
        await ctx.send(track_link)


def setup(bot):
    bot.add_cog(LastfmCog(bot))
