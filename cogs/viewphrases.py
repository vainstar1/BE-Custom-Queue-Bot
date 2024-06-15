import discord
from discord import app_commands
from discord.ext import commands
import pandas as pd

PHRASES_FILE = 'phrases.csv'

class viewphrases(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client        
    
    def read_phrases_from_csv(self, file_path):
        try:
            df = pd.read_csv(file_path, header=None)
            phrases = df[0].tolist()
            return phrases
        except FileNotFoundError:
            return []

    @app_commands.command(name="viewphrases", description="View the full list of phrases. This command can only be used by Odd.")
    async def viewphrases(self, interaction: discord.Interaction):
        if interaction.user.id != 745762346479386686: # user ID for Odd (me) :3
            await interaction.response.send_message("You are not authorized to view the phrases.", ephemeral=True)
            return

        phrases = read_phrases_from_csv(PHRASES_FILE)

        if phrases:
            phrases_str = "\n".join(phrases)
            await interaction.response.send_message(f"List of phrases:\n{phrases_str}", ephemeral=True)
        else:
            await interaction.response.send_message("No phrases found.", ephemeral=True)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(viewphrases(client))
