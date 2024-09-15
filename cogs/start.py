import discord
from discord import app_commands
from discord.ext import commands
import json
import os
import shared_state

DATABASE_FILE = 'server_settings.json'

def load_settings():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_settings(settings):
    with open(DATABASE_FILE, 'w') as file:
        json.dump(settings, file, indent=4)

server_settings = load_settings()

class Start(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client    

    @app_commands.command(name="setup", description="Setup the channel and message format for custom games.")
    async def setup(self, interaction: discord.Interaction, channel: discord.TextChannel, role: discord.Role = None, message: str = None):
        server_id = str(interaction.guild.id)
        if server_id not in server_settings:
            server_settings[server_id] = {}

        if channel:
            server_settings[server_id]['channel_id'] = channel.id
        if role:
            server_settings[server_id]['role_id'] = role.id
        if message:
            server_settings[server_id]['start_message'] = message
        else:
            role_ping = f"<@&{server_settings[server_id].get('role_id', '')}>" if 'role_id' in server_settings[server_id] else ""
            server_settings[server_id]['start_message'] = f"{role_ping} {{user_mention}} Started a custom queue with code: {{code}}. Type /join to be put on the list."

        save_settings(server_settings)
        embed = discord.Embed(title="Setup Completed", description="Setup completed successfully.", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="view-setup", description="View the current setup for custom games.")
    async def view_setup(self, interaction: discord.Interaction):
        server_id = str(interaction.guild.id)
        settings = server_settings.get(server_id, {})

        channel_id = settings.get('channel_id', 'Not set')
        role_id = settings.get('role_id', 'Not set')
        start_message = settings.get('start_message', 'Not set')

        role_name = f"<@&{role_id}>" if role_id != 'Not set' else 'None'
        channel = interaction.guild.get_channel(int(channel_id)) if channel_id != 'Not set' else 'None'

        embed = discord.Embed(title="Current Setup", color=discord.Color.blue())
        embed.add_field(name="Channel", value=channel if channel != 'None' else 'None', inline=False)
        embed.add_field(name="Role", value=role_name, inline=False)
        embed.add_field(name="Message", value=start_message, inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="edit-setup", description="Edit the setup for custom games.")
    async def edit_setup(self, interaction: discord.Interaction, channel: discord.TextChannel = None, role: discord.Role = None, message: str = None):
        server_id = str(interaction.guild.id)
        if server_id not in server_settings:
            server_settings[server_id] = {}

        if channel:
            server_settings[server_id]['channel_id'] = channel.id
        if role is None:
            server_settings[server_id].pop('role_id', None)
        elif role:
            server_settings[server_id]['role_id'] = role.id
        if message:
            server_settings[server_id]['start_message'] = message

        if 'role_id' not in server_settings[server_id]:
            role_ping = ""
        else:
            role_ping = f"<@&{server_settings[server_id].get('role_id', '')}>"

        if 'start_message' not in server_settings[server_id]:
            server_settings[server_id]['start_message'] = f"{role_ping} {{user_mention}} Started a custom queue with code: {{code}}. Type /join to be put on the list."
        else:
            start_message_template = server_settings[server_id]['start_message']
            if role_ping:
                server_settings[server_id]['start_message'] = start_message_template
            else:
                server_settings[server_id]['start_message'] = start_message_template.replace(f"{role_ping} ", "")

        save_settings(server_settings)
        embed = discord.Embed(title="Setup Updated", description="Setup updated successfully.", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="remove-setup", description="Remove the channel, role, message, or all setup components.")
    async def remove_setup(self, interaction: discord.Interaction, channel: bool = False, role: bool = False, message: bool = False, all: bool = False):
        server_id = str(interaction.guild.id)
        
        if all:
            server_settings.pop(server_id, None)
            save_settings(server_settings)
            embed = discord.Embed(title="Setup Reset", description="All setup components have been removed.", color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
            return

        if server_id not in server_settings:
            embed = discord.Embed(title="No Setup Found", description="No setup found for this server.", color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
            return

        if channel:
            server_settings[server_id].pop('channel_id', None)
        if role:
            server_settings[server_id].pop('role_id', None)
        if message:
            server_settings[server_id].pop('start_message', None)
        
        if not server_settings[server_id]:
            server_settings.pop(server_id, None)

        save_settings(server_settings)
        embed = discord.Embed(title="Setup Component Removed", description="Setup component(s) removed successfully.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="start", description="Starts a customs list with the given code.")
    async def start(self, interaction: discord.Interaction, code: str): 
        server_id = str(interaction.guild.id)
        settings = server_settings.get(server_id, {})
        channel_id = settings.get('channel_id')
        role_id = settings.get('role_id')
        start_message_template = settings.get('start_message', '{user_mention} Started a custom queue with code: {code}. Type /join to be put on the list.')

        nickname = interaction.user.nick
        username = interaction.user.name
        
        if nickname:
            username = nickname

        if username not in shared_state.players_list:
            shared_state.players_list.append(username)

        if shared_state.customs_started:
            embed = discord.Embed(title="Customs Active", description="A custom queue is already active.", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)

        shared_state.customs_started = True
        shared_state.current_code = code
        
        role_ping = f"<@&{role_id}>" if role_id else ""
        start_message = start_message_template.format(user_mention=interaction.user.mention, code=code)
        start_message = f"{role_ping} {start_message}"

        channel = interaction.guild.get_channel(channel_id)
        if channel is not None:
            embed = discord.Embed(title="Customs Initiated", description="You have initiated customs. Sending ping in the setup channel.", color=discord.Color.green())
            await interaction.response.send_message(embed=embed)
            await channel.send(start_message)
        else:
            embed = discord.Embed(title="Channel Not Found", description="Failed to find the specified channel.", color=discord.Color.red())
            await interaction.response.send_message(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Start(client))
