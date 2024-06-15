import discord
from discord import app_commands
from discord.ext import commands

customs_started = False

class end(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client    

    @app_commands.command(name="end", description="Ends the currently active customs list.")
    async def end(self, interaction: discord.Interaction):
        global customs_started

        if customs_started:
            customs_started = False
            await interaction.response.send_message("You have ended customs.")
        else:
            await interaction.response.send_message("Customs haven't started yet!", ephemeral=True)

        await bot.change_presence(activity=discord.Game(name="!commands"))

async def setup(client:commands.Bot) -> None:
    await client.add_cog(end(client))

