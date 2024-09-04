import pathlib
import discord
from discord.ext import commands, tasks
from discord import app_commands
from dotenv import load_dotenv
import os
import random
import pytz
import datetime
import requests
from PIL import Image, ImageDraw, ImageFont
import io
from colorama import Back, Fore, Style
import time
import platform

load_dotenv()

TOKEN = os.getenv('TOKEN')
CQBTOKEN = os.getenv('CQBTOKEN')
TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
TWITCH_OAUTH_TOKEN = os.getenv('TWITCH_OAUTH_TOKEN')
TWITCH_REFRESH_TOKEN = os.getenv('TWITCH_REFRESH_TOKEN')
TWITCH_CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')
MESSAGE_ID = os.getenv('MESSAGE_ID')
ROLE_ID = os.getenv('ROLE_ID')
ROLE_ID2 = os.getenv('ROLE_ID2')

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
            "cogs.playermanager"
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
        if message.author == self.user:
            return

        if message.content.startswith('!'):
            await self.process_commands(message)
            return

        await self.process_commands(message)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == int(MESSAGE_ID) and str(payload.emoji) == '👍':
            guild = self.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            role = guild.get_role(ROLE_ID)

            if member is not None and role is not None:
                await member.add_roles(role)

        if payload.message_id == int(MESSAGE_ID) and str(payload.emoji) == '✅':
            guild = self.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            role = guild.get_role(ROLE_ID2)

            if member is not None and role is not None:
                await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == int(MESSAGE_ID) and str(payload.emoji) == '👍':
            guild = self.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            role = guild.get_role(ROLE_ID)

            if member is not None and role is not None:
                await member.remove_roles(role)

        if payload.message_id == int(MESSAGE_ID) and str(payload.emoji) == '✅':
            guild = self.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            role = guild.get_role(ROLE_ID2)

            if member is not None and role is not None:
                await member.remove_roles(role)

    @tasks.loop(seconds=60)
    async def status_task(self):
        phrases = ["HITSTUN THE GIZMO", "press Y to heal on zerocool", "move your camera to see your team"]
        new_status = random.choice(phrases)
        await self.change_presence(activity=discord.Game(name=new_status))

client = Client()

client.run(CQBTOKEN)
