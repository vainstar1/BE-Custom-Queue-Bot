import csv
import discord
from discord.ext import commands
from discord import app_commands

class ViewPhrases(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client 

    @app_commands.command(name='viewphrases', description="View the phrases file. Can only be used by Odd.")
    async def view_phrases(self, interaction: discord.Interaction):
        user_id = 745762346479386686

        if interaction.user.id != user_id:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            return

        phrases = self.load_phrases_from_csv()
        
        if phrases:
            numbered_phrases = "\n".join([f"{i+1}. {phrase}" for i, phrase in enumerate(phrases)])
            await interaction.response.send_message(f"Here are the phrases:\n{numbered_phrases}", ephemeral=True)
        else:
            await interaction.response.send_message("No phrases found in the CSV file.", ephemeral=True)

    def load_phrases_from_csv(self):
        with open('phrases.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            return [row[0] for row in reader if len(row) > 0 and not row[0].startswith('#') and row[0].strip()]

async def setup(client: commands.Bot) -> None:
    await client.add_cog(ViewPhrases(client))
