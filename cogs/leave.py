import discord
from discord import app_commands
from discord.ext import commands

customs_started = False
players_list = []

class leave(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client        
    
    @app_commands.command(name="leave", description="Automatically takes you off the list.")
    async def leave(self, interaction: discord.Interaction):
        global customs_started, players_list

        if customs_started:
            nickname = interaction.user.nick
            username = interaction.user.name

            if nickname:
                username = nickname
            
            if username in players_list:
                players_list.remove(username)
                await interaction.response.send_message(f"{username} has been removed from the list.")
            else:
                await interaction.response.send_message(f"{username} is not in the list.")
        else:
            await interaction.response.send_message("Customs haven't started yet!")

async def setup(client:commands.Bot) -> None:
    await client.add_cog(leave(client))
