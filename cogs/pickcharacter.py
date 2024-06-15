import discord
from discord import app_commands
from discord.ext import commands
import random

class pickcharacter(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client    
    
    @app_commands.command(name="pickcharacter", description="Randomly picks a character. Leave blank for any class, or you can specify a class.")
    async def pickcharacter(self, interaction: discord.Interaction, category: str = None):
        damage = ["Daemon", "Gizmo", "Nidhoggr", "Maeve", "Cass"]
        support = ["Miko", "Kulev", "Zerocool", "Azrael"]
        tank = ["El Bastardo", "Mekko", "Makutu", "Buttercup"]

        if category:
            category = category.lower()

            if category == "damage":
                character_list = damage
                category_message = "damage"
            elif category == "support":
                character_list = support
                category_message = "support"
            elif category == "tank":
                character_list = tank
                category_message = "tank"
            else:
                await interaction.response.send_message("Invalid category provided. Please specify 'damage', 'support', 'tank', or leave blank for any category.", ephemeral=True)
                return
        else:
            character_list = damage + support + tank
            category_message = "character"

        character = random.choice(character_list)
        await interaction.response.send_message(f"Your randomly picked {category_message}: {character}", ephemeral=True)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(pickcharacter(client))

