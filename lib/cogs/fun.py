from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Member
from typing import Optional

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="hello",aliases=["hi"])
    async def say_hello(self, ctx):
        await ctx.send(f"Hello {ctx.author.mention}!")

    @command(name="slap", aliases=["hit"])
    async def slap_member(self, ctx, member:Member, *, reason:Optional[str] ):
        pass

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")
            # await self.bot.stdout.send("Fun cog Ready...")
            # print("Fun Cog Ready...")


def setup(bot):
    bot.add_cog(Fun(bot))
