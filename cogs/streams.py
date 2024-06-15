import discord
from discord import app_commands
from discord.ext import commands
import requests
import datetime
import pytz
import os

TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
TWITCH_OAUTH_TOKEN = os.getenv('TWITCH_OAUTH_TOKEN')
game_id = "512990"
stream_ping = f"<@&{os.getenv('STREAM_PING_ROLE_ID')}>"
STREAM_CHANNEL_ID = 1207219899416580107
STREAM_CHANNEL_ID2 = 1237240055840505906

class streams(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client        
    
    def get_active_streams_in_category(game_id, TWITCH_CLIENT_ID, TWITCH_OAUTH_TOKEN):
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

    async def send_streams_to_channels():
        global sent_streams

        active_streams = get_active_streams_in_category(game_id, TWITCH_CLIENT_ID, TWITCH_OAUTH_TOKEN)

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

    
    @app_commands.command(name="streams", description="Displays all currently active livestreams in the Bleeding Edge Twitch category.")
    async def streams(self, interaction: discord.Interaction):
        active_streams = get_active_streams_in_category(game_id, TWITCH_CLIENT_ID, TWITCH_OAUTH_TOKEN)

        if active_streams:
            for stream in active_streams:
                stream_link = f"https://www.twitch.tv/{stream['user_login']}"
                
                start_time = datetime.datetime.strptime(stream['started_at'], "%Y-%m-%dT%H:%M:%SZ")
                utc = pytz.utc
                est = pytz.timezone('America/New_York')
                start_time = utc.localize(start_time).astimezone(est)
                
                formatted_start_time = start_time.strftime("%m/%d/%Y, %I:%M %p")
                message = f"Title: {stream['title']}\nStream Started at: {formatted_start_time} EST\nViewer Count: {stream['viewer_count']}\nStream Link: {stream_link}\n-------------"
                await interaction.response.send_message(message)
        else:
            await interaction.response.send_message("No one is streaming Bleeding Edge right now.")

async def setup(client:commands.Bot) -> None:
    await client.add_cog(streams(client))

