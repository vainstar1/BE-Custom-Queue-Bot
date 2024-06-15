import discord
from discord import app_commands
from discord.ext import commands

customs_started = False
players_list = []

class list(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client       
   
    @app_commands.command(name="list", description="Displays the list of players.")
    async def list(self, interaction: discord.Interaction):
        if customs_started:
            total_players = len(players_list)
            if total_players > 0:
                players = "\n".join([f"{i + 1}. {user}" for i, user in enumerate(players_list)])
                await interaction.response.send_message(f"There are {total_players} people in the list:\n{players}")
            else:
                await interaction.response.send_message(f"There is nobody in the current list.")
        else:
            await interaction.response.send_message(f"Customs haven't started yet! Use /start (code) to start them.")

async def setup(client:commands.Bot) -> None:
    await client.add_cog(list(client))
