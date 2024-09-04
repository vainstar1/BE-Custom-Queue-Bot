import discord
from discord import app_commands
from discord.ext import commands
import shared_state  

class join(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client    

    @app_commands.command(name="join", description="Automatically places you on the list.")
    async def join(self, interaction: discord.Interaction):
        if shared_state.customs_started:
            nickname = interaction.user.nick
            username = interaction.user.name

            if nickname:
                username = nickname

            if username not in shared_state.players_list:
                shared_state.players_list.append(username)
                await interaction.response.send_message(f"{username} has been added to the list.")
            else:
                await interaction.response.send_message(f"{username} is already in the list.")
        else:
            await interaction.response.send_message("Customs haven't started yet!", ephemeral=True)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(join(client))
