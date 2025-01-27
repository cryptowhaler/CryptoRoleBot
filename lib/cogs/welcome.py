from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Forbidden
from ..db import db

class Welcome(Cog):
    def __init__(self,bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")
            # await self.bot.stdout.send("Fun cog Ready...")
            # print("Fun Cog Ready...")

    @Cog.listener()
    async def on_member_join(self, member):
        db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)
        # await self.bot.get_channel(833334526348099585).send(f"Hi {member.mention}! Welcome to MARS Protocol ")
        try:
            await member.send(f"Welcome to **{member.guild.name}**! Enjoy your stay!")
        except Forbidden:
            pass

    @Cog.listener( )
    async def on_member_leave(self, member):
        pass

def setup(bot):
    bot.add_cog(Welcome(bot))