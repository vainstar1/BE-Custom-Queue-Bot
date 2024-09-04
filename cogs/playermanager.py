import discord
from discord.ext import commands
from discord import app_commands
import pandas as pd
import os

PLAYERS_FILE = 'players.csv'

class PlayerManager(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.characters = {
            "Daemon": "damage", "Gizmo": "damage", "Nidhoggr": "damage", "Maeve": "damage", "Cass": "damage",
            "Miko": "support", "Kulev": "support", "Zerocool": "support", "Azrael": "support",
            "El Bastardo": "tank", "Mekko": "tank", "Makutu": "tank", "Buttercup": "tank",
            "Any": "any"
        }
        self.initialize_csv()

    def initialize_csv(self):
        if not os.path.exists(PLAYERS_FILE) or os.path.getsize(PLAYERS_FILE) == 0:
            df = pd.DataFrame(columns=["Username", "MainCharacter"])
            df.to_csv(PLAYERS_FILE, index=False, encoding='utf-8')

    @app_commands.command(name="addplayer", description="Adds a player to the players list with an optional main character.")
    async def addplayer(self, interaction: discord.Interaction, username: str, main_character: str = None):
        players = self.read_players_from_csv(PLAYERS_FILE)

        if main_character:
            main_character_lower = main_character.lower()
            if main_character_lower not in [char.lower() for char in self.characters.keys()]:
                await interaction.response.send_message(f"Character '{main_character}' is not a valid character.", ephemeral=True)
                return
            # Use the correctly capitalized form for storage
            main_character = [key for key in self.characters if key.lower() == main_character_lower][0]

        players.append([username, main_character])
        pd.DataFrame(players, columns=["Username", "MainCharacter"]).to_csv(PLAYERS_FILE, index=False, encoding='utf-8')
        await interaction.response.send_message(f"Player '{username}' has been added with main character '{main_character}'.")

    @app_commands.command(name="removeplayer", description="Removes a player from the players list.")
    async def removeplayer(self, interaction: discord.Interaction, username: str):
        players = self.read_players_from_csv(PLAYERS_FILE)
        updated_players = [player for player in players if player[0] != username]

        if len(players) == len(updated_players):
            await interaction.response.send_message(f"Player '{username}' was not found.", ephemeral=True)
        else:
            pd.DataFrame(updated_players, columns=["Username", "MainCharacter"]).to_csv(PLAYERS_FILE, index=False, encoding='utf-8')
            await interaction.response.send_message(f"Player '{username}' has been removed.")

    @app_commands.command(name="viewplayers", description="Views all players categorized by their main character.")
    async def viewplayers(self, interaction: discord.Interaction):
        players = self.read_players_from_csv(PLAYERS_FILE)
        categorized_players = self.categorize_players(players)
        total_players = sum(len(players_list) for players_list in categorized_players.values())
        embed = self.create_embed(categorized_players, total_players)
        await interaction.response.send_message(embed=embed)

    def read_players_from_csv(self, file_path):
        try:
            players_df = pd.read_csv(file_path, encoding='utf-8')
            players = players_df.values.tolist()
        except pd.errors.EmptyDataError:
            players = []
        return players

    def categorize_players(self, players):
        categorized = {character: [] for character in self.characters.keys()}
        for player in players:
            username, main_character = player
            if main_character:
                main_character_capitalized = [char for char in categorized if char.lower() == main_character.lower()]
                if main_character_capitalized:
                    categorized[main_character_capitalized[0]].append(username)
        return categorized

    def create_embed(self, categorized_players, total_players):
        embed = discord.Embed(title="Player Mains", color=discord.Color.blue())
        for character, usernames in categorized_players.items():
            if usernames:
                embed.add_field(name=f"{character} Mains", value="\n".join(usernames), inline=False)
        embed.set_footer(text=f"Total Players: {total_players}")
        return embed

async def setup(client: commands.Bot) -> None:
    await client.add_cog(PlayerManager(client))
