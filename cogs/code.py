import discord
from discord import app_commands
from discord.ext import commands

customs_started = False
current_code = None

class code(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @app_commands.command(name="code", description="Displays the currently active custom code.")
    async def code(self, interaction: discord.Interaction):
        global customs_started, current_code

        if customs_started:
            await interaction.response.send_message(f"The currently active custom code is: `{current_code}`")
        else:
            await interaction.response.send_message("Customs haven't started yet!", ephemeral=True)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(code(client))
