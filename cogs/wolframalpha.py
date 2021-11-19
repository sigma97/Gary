'''
Cog containing commands using the WolframAlpha API.
'''

import discord
from discord.ext import commands
import wolframalpha


class WolframAlphaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = wolframalpha.Client('2QVLUQ-W92K8L7TR2')


    @commands.command(aliases=['wolfram', 'wa', 'wolframalpha'])
    async def query(self, ctx, query, *section):

        await ctx.channel.trigger_typing()

        emb = discord.Embed(colour=0xFDC81A)
        emb.set_author(name="Wolfram|Alpha", icon_url="https://pbs.twimg.com/profile_images/804868917990739969/OFknlig__400x400.jpg")

        res = self.client.query(query)

        if not section or section[0] == "sections":

            try:
                emb_string = ""

                for pod in res.pods:

                    emb_string += f"**{pod['@title']}**\n"

                    for subpod in pod.subpods:

                        if pod['@title'].lower() == "result" and not section:
                            result = discord.Embed(colour=0xFDC81A)
                            result.set_author(name="Wolfram|Alpha", icon_url="https://pbs.twimg.com/profile_images/804868917990739969/OFknlig__400x400.jpg")
                            result.add_field(name="Inputted Query", value=f"`{query}`")
                            result.add_field(name="Result", value=f"`{subpod['img']['@title']}`" if subpod['img']['@title'] else subpod['img']['@src'], inline=False)
                            result.set_image(url=subpod['img']['@src'])
                            result.set_footer(text='To see all sections for this query, use %query "[query]" sections.')
                            await ctx.send(embed=result)
                            return

                        if pod['@title'].lower() == "input interpretation":
                            emb.add_field(name="Input Interpretation", value=f"`{subpod['img']['@title']}`", inline=False)


            except:
                await ctx.send("Wolfram|Alpha does not understand your query.")
                return

            emb.add_field(name="Sections", value=emb_string)
            emb.set_footer(text='Use %query "[query]" [section_name] to see information on a specific section.')

            await ctx.send(embed=emb)
            return

        section = " ".join(section).lower()

        try:
            emb.add_field(name="Inputted Query", value=f"`{query}`")

            for pod in res.pods:

                for subpod in pod.subpods:

                    if pod['@title'].lower() == section:
                        emb.add_field(name=section.title(), value=f"`{subpod['img']['@title']}`" if subpod['img']['@title'] else subpod['img']['@src'], inline=False)
                        emb.set_image(url=subpod['img']['@src'])
                        break

        except:
            pass

        if len(emb.fields) <= 1:
            emb.add_field(name="Not Found", value="The requested field could not be retrieved or does not exist.")

        await ctx.send(embed=emb)

    
def setup(bot):
    bot.add_cog(WolframAlphaCog(bot))

def teardown(bot):
    bot.remove_cog(WolframAlphaCog(bot))