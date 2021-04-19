from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from discord import Intents
from discord import Embed
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ..db import db
from apscheduler.triggers.cron import CronTrigger
from glob import glob
from asyncio import sleep
PREFIX = "+"
SERVER_ID = 833334525890134027
GENERAL_CHANNEL_ID = 833334526348099585
OWNER_IDS = [700177326830518332]  # MY ID
COGS = [path.split("/")[-1][:-3] for path in glob("./lib/cogs/*.py")]  # returns the name of the cogs


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self,cog,False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog ready")

    def all_ready(self):
        return all([getattr(self,cog) for cog in COGS])



class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS, intents=Intents.all())

    def setup(self):
        # print(COGS)
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{cog} cog loaded")

        print("setup complete")

    def run(self, version):
        self.VERSION = version

        print("running setup...")
        self.setup()

        with open("./lib/bot/token", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("running bot... ")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("BOT IS CONNECTED")

    async def on_disconnect(self):
        print("BOT DIS-CONNECTED")

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(SERVER_ID)  # Server's ID
            self.stdout = self.get_channel(GENERAL_CHANNEL_ID)
            # self.scheduler.add_job(self.print_message, CronTrigger(second="0,15,30,45"))
            self.scheduler.start()

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            self.ready = True
            print("BOT READY... ")
            await self.stdout.send("Now Online")

            # embed = Embed(title="Now Online", description="Bot is now online", colour=0xFF0000)
            # fields = [("Name 1", "value 1", True),
            #           ("Name 2", "value 2", True),
            #           ("Name 3", "value 3", False)]
            # for name, value, inline in fields:
            #     embed.add_field(name=name, value=value, inline=inline)
            # embed.set_footer(text="This is a footer")
            # embed.set_author(name="Testing Bot", icon_url=self.guild.icon_url)
        else:
            print("BOT RECONNECTED... ")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong")

        await self.stdout.send("An error occured")
        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass
        elif hasattr(exc, "original"):
            raise exc.original
        else:
            raise exc

    async def print_message(self):
        await self.stdout.send("I am a timed notification")


bot = Bot()
