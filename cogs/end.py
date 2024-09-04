import discord
from discord import app_commands
from discord.ext import commands
import shared_state  

class end(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client    

    @app_commands.command(name="end", description="Ends the currently active customs list.")
    async def end(self, interaction: discord.Interaction):
        if shared_state.customs_started:
            shared_state.customs_started = False
            shared_state.players_list.clear()  # Clear the player list when ending customs
            await interaction.response.send_message("You have ended customs.")
        else:
            await interaction.response.send_message("Customs haven't started yet!", ephemeral=True)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(end(client))
