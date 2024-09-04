import discord
from discord import app_commands
from discord.ext import commands
import pandas as pd

PHRASES_FILE = 'phrases.csv'

class removephrase(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client    
    
    def read_phrases_from_csv(self, file_path):
        try:
            df = pd.read_csv(file_path, header=None)
            phrases = df[0].tolist()
            return phrases
        except FileNotFoundError:
            return []

    @app_commands.command(name="removephrase", description="Removes a phrase from the phrases list. This command can only be used by Odd.")
    async def removephrase(self, interaction: discord.Interaction, phrase: str):
        if interaction.user.id != 745762346479386686: 
            await interaction.response.send_message("You are not authorized to remove phrases.", ephemeral=True)
            return

        phrases = self.read_phrases_from_csv(PHRASES_FILE)

        if phrase in phrases:
            phrases.remove(phrase)
            pd.DataFrame(phrases).to_csv(PHRASES_FILE, header=False, index=False, encoding='utf-8')
            await interaction.response.send_message(f"Phrase '{phrase}' has been removed.")
        else:
            await interaction.response.send_message(f"Phrase '{phrase}' not found.", ephemeral=True)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(removephrase(client))
