import pathlib
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import random
import pytz
import datetime
import time
import platform
import csv

load_dotenv()

TOKEN = os.getenv('TOKEN')
CQBTOKEN = os.getenv('CQBTOKEN')

cooldown_time = 1800  # Cooldown of 30 minutes
last_used = 0

def load_phrases_from_csv():
    with open('phrases.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        return [row[0] for row in reader if len(row) > 0 and row[0].strip()]

trigger_phrases = load_phrases_from_csv()

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=discord.Intents().all())
        self.token_expiry = datetime.datetime.utcnow()
        self.cogslist = [
            "cogs.add",
            "cogs.changecode",
            "cogs.code",
            "cogs.createimage",
            "cogs.end",
            "cogs.join",
            "cogs.leave",
            "cogs.list",
            "cogs.pickcharacter",
            "cogs.remove",
            "cogs.removephrase",
            "cogs.spreadsheet",
            "cogs.start",
            "cogs.streams",
            "cogs.teststart",
            "cogs.trollcog",
            "cogs.playermanager",
            "cogs.viewphrases"
        ]

    async def setup_hook(self):
        for ext in self.cogslist:
            await self.load_extension(ext)

    async def on_ready(self):
        print(f"Logged in as {self.user.name}")
        print(f"Bot ID: {self.user.id}")
        print(f"Discord Version: {discord.__version__}")
        print(f"Python Version: {platform.python_version()}")
        self.status_task.start()
        synced = await self.tree.sync()

    @commands.Cog.listener()
    async def on_message(self, message):
        global last_used
        current_time = time.time()

        if message.author == self.user:
            return

        if any(phrase in message.content.lower() for phrase in trigger_phrases):
            if current_time - last_used >= cooldown_time:
                last_used = current_time
                matched_phrase = next((p for p in trigger_phrases if p in message.content.lower()), None)
                if matched_phrase:
                    await message.reply(f'"{matched_phrase}" 🤓')
            else:
                remaining_time = int(cooldown_time - (current_time - last_used))
                print(f"on cooldown for {remaining_time} seconds")

        await self.process_commands(message)

    @tasks.loop(seconds=60)
    async def status_task(self):
        phrases = ["HITSTUN THE GIZMO", "press Y to heal on zerocool", "move your camera to see your team"]
        new_status = random.choice(phrases)
        await self.change_presence(activity=discord.Game(name=new_status))

client = Client()

client.run(CQBTOKEN)
