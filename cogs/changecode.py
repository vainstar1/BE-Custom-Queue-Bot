import discord
from discord import app_commands
from discord.ext import commands
import shared_state

customs_started = False
current_code = None

class changecode(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @app_commands.command(name="changecode", description="Changes the currently active custom code.")
    async def changecode(self, interaction: discord.Interaction, new_code: str):

        if shared_state.customs_started:
            shared_state.current_code = new_code
            await interaction.response.send_message(f"Custom code changed to `{new_code}`.")
        else:
            await interaction.response.send_message("Customs haven't started yet!")

async def setup(client:commands.Bot) -> None:
    await client.add_cog(changecode(client))
