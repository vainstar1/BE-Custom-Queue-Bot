import discord
from discord.ext import commands
from discord import app_commands
import pandas as pd

PHRASES_FILE = 'phrases.csv'

class addphrase(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="addphrase", description="Adds a phrase to the phrases list. Can only be used by Odd")
    async def addphrase(self, interaction: discord.Interaction, phrase: str):
        if interaction.user.id != 745762346479386686: 
            await interaction.response.send_message("You are not authorized to add phrases.", ephemeral=True)
            return

        phrases = self.read_phrases_from_csv(PHRASES_FILE)

        if phrase in phrases:
            await interaction.response.send_message(f"Phrase '{phrase}' already exists in the list.", ephemeral=True)
        else:
            phrases.append(phrase)
            pd.DataFrame(phrases).to_csv(PHRASES_FILE, header=False, index=False, encoding='utf-8')
            await interaction.response.send_message(f"Phrase '{phrase}' has been added.", ephemeral=True)

    def read_phrases_from_csv(self, file_path):
        try:
            phrases_df = pd.read_csv(file_path, header=None, encoding='utf-8')
            phrases = phrases_df[0].tolist()
        except FileNotFoundError:
            phrases = []
        return phrases

async def setup(client:commands.Bot) -> None:
    await client.add_cog(addphrase(client))