'''
Cog containing scheduling commands.
'''

import discord
from discord.ext import commands

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import date

class ScheduleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.days = ['mon','tue','wed','thu','fri','sat','sun']
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(self.open_sns, 'cron', day_of_week="sat", hour=23, minute=45, timezone="EST")
        self.scheduler.add_job(self.close_sns, 'cron', day_of_week="sun", hour=23, minute=45, timezone="EST")
        self.scheduler.start()
    
    
    async def open_sns(self):

        me = self.bot.get_user(304980605207183370)

        await me.send("It's 11:45 PM on Saturday, that means it's almost time to open Sweet 'n' Sour!")

    async def close_sns(self):

        me = self.bot.get_user(304980605207183370)

        await me.send("It's 11:45 PM on Sunday, that means it's almost time to close Sweet 'n' Sour!")


    @staticmethod
    async def new_reminder(ctx, message):

        await ctx.author.send(message)


    @commands.command()
    async def set_reminder(self, ctx, kind, day, time, *, message):

        if kind == 'weekly': 
            if day not in self.days:
                await ctx.send(f"Invalid day argument. Please use one of the following: `{'`, `'.join(self.days)}`.")
                return

            try:
                time = time.split(':')
            except:
                await ctx.send("Invalid time argument. Please use the format `[HOUR]:[MINUTE]:[SECOND]`.")
                return

            self.scheduler.add_job(self.new_reminder, 'cron', day_of_week=day, hour=int(time[0]), minute=int(time[1]), second=int(time[2]), timezone='EST', args=[ctx, message])

        elif kind == 'date':
            try:
                self.scheduler.add_job(self.new_reminder, 'date', run_date=f"{day} {time}", timezone='EST', args=[ctx, message])
            except:
                await ctx.send("Invalid date or time argument. Please use the format `[YEAR]-[MONTH]-[DATE] [HOURS]:[MINUTES]:[SECONDS]`.")
                return
        else:
            await ctx.send("Invalid reminder type.")

        await ctx.send("Reminder successfully set!")


def setup(bot):
    bot.add_cog(ScheduleCog(bot))

def teardown(bot):
    bot.remove_cog(ScheduleCog(bot))