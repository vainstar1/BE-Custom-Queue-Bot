import discord
from discord import app_commands
from discord.ext import commands
import shared_state

GENERAL_CHANNEL_ID = 1099419224914542693
ROLE_ID = 1198429813103403148

class start(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client    

    @app_commands.command(name="start", description="Starts a customs list with the given code.")
    async def start(self, interaction: discord.Interaction, code: str): 
        nickname = interaction.user.nick
        username = interaction.user.name
        
        if nickname:
            username = nickname

        if username not in shared_state.players_list:
            shared_state.players_list.append(username)

        if shared_state.customs_started:
            return await interaction.response.send_message("A custom queue is already active.")

        rolePing = f"<@&{ROLE_ID}>"
        shared_state.customs_started = True
        # Remove the line shared_state.players_list.clear() from here
        
        shared_state.current_code = code
        startMessage = (f"{rolePing} {interaction.user.mention} Started a custom queue with code: {code}. Type /join to be put on the list.")

        channel = interaction.guild.get_channel(GENERAL_CHANNEL_ID)
        if channel is not None:
            await interaction.response.send_message("You have initiated customs. Sending ping in general.", ephemeral=True)
            await channel.send(startMessage)
        else:
            await interaction.response.send_message("Failed to find the specified channel.")

async def setup(client: commands.Bot) -> None:
    await client.add_cog(start(client))
