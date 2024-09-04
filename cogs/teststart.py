import discord
from discord import app_commands
from discord.ext import commands
import shared_state 

GENERAL_CHANNEL_ID = 1099419224914542693
ROLE_ID = 1198429813103403148

class teststart(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client    

    @app_commands.command(name="teststart", description="Starts a customs list with the given code.")
    async def start(self, interaction: discord.Interaction, code: str): 
        nickname = interaction.user.nick
        username = interaction.user.name
        
        if nickname:
            username = nickname

        if username not in shared_state.players_list:
            shared_state.players_list.append(username)

        if shared_state.customs_started:
            return await interaction.response.send_message("A custom queue is already active.")
        
        shared_state.customs_started = True
        shared_state.current_code = code

        # Determine the name to use (nickname or username)
        invoker_name = interaction.user.display_name if interaction.user.display_name else interaction.user.name
        start_message = f"{invoker_name} has initiated customs with code: {code}"

        channel = interaction.guild.get_channel(GENERAL_CHANNEL_ID)
        if channel is not None:
            await interaction.response.send_message("You have initiated customs. Sending ping in general.", ephemeral=True)
           # await channel.send(start_message)
        else:
            await interaction.response.send_message("Failed to find the specified channel.")

async def setup(client: commands.Bot) -> None:
    await client.add_cog(teststart(client))
