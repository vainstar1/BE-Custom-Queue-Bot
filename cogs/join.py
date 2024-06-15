import discord
from discord import app_commands
from discord.ext import commands

customs_started = False
players_list = []

class join(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client    
    
    @app_commands.command(name="join", description="Automatically places you on the list.")
    async def join(self, interaction: discord.Interaction):
        global customs_started

        if customs_started:
            nickname = interaction.user.nick
            username = interaction.user.name

            if nickname:
                username = nickname
            
            if username not in players_list:
                players_list.append(username)
                await interaction.response.send_message(f"{username} has been added to the list.")
        else:
            await interaction.response.send_message("Customs haven't started yet!", ephemeral=True)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(join(client))

