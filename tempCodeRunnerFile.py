import pathlib
import discord
from discord.ext import commands, tasks
from discord import app_commands
from dotenv import load_dotenv
import os
import random
import pytz
import datetime
import pandas as pd
import unicodedata
import re
import requests
from PIL import Image, ImageDraw, ImageFont
import io
from colorama import Back, Fore, Style
import time
import platform
import json

load_dotenv()

TOKEN = os.getenv('TOKEN')
CQBTOKEN = os.getenv('CQBTOKEN')
TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
TWITCH_OAUTH_TOKEN = os.getenv('TWITCH_OAUTH_TOKEN')
STREAM_PING_ROLE_ID = os.getenv('STREAM_PING_ROLE_ID')
MESSAGE_ID = os.getenv('MESSAGE_ID')
ROLE_ID = os.getenv('ROLE_ID')
ROLE_ID2 = os.getenv('ROLE_ID2')

PHRASES_FILE = 'phrases.csv'
game_id = "512990"
sent_streams = {}
stream_ping = f"<@&{STREAM_PING_ROLE_ID}>"

ROLE_ID=1198429813103403148
ROLE_ID2=1213678901339881552
MESSAGE_ID=1239344868879237130

# test server
# STREAM_CHANNEL_ID = 1244464401885429812
# STREAM_CHANNEL_ID2 = 1244482174808490034
# GENERAL_CHANNEL_ID = 1244460996584804405
# GENERAL_CHANNEL_ID2 = 1244470972136820806
# SERVER1_ID = 1244460994470608986
# SERVER2_ID = 1245568892701769779

# test server 2
STREAM_CHANNEL_ID = 1248161533054160906
GENERAL_CHANNEL_ID = 1246669584820469845

# main server
# STREAM_CHANNEL_ID = 1207219899416580107
# STREAM_CHANNEL_ID2 = 1237240055840505906
# GENERAL_CHANNEL_ID = 1099419224914542693
# GENERAL_CHANNEL_ID2 = 1237239992917692489
# SERVER1_ID = 1057765501121601630
# SERVER2_ID = 1237239992917692486
    
class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=discord.Intents().all())
            
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
        "cogs.viewphrases"
        ]

    async def setup_hook(self):
      for ext in self.cogslist:
        await self.load_extension(ext)
    
    async def on_ready(self):
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        print(prfx + " Logged in as " + Fore.YELLOW + self.user.name)
        print(prfx + " Bot ID " + Fore.YELLOW + str(self.user.id))
        print(prfx + " Discord Version " + Fore.YELLOW + discord.__version__)
        print(prfx + " Python Version " + Fore.YELLOW + str(platform.python_version()))
        synced = await self.tree.sync()
        print(prfx + " Slash CMDs Synced " + Fore.YELLOW + str(len(synced)) + " Commands")
        self.automatic_stream_check.start()
        self.status_task.start()

    @tasks.loop(seconds=60)
    async def status_task(self):
        phrases = ["HITSTUN THE GIZMO", "press Y to heal on zerocool", "move your camera to see your team"]
        new_status = random.choice(phrases)
        await self.change_presence(activity=discord.Game(name=new_status))

    @tasks.loop(seconds=2)
    async def automatic_stream_check(self):
        await self.send_streams_to_channels()

    def get_active_streams_in_category(self, game_id, TWITCH_CLIENT_ID, TWITCH_OAUTH_TOKEN):
        url = "https://api.twitch.tv/helix/streams"
        headers = {
            "Client-ID": TWITCH_CLIENT_ID,
            "Authorization": "Bearer " + TWITCH_OAUTH_TOKEN
        }
        params = {
            "game_id": game_id
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data["data"]
        else:
            print("Error:", response.status_code)
            return []

    async def send_streams_to_channels(self):
        global sent_streams

        active_streams = self.get_active_streams_in_category(game_id, TWITCH_CLIENT_ID, TWITCH_OAUTH_TOKEN)

        if active_streams:
            for stream in active_streams:
                stream_id = stream['id']
                if stream_id not in sent_streams or not sent_streams[stream_id]:
                    stream_link = f"https://www.twitch.tv/{stream['user_login']}"

                    start_time = datetime.datetime.strptime(stream['started_at'], "%Y-%m-%dT%H:%M:%SZ")
                    utc = pytz.utc
                    est = pytz.timezone('America/New_York')
                    start_time = utc.localize(start_time).astimezone(est)

                    formatted_start_time = start_time.strftime("%m/%d/%Y, %I:%M %p")

                    message = f"{stream_ping}\nTitle: {stream['title']}\nStream Started at: {formatted_start_time} EST\nViewer Count: {stream['viewer_count']}\nStream Link: {stream_link}\n-------------"
                    channel1 = bot.get_channel(STREAM_CHANNEL_ID)
                    channel2 = bot.get_channel(STREAM_CHANNEL_ID2)
                    if channel1 and channel2:
                        await channel1.send(message)
                        await channel2.send(message)
                    sent_streams[stream_id] = True
                    print(f"Stream detected and sent: {stream['title']} - Viewer Count: {stream['viewer_count']}")
                else:
                    if stream_id in sent_streams:
                        if not stream['type'] == 'live':
                            sent_streams[stream_id] = False
        else:
            print("No active streams detected.")

    def read_phrases_from_csv(self, file_path):
        try:
            df = pd.read_csv(file_path, header=None)
            phrases = df[0].tolist()
            return phrases
        except FileNotFoundError:
            return []

    def write_phrase_to_csv(self, file_path, phrase):
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f"{phrase}\n")

    def remove_zalgo(self, text):
        return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('!'):
            await self.process_commands(message)
            return

        cleaned_content = self.remove_zalgo(message.content)

        phrases = self.read_phrases_from_csv(PHRASES_FILE)
        content_lower = cleaned_content.lower()

        for phrase in phrases:
            if re.sub(r'\W+', '', phrase.lower()) in re.sub(r'\W+', '', content_lower):
                await message.channel.send(f'"{phrase}" 🤓')
                break

        await self.process_commands(message)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if str(payload.emoji) == '😶':
            if payload.user_id == 745762346479386686:
                channel = self.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                phrase = message.content.lower().strip()
                self.write_phrase_to_csv(PHRASES_FILE, phrase)
            else:
                channel = self.get_channel(payload.channel_id)

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

client = Client()

# client.run(CQBTOKEN)

client.run(TOKEN)